from pathlib import Path
import sys
import yaml

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from build import render_readme  # noqa: E402


def _load(name: str):
    with (REPO_ROOT / "tests" / "fixtures" / name).open() as f:
        return yaml.safe_load(f)


def test_render_readme_starts_with_h1():
    site = _load("minimal_site.yaml")
    showcase = _load("minimal_showcase.yaml")
    md = render_readme(site, showcase)
    first_line = md.strip().splitlines()[0]
    assert first_line.startswith("# ")


def test_render_readme_includes_name():
    site = _load("minimal_site.yaml")
    showcase = _load("minimal_showcase.yaml")
    md = render_readme(site, showcase)
    assert site["name"] in md


def test_render_readme_includes_oneliner_and_about():
    site = _load("minimal_site.yaml")
    showcase = _load("minimal_showcase.yaml")
    md = render_readme(site, showcase)
    assert site["hero_oneliner"] in md
    assert site["about"] in md


def test_render_readme_renders_section_headers():
    site = _load("minimal_site.yaml")
    showcase = _load("minimal_showcase.yaml")
    md = render_readme(site, showcase)
    assert "## Teaching" in md


def test_render_readme_links_to_landing_page():
    site = _load("minimal_site.yaml")
    showcase = _load("minimal_showcase.yaml")
    md = render_readme(site, showcase)
    assert "mahmood726-cyber.github.io" in md


def test_render_readme_renders_card_titles_as_links():
    site = _load("minimal_site.yaml")
    showcase = _load("minimal_showcase.yaml")
    md = render_readme(site, showcase)
    for card in showcase["cards"]:
        marker_a = f"[**{card['title']}**]({card['demo_url']})"
        marker_b = f"[{card['title']}]({card['demo_url']})"
        assert marker_a in md or marker_b in md


def test_render_readme_robust_to_missing_footer():
    site = _load("minimal_site.yaml")
    showcase = _load("minimal_showcase.yaml")
    md = render_readme(site, showcase)
    assert isinstance(md, str)
    assert len(md) > 50
