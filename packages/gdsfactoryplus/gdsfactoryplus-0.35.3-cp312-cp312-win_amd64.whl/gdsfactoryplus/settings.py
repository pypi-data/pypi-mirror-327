import os
import warnings
from typing import Any, Literal
from urllib.parse import urljoin

import numpy as np
import sax
import toml
from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseModel, Field, field_validator, model_validator

from gdsfactoryplus.logging import setup_logging

from .project import find_docode_project_dir, maybe_find_docode_project_dir

setup_logging()
GFP_LANDING_PAGE_BASE_URL = os.environ.get("GFP_LANDING_PAGE_BASE_URL", "https://prod.gdsfactory.com/")


try:
    load_dotenv(os.path.join(find_docode_project_dir(), ".env"))
except FileNotFoundError:
    try:
        load_dotenv(os.path.join(os.getcwd(), ".env"))
    except FileNotFoundError:
        pass


def load_settings():
    project_dir = maybe_find_docode_project_dir()
    project_toml = "" if not project_dir else os.path.join(project_dir, "pyproject.toml")
    if not os.path.isfile(project_toml):
        project_toml = ""
    global_toml = os.path.expanduser("~/.gdsfactory/gdsfactoryplus.toml")
    if not os.path.isfile(global_toml):
        global_toml = ""
    try:
        try:
            global_raw = _get_raw_docode_settings(global_toml)
        except FileNotFoundError:
            global_raw = {}
        try:
            project_raw = _get_raw_docode_settings(project_toml)
        except FileNotFoundError:
            project_raw = {}
        raw = sax.merge_dicts(global_raw, project_raw)
        settings = Settings.model_validate(raw)
        if not settings.api.key:
            settings.api.key = global_raw.get("api", {}).get("key", "").strip()
    except Exception as e:
        warnings.warn(str(e), stacklevel=2)
        settings = Settings()
    return settings


class Default:
    pass


class DefaultStr(str, Default):
    pass


class DefaultInt(int, Default):
    pass


class PdkSettings(BaseModel):
    tag: str = DefaultStr("generic")
    name: str = DefaultStr("generic")
    path: str = DefaultStr("")

    @model_validator(mode="after")
    def validate_pdk(self):
        tag = _any_env_var_like("GFP_PDK_TAG", "DOCODE_PDK_TAG")
        name = _any_env_var_like("GFP_PDK_NAME", "GFP_PDK", "DOCODE_PDK")
        path = _any_env_var_like("GFP_PDK_PATH")

        if tag:
            self.tag = tag

        if name:
            self.name = name

        if path:
            self.path = path

        self.tag = str(self.tag)
        self.name = str(self.name)
        self.path = str(self.path)

        return self


class DrcSettings(BaseModel):
    timeout: int = DefaultInt(60)
    host: str = DefaultStr("https://dodeck.gdsfactory.com")
    process: str = DefaultStr("")

    @model_validator(mode="before")
    def validate_model(obj):
        if isinstance(obj, DrcSettings):
            obj = obj.model_dump()
        if isinstance(obj, dict):
            if "duration" in obj and "timeout" not in obj:
                obj["timeout"] = obj.pop("duration")
        return obj

    @model_validator(mode="after")
    def validate_drc(self):
        timeout = _try_int(_any_env_var_like("GFP_DRC_TIMEOUT", "GFP_DRC_DURATION", "DOCODE_DRC_DURATION"))
        host = _any_env_var_like("GFP_DRC_HOST", "DOCODE_DRC_HOST", "DRC_HOST")
        process = _any_env_var_like("GFP_DRC_PROCESS")

        if timeout is not None:
            self.timeout = timeout

        if self.timeout < 30:
            self.timeout = 30

        if host:
            self.host = str(host)

        if process:
            self.process = process

        self.timeout = int(self.timeout)

        return self


class ApiSettings(BaseModel):
    domain: str = DefaultStr("gdsfactory.com")
    subdomain: str = DefaultStr("plus")
    nickname: str = DefaultStr("main")
    host: str = DefaultStr("main.plus.gdsfactory.com")
    license_url: str = urljoin(GFP_LANDING_PAGE_BASE_URL, "/api/verify-api-key")
    key: Literal[""] = ""  # this setting cannot be allowed to be set in pyproject.toml

    def full_license_url(self):
        if not self.key:
            message = (
                "Missing 'GFP_API_KEY'. Ensure GDSFactory+ is properly configured with "
                "a valid license. "
                "If you don't have a key, please contact us at contact@gdsfactory.com"
            )
            logger.error(message)
            raise ValueError(message)
        return f"{self.license_url}?api_key={self.key}"

    @field_validator("key", mode="before")
    def validate_key(key):
        return ""

    @model_validator(mode="after")
    def validate_api(self):
        self._validate_api()
        self._set_attributes_as_defaults()
        self.domain = _any_env_var_like("GFP_API_DOMAIN", "GFP_DOMAIN", "DOCODE_DOMAIN") or self.domain
        self.subdomain = _any_env_var_like("GFP_API_SUBDOMAIN", "GFP_SUBDOMAIN", "DOCODE_SUBDOMAIN") or self.subdomain
        self.nickname = _any_env_var_like("GFP_API_NICKNAME", "GFP_NICKNAME", "DOCODE_NICKNAME") or self.nickname
        self.license_url = (
            _any_env_var_like("GFP_LICENSE_URL", "GFP_LICENSE_ARN", "DOCODE_LICENSE_ARN") or self.license_url
        )
        if self.license_url != urljoin(GFP_LANDING_PAGE_BASE_URL, "/api/verify-api-key"):
            raise ValueError("Changing the license server URL is currently not supported.")

        self.host = _any_env_var_like("GFP_API_HOST", "GFP_HOST", "DOCODE_HOST") or self.host
        self._validate_api()
        self.key = _any_env_var_like("GFP_API_KEY", "DOCODE_API_KEY")  # type: ignore

        self.domain = str(self.domain)
        self.subdomain = str(self.subdomain)
        self.nickname = str(self.nickname)
        self.host = str(self.host)
        self.license_url = str(self.license_url)
        self.key = str(self.key)  # type: ignore
        return self

    def _validate_api(self):
        are_defaults = _are_defaults(self.domain, self.subdomain, self.nickname, self.host)
        if not any(are_defaults):
            host = f"{self.nickname}.{self.subdomain}.{self.domain}"
            if host != self.host:
                raise ValueError(
                    f"'api.host [{self.host}]' does not match "
                    "'{api.nickname}.{api.subdomain}.{api.domain}'. "
                    f"'{self.nickname}.{self.subdomain}.{self.domain}'. "
                    "Maybe only give api.host?"
                )
        elif are_defaults[-1]:
            self.host = f"{self.nickname}.{self.subdomain}.{self.domain}"
        elif are_defaults[:-1]:
            parts = self.host.split(".")
            self.nickname = parts[0]
            self.subdomain = parts[1]
            self.domain = ".".join(parts[2:])

    def _set_attributes_as_defaults(self):
        self.domain = DefaultStr(str(self.domain))
        self.subdomain = DefaultStr(str(self.subdomain))
        self.nickname = DefaultStr(str(self.nickname))
        self.host = DefaultStr(str(self.host))


class KwebSettings(BaseModel):
    host: str = DefaultStr("localhost")
    https: bool = False

    @model_validator(mode="after")
    def validate_sim(self):
        host = _any_env_var_like("GFP_KWEB_HOST", "KWEB_HOST", "DOWEB_HOST")
        https = _any_env_var_like("GFP_KWEB_HTTPS", "KWEB_HTTPS", "DOWEB_HTTPS")

        if host:
            self.host = host

        if https:
            self.https = _try_bool(https)

        self.host = str(self.host)
        self.https = bool(self.https)

        return self


class Linspace(BaseModel):
    min: float = 0.0
    max: float = 1.0
    num: int = 50

    @property
    def arr(self):
        return np.linspace(self.min, self.max, self.num)

    @property
    def step(self):
        return self.arr[1] - self.arr[0]


class Arange(BaseModel):
    min: float = 0.0
    max: float = 1.0
    step: float = 0.1

    @property
    def arr(self):
        return np.arange(self.min, self.max, self.step)

    @property
    def num(self):
        return self.arr.shape[0]


class SimSettings(BaseModel):
    host: str = DefaultStr("")
    wls: Linspace | Arange = Field(default_factory=lambda: Linspace(min=1.5, max=1.6, num=300))

    @model_validator(mode="after")
    def validate_sim(self):
        host = _any_env_var_like("GFP_SIM_HOST", "DOCODE_SIM_HOST", "SIM_HOST")

        if host:
            self.host = host

        # self.host = str(self.host)

        return self


class GptSettings(BaseModel):
    host: str = DefaultStr("")

    @model_validator(mode="after")
    def validate_gpt(self):
        host = _any_env_var_like("GFP_GPT_HOST", "DOCODE_GPT_HOST", "GPT_HOST")

        if host:
            self.host = host

        # self.host = str(self.host)

        return self


class Settings(BaseModel):
    name: str = DefaultStr("pics")
    pdk: PdkSettings = Field(default_factory=PdkSettings)
    api: ApiSettings = Field(default_factory=ApiSettings)
    drc: DrcSettings = Field(default_factory=DrcSettings)
    sim: SimSettings = Field(default_factory=SimSettings)
    gpt: GptSettings = Field(default_factory=GptSettings)
    kweb: KwebSettings = Field(default_factory=KwebSettings)
    debug: bool = False
    pyproject: str = DefaultStr("")

    @model_validator(mode="after")
    def validate_settings(self):
        name = _any_env_var_like("GFP_NAME")
        if name:
            self.name = name
        if _is_default(self.name):
            self.name = str(self.name)
        if _is_default(self.drc.host):
            self.drc.host = str(self.drc.host)
        if _is_default(self.sim.host):
            protocol = "https" if self.kweb.https else "http"
            self.sim.host = f"{protocol}://{self.kweb.host}"
        if _is_default(self.gpt.host):
            self.gpt.host = f"https://doitforme.{self.api.host}"
        if _is_default(self.drc.process):
            self.drc.process = str(self.drc.process)

        project_dir = maybe_find_docode_project_dir()
        if project_dir is not None:
            pyproject = os.path.join(project_dir, "pyproject.toml")
            if os.path.isfile(pyproject):
                self.pyproject = pyproject
            else:
                self.pyproject = ""
        else:
            self.pyproject = ""

        return self


def _is_default(item: str) -> bool:
    return isinstance(item, Default)


def _are_defaults(*items: str) -> tuple[bool, ...]:
    return tuple(_is_default(i) for i in items)


def _any_env_var_like(*vars: str, deprecate: bool = True) -> str:
    for i, key in enumerate(vars):
        if key in os.environ:
            if deprecate and i > 0:
                warnings.warn(
                    f"Environment variable {key} is deprecated. Use {vars[0]} instead.",
                    stacklevel=2,
                )
            return os.environ[key]
    return ""


def _try_int(s: str) -> int | None:
    try:
        return int(s)
    except Exception:
        return None


def _try_float(s: str) -> float | None:
    try:
        return float(s)
    except Exception:
        return None


def _try_bool(s: str | bool) -> bool:
    s = str(s).lower()
    if s == "true" or _try_int(s) or _try_float(s):
        return True
    return False


def _get_raw_docode_settings(path: str) -> dict[str, Any]:
    settings = toml.load(open(path))
    projectSettings = settings.get("project", {})
    name = projectSettings.get("name", "pics")
    toolSettings = settings.get("tool", {})
    settings: dict[str, Any] = {}
    if "gdsfactoryplus" in toolSettings:
        settings = toolSettings["gdsfactoryplus"]
    if "gfp" in toolSettings:
        settings = toolSettings["gfp"]
    if "dodesign" in toolSettings:
        settings = toolSettings["dodesign"]
    settings["name"] = name
    return settings


SETTINGS = load_settings()
