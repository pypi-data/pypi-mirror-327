import io
import json
import os
import sys
import traceback

import yaml
from loguru import logger
from natsort import natsorted
from pydantic import BaseModel, Field

from ..core.cli.watch import ReloadLayoutMessage
from ..core.communication import send_message
from ..core.netlist import try_get_ports
from ..core.schema import get_netlist_schema
from ..core.shared import (
    activate_pdk_by_name,
    build_cell,
    clear_cells_from_cache,
    fix_log_line_numbers,
    get_python_cells,
    get_yaml_cell_name,
    list_cells_from_regex,
)
from ..settings import SETTINGS as s
from .app import PDK, PROJECT_DIR, app


@app.get("/watch/on-created")
def on_created(path: str):
    result = save_gds(path)
    logger.info(f"created {path}.")
    return result.model_dump()


@app.get("/watch/on-modified")
def on_modified(path: str):
    result = save_gds(path)
    logger.info(f"modified {path}.")
    return result.model_dump()


@app.get("/watch/on-deleted")
def on_deleted(path: str):
    result = Result(errors=["No on-deleted callback implemented."])
    logger.info(f"did not delete {path}. (not implemented)")
    return result.model_dump()


class Result(BaseModel):
    log: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


def save_gds(path) -> Result:
    logger.info(f"saving {path}...")
    result = Result()
    pdk = activate_pdk_by_name(PDK)
    path = os.path.abspath(path)
    dir = os.path.dirname(path)
    dir_repo = os.path.abspath(PROJECT_DIR)
    dir_pics = os.path.join(dir_repo, s.name)

    if not path_is_subpath_of_dir(path, dir_pics):
        result.errors.append(f"path {path!r} is not a subpath of {dir_pics!r}.")
        return result

    dir_gds = os.path.abspath(os.path.join(dir_repo, "build", "gds", os.path.relpath(dir, dir_pics)))
    os.makedirs(dir_gds, exist_ok=True)
    logger.info(f"{dir_gds=}")

    dir_ports = os.path.join(dir_gds, "ports")
    os.makedirs(dir_ports, exist_ok=True)
    logger.info(f"{dir_ports=}")

    dir_log = os.path.abspath(os.path.join(dir_repo, "build", "log", os.path.relpath(dir, dir_pics)))
    os.makedirs(dir_log, exist_ok=True)
    logger.info(f"{dir_log=}")

    dir_schema = os.path.abspath(os.path.join(dir_repo, "build", "schemas", os.path.relpath(dir, dir_pics)))
    os.makedirs(dir_schema, exist_ok=True)
    logger.info(f"{dir_schema=}")

    if path.endswith(".pic.yml"):
        generate_schema = True
        names = [get_yaml_cell_name(path)]
    elif path.endswith(".py"):
        generate_schema = False
        names = natsorted(set(get_python_cells(dir_pics, [path])) | {*list_cells_from_regex(path)})
    else:
        result.errors.append(f"path {path!r} is not a .pic.yml of a .py file.")
        return result

    logger.info(f"{names=}")
    result.log.append(f"cells: {names}.")

    clear_cells_from_cache(pdk, *names)

    for name in names:
        if name not in pdk.cells:
            result.errors.append(f"{name} not found in PDK!")

    del pdk

    if result.errors:
        return result
    logger.info(f"{result=}")

    busy_paths = []
    for cell_name in names:
        path_log_busy = os.path.join(dir_log, f"{cell_name}.busy.log")
        with open(path_log_busy, "w") as file:
            file.write("")
        busy_paths.append(path_log_busy)

    for cell_name in names:
        logger.info(f"{cell_name=}")
        path_gds = os.path.join(dir_gds, f"{cell_name}.gds")
        path_ports = os.path.join(dir_ports, f"{cell_name}.json")
        path_log = os.path.join(dir_log, f"{cell_name}.log")
        path_log_busy = os.path.join(dir_log, f"{cell_name}.busy.log")
        path_schema = os.path.join(dir_schema, f"{cell_name}.json")

        exc = None
        comp = None
        file = io.StringIO()
        old_stdout, sys.stdout = sys.stdout, file
        old_stderr, sys.stderr = sys.stderr, file
        try:
            func = build_cell(path, cell_name)
            comp = func()
            comp.write(path_gds)
            ports = try_get_ports(comp)
            with open(path_ports, "w") as port_file:
                json.dump(ports, port_file)
            logger.success(f"SUCCESS: Succesfully built '{cell_name}.gds'.")
            file.write(f"SUCCESS: Succesfully built '{cell_name}.gds'.")
        except Exception as e:
            exc = e
            logger.error(f"ERROR building {cell_name}.")
            file.write(f"ERROR building {cell_name}.\n")
            traceback.print_exc(file=file)  # DO NOT CHANGE TO RICH TRACEBACK
        finally:
            if os.path.exists(path_log_busy):
                os.remove(path_log_busy)
            with open(path_log, "w") as f:
                f.write(fix_log_line_numbers(file.getvalue()))
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        send_message(ReloadLayoutMessage(cell=cell_name))

        if exc is not None:
            msg = f"Could not build {cell_name!r} [{exc.__class__.__name__}]. Please check logs."
            logger.error(msg)
            result.errors.append(msg)
            continue

        if comp is None:  # this should actually never happen
            logger.error(f"Could not build {cell_name!r} [Unknown Exception]. Please check logs.")
            result.errors.append(f"Could not build {cell_name!r} [Unknown Exception]. Please check logs.")
            continue

        result.log.append(f"SUCCESS. -> {path_gds}")

        if generate_schema:
            try:
                netlist = yaml.safe_load(open(path))
                schema = get_netlist_schema(netlist)
                with open(path_schema, "w") as file:
                    file.write(json.dumps(schema, indent=2))
                logger.success(f"{cell_name}: schema generation succeeded.")
                result.log.append(f"{cell_name}: schema generation succeeded.")
            except Exception:
                logger.error(f"{cell_name}: schema generation failed.")
                result.errors.append(f"{cell_name}: schema generation failed.")

        logger.success(f"{cell_name}: saved.")

    for busy_path in busy_paths:
        if os.path.exists(busy_path):
            os.remove(busy_path)

    return result


def path_is_subpath_of_dir(path, dir):
    path = os.path.realpath(os.path.abspath(path))
    dir = os.path.realpath(os.path.abspath(path))
    if os.name == "nt":
        # paths on windows are case-insensitive
        path = path.lower()
        dir = dir.lower()
    return os.path.commonpath([path, dir]) == dir
