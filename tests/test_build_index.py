from pathlib import Path
import sys
import yaml

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from build import render_index  # noqa: E402


def _load(name: str):
    with (REPO_ROOT / "tests" / "fixtures" / name).open() as f:
        return yaml.safe_load(f)


def test_render_index_contains_hero_oneliner():
    site = _load("minimal_site.yaml")
    showcase = _load("minimal_showcase.yaml")
    html = render_index(site, showcase)
    assert "A one-line mission for testing." in html


def test_render_index_contains_byline_lines():
    site = _load("minimal_site.yaml")
    showcase = _load("minimal_showcase.yaml")
    html = render_index(site, showcase)
    assert "Test Institution" in html


def test_render_index_renders_section_headers():
    site = _load("minimal_site.yaml")
    showcase = _load("minimal_showcase.yaml")
    html = render_index(site, showcase)
    assert "Teaching" in html
    assert "Atlases" in html


def test_render_index_renders_each_card_title():
    site = _load("minimal_site.yaml")
    showcase = _load("minimal_showcase.yaml")
    html = render_index(site, showcase)
    for card in showcase["cards"]:
        assert card["title"] in html


def test_render_index_renders_status_badge():
    site = _load("minimal_site.yaml")
    showcase = _load("minimal_showcase.yaml")
    html = render_index(site, showcase)
    assert "live" in html.lower()
    assert "preprint" in html.lower()


def test_render_index_renders_africa_thread_badge():
    site = _load("minimal_site.yaml")
    showcase = _load("minimal_showcase.yaml")
    html = render_index(site, showcase)
    assert "africa" in html.lower()


def test_render_index_links_to_all():
    site = _load("minimal_site.yaml")
    showcase = _load("minimal_showcase.yaml")
    html = render_index(site, showcase)
    assert "all/" in html


def test_render_index_no_marketing_words():
    site = _load("minimal_site.yaml")
    showcase = _load("minimal_showcase.yaml")
    html = render_index(site, showcase)
    banned = ["Quantum", "Grand Unified", "Comprehensive Global"]
    for word in banned:
        assert word not in html
