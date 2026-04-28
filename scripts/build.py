"""Build script: render index.html and README.md from data/site.yaml + data/showcase.yaml."""
from __future__ import annotations
import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

REPO_ROOT = Path(__file__).parent.parent


def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(REPO_ROOT / "templates"),
        autoescape=select_autoescape(["html", "j2"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render_index(site: dict, showcase: dict, build_timestamp: str | None = None) -> str:
    env = _env()
    template = env.get_template("index.html.j2")
    ts = build_timestamp or datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")
    return template.render(site=site, showcase=showcase, build_timestamp=ts)
