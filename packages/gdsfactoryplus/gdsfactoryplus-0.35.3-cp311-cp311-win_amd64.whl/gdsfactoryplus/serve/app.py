import os
from typing import cast

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ..settings import SETTINGS as s
from ..settings import maybe_find_docode_project_dir

try:
    from doweb.browser import get_app  # type: ignore
    from doweb.layout_server import LayoutViewServerEndpoint

    LayoutViewServerEndpoint.mode_dump = lambda self: ("ruler",)  # type: ignore
except ImportError:
    from kweb.browser import get_app  # type: ignore

PDK: str = s.pdk.name
PROJECT_DIR: str = maybe_find_docode_project_dir() or os.getcwd()

app = cast(FastAPI, get_app(fileslocation=PROJECT_DIR, editable=True))
assert isinstance(app, FastAPI)


def needs_to_be_removed(path: str) -> bool:
    if path == "/":
        return True
    elif path.startswith("/file"):
        return True
    elif path.startswith("/gds"):
        return True
    return False


app.router.routes = [r for r in app.routes if not needs_to_be_removed(r.path)]  # type: ignore

this_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(this_dir, "static")
app.mount("/static2", StaticFiles(directory=static_dir), name="static2")
templates = Jinja2Templates(directory=os.path.join(this_dir, "templates"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
