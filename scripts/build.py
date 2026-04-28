"""Build script: render index.html and README.md from data/site.yaml + data/showcase.yaml."""
from __future__ import annotations
import argparse
import datetime
import json
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from jsonschema import validate, ValidationError
import yaml

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


def render_readme(site: dict, showcase: dict) -> str:
    env = _env()
    env.autoescape = False
    template = env.get_template("README.md.j2")
    return template.render(site=site, showcase=showcase)


def _load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _validate(data: dict, schema_name: str) -> None:
    schema_path = REPO_ROOT / "schemas" / f"{schema_name}.schema.json"
    with schema_path.open(encoding="utf-8") as f:
        schema = json.load(f)
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        sys.stderr.write(f"schema validation failed for {schema_name}: {e.message}\n")
        sys.exit(2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render index.html + README.md from YAML data.")
    parser.add_argument("--site", required=True, type=Path)
    parser.add_argument("--showcase", required=True, type=Path)
    parser.add_argument("--out-html", required=True, type=Path)
    parser.add_argument("--out-readme", required=True, type=Path)
    args = parser.parse_args()

    site = _load_yaml(args.site)
    showcase = _load_yaml(args.showcase)
    _validate(site, "site")
    _validate(showcase, "showcase")

    args.out_html.parent.mkdir(parents=True, exist_ok=True)
    args.out_readme.parent.mkdir(parents=True, exist_ok=True)

    args.out_html.write_text(render_index(site, showcase), encoding="utf-8")
    args.out_readme.write_text(render_readme(site, showcase), encoding="utf-8")

    print(f"wrote {args.out_html}")
    print(f"wrote {args.out_readme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
