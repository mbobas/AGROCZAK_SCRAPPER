import json
from pathlib import Path

import pytest

from src.core.results_io import (
    analyzer_summary_row,
    filter_offers,
    filter_products,
    flatten_offers,
)


def _offer(oid, price, buyers=None, title="Filtr paliwa"):
    return {
        "offer_id": oid,
        "price": price,
        "buyers_count": buyers,
        "title": title,
        "url": f"https://x/{oid}",
        "seller_name": "s",
    }


def _product(offers, ean="E1", my_price=100.0):
    return {
        "ean": ean,
        "name": "Filtr paliwa",
        "my_price": my_price,
        "search_mode": "name",
        "offers": offers,
    }


@pytest.fixture
def product():
    return _product(
        [
            _offer("a", 50, 5),  # -50%
            _offer("b", 100, None),  # 0%
            _offer("c", 105, 0),  # +5%
            _offer("d", 109, 3),  # +9%
            _offer("e", 150, 10),  # +50%
            _offer("f", 500, None),  # +400%
        ]
    )


def _markups(rows):
    return [r["Marża %"] for r in rows]


def test_markup_range_applies_to_offers(product):
    rows = flatten_offers([product], markup_min_pct=0, markup_max_pct=9)
    assert sorted(_markups(rows)) == [0.0, 5.0, 9.0]


def test_negative_and_above_100(product):
    rows = flatten_offers([product], markup_min_pct=-100, markup_max_pct=-1)
    assert _markups(rows) == [-50.0]
    rows = flatten_offers([product], markup_min_pct=101, markup_max_pct=None)
    assert _markups(rows) == [400.0]


def test_infinite_ends_return_everything(product):
    rows = flatten_offers([product], markup_min_pct=None, markup_max_pct=None)
    assert len(rows) == 6


def test_min_buyers_zero_keeps_none(product):
    assert len(filter_offers(product, min_buyers=0)) == 6
    assert len(filter_offers(product, min_buyers=None)) == 6


def test_min_buyers_one_drops_none_and_zero(product):
    ids = {o["offer_id"] for o in filter_offers(product, min_buyers=1)}
    assert ids == {"a", "d", "e"}


def test_summary_matches_flat_rows(product):
    kw = dict(markup_min_pct=0, markup_max_pct=9, min_buyers=None)
    row = analyzer_summary_row(product, **kw)
    flat = flatten_offers([product], **kw)
    assert row["Liczba ofert"] == len(flat) == 3
    assert row["Cena min"] == 100
    assert row["Cena max"] == 109
    assert row["Tytuł najtańszej"] == "Filtr paliwa"
    assert row["Kupujących max"] == 3
    assert row["Cena lidera"] == 109
    assert "Najtańsza oferta" not in row


def test_product_without_matching_offers_dropped(product):
    assert filter_products([product], markup_min_pct=900, markup_max_pct=None) == []
    assert filter_products([product], markup_min_pct=0, markup_max_pct=9) == [product]


def test_min_offers_counts_filtered_offers(product):
    assert filter_products([product], markup_min_pct=0, markup_max_pct=9, min_offers=3)
    assert not filter_products(
        [product], markup_min_pct=0, markup_max_pct=9, min_offers=4
    )


def test_regression_latest_results():
    out = Path("data/output")
    candidates = sorted(
        out.glob("results_*_szukanie_po_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        candidates = sorted(
            out.glob("results_*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
    if not candidates:
        pytest.skip("brak results_*.json w data/output")
    path = candidates[0]
    data = json.loads(path.read_text(encoding="utf-8"))
    products = data["products"] if isinstance(data, dict) else data
    rows = flatten_offers(products, markup_min_pct=0, markup_max_pct=9)
    for m in _markups(rows):
        assert m is not None and 0 <= m <= 9


def test_min_match_100_requires_code_and_name():
    p = _product(
        [
            _offer("a", 100, title="Filtr paliwa 2654407"),  # kod + nazwa -> 100
            _offer("b", 100, title="Pompa 2654407"),  # tylko kod -> 90
            _offer("c", 100, title="Filtr paliwa"),  # sama nazwa -> 99
        ],
        ean="2654407",
    )
    ids = {o["offer_id"] for o in filter_offers(p, min_match_pct=100)}
    assert ids == {"a"}
    ids = {o["offer_id"] for o in filter_offers(p, min_match_pct=90)}
    assert ids == {"a", "b", "c"}


ANALYZE_DEFAULTS = dict(
    markup_min_pct=None,
    markup_max_pct=None,
    min_buyers=1,
    min_match_pct=90.0,
)


def test_golden_2654407_leader_is_sold_code_match():
    p = _product(
        [
            _offer(
                "vasco",
                15.92,
                None,
                "DAVID VASCO V162 Filtr oleju",
            ),
            _offer(
                "donaldson",
                45.0,
                35,
                "Filtr oleju Donaldson P554407 Perkins 2654407",
            ),
            _offer(
                "pack2",
                191.97,
                29,
                "2× Filtr oleju Perkins 2654407 3/4 UNF 178mm",
            ),
        ],
        ean="2654407",
        my_price=86.0,
    )
    p["name"] = "Filtr oleju  oryginał Perkins"
    p["search_mode"] = "code"
    row = analyzer_summary_row(p, **ANALYZE_DEFAULTS)
    assert row["Kupujących max"] == 35
    assert row["Cena lidera"] == 45.0
    assert "2654407" in (row["Tytuł lidera"] or "")
    assert row["Cena min"] == 45.0
    assert row["Liczba ofert"] == 2
    assert row["Pasujące"] == 2


def test_golden_noise_dropped_without_code_or_buyers():
    es8t = _product(
        [
            _offer(
                "cap",
                6.49,
                1,
                "10× KONDENSATOR 680UF 10V Ø8x12mm 10% TNT JCCON",
            ),
        ],
        ean="ES8T",
        my_price=36.5,
    )
    es8t["name"] = "Szybkozłącze z końcówką na wąż 8 mm"
    es8t["search_mode"] = "code"
    assert filter_products([es8t], **ANALYZE_DEFAULTS) == []

    cable = _product(
        [
            _offer("febi", 5.2, None, "Febi Bilstein 14346 Śruba głowicy cylindrów"),
            _offer("ina", 217.32, 1, "Schaeffler INA 712 1503 10 Łożysko"),
        ],
        ean="1432045071",
        my_price=18.0,
    )
    cable["name"] = "Przewód elektryczny YLY-S 5 x 0.75 mm²"
    cable["search_mode"] = "code"
    assert filter_products([cable], **ANALYZE_DEFAULTS) == []


def test_matching_count_not_all_offers_with_defaults(product):
    row = analyzer_summary_row(product, **ANALYZE_DEFAULTS)
    assert row["Liczba ofert"] == 3
    assert row["Pasujące"] == 3
    assert row["Liczba ofert"] < len(product["offers"])
