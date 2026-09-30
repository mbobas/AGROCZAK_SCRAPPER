"""Test parsera listingu na zapisanym HTML."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.api.scraper import parse_allegro_search_html
from src.core.request_log import log_request, logs_dir


def test_parse_existing_html():
    html_path = Path("data/output/test_scrape_render.html")
    assert html_path.exists()
    html = html_path.read_text(encoding="utf-8")
    offers = parse_allegro_search_html(html)
    meta = parse_allegro_search_html.last_meta
    assert len(offers) > 0, f"expected offers, meta={meta}"
    assert offers[0].title
    assert offers[0].price > 0
    assert meta.get("parse_method") in ("raw_decode", "regex")


def test_request_log_writes_file(tmp_path, monkeypatch):
    import src.core.request_log as rl

    monkeypatch.setattr(rl, "LOG_ROOT", tmp_path / "logs")
    monkeypatch.setattr(rl, "REQUESTS_DIR", tmp_path / "logs" / "requests")
    monkeypatch.setattr(rl, "HTML_DIR", tmp_path / "logs" / "html")

    path = log_request(
        source="test",
        url="https://example.com",
        code="SW-378311",
        http_status=200,
        error=None,
        response_text="<html>ofert</html>",
        offers_parsed=0,
        offer_titles=[],
        save_html_on_empty=True,
    )
    assert path.exists()
    assert (tmp_path / "logs" / "html").exists()


if __name__ == "__main__":
    test_parse_existing_html()
    print("parse OK", len(parse_allegro_search_html(
        Path("data/output/test_scrape_render.html").read_text(encoding="utf-8")
    )), "offers")
    print("logs_dir", logs_dir())
