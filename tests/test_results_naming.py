"""Nazwy plików wyników wg trybu szukania."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.results_io import (
    infer_search_mode,
    save_results_json,
    search_mode_suffix,
)


def test_search_mode_suffix():
    assert search_mode_suffix("code") == "_szukanie_po_kodzie"
    assert search_mode_suffix("name") == "_szukanie_po_nazwie"
    assert search_mode_suffix("Nazwa") == "_szukanie_po_nazwie"
    assert search_mode_suffix(None) == "_szukanie_po_kodzie"
    assert search_mode_suffix("other") == "_szukanie_po_kodzie"


def test_infer_search_mode():
    assert infer_search_mode([]) == "code"
    assert infer_search_mode([{"ean": "1"}]) == "code"
    assert infer_search_mode([{"search_mode": "name"}]) == "name"
    assert infer_search_mode(
        [{"search_mode": "code"}, {"search_mode": "name"}]
    ) == "code"


def test_save_results_json_filename(tmp_path, monkeypatch):
    import src.core.results_io as rio

    monkeypatch.setattr(rio, "OUTPUT_DIR", tmp_path)
    products = [{"ean": "1", "search_mode": "name", "offers": []}]
    path = save_results_json(products)
    assert path.parent == tmp_path
    assert path.name.startswith("results_")
    assert path.name.endswith("_szukanie_po_nazwie.json")

    path2 = save_results_json(products, search_mode="code")
    assert path2.name.endswith("_szukanie_po_kodzie.json")
