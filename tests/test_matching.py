import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.matching import name_match_pct


def test_no_name():
    assert name_match_pct(None, "Filtr") is None
    assert name_match_pct("  ", "Filtr") is None


def test_full_and_partial():
    # bez kodu: pelna zgodnosc nazwy = max 99
    assert name_match_pct("Filtr oleju oryginał Perkins", "Filtr oleju Perkins 2654407") == 99.0
    assert name_match_pct("filtr oleju silnika perkins", "Filtr oleju Perkins") == 75.0


def test_inflection_and_diacritics():
    assert name_match_pct("Filtr oleju", "Filtra olej") == 99.0
    assert name_match_pct("Podkładka stal", "podkladka stal 76") == 99.0


def test_code():
    assert name_match_pct("Filtr paliwa 4816636", "Filtr paliwa 4816636") == 99.0
    assert name_match_pct("Filtr paliwa 4816636", "Filtr paliwa 4816636", "4816636") == 100.0
    assert name_match_pct("Filtr paliwa 4816636", "Filtr paliwa 1111") == 66.7


def test_build_search_query():
    from src.core.matching import build_search_query
    assert build_search_query("Filtr oleju  oryginał Perkins") == "Filtr oleju Perkins"
    assert build_search_query("Podkładka Ø 76x135x0.5 mm  stal") == "Podkładka 76x135x0.5 mm stal"
    assert build_search_query(None) == ""


def test_code_in_title():
    from src.core.matching import code_in_title
    assert code_in_title("SW-378311", "Zbiornik SW378311 22000 l")
    assert code_in_title("SW-378311", "zbiornik sw 378311")
    assert code_in_title("SW-378311", "Zbiornik SW-378311")
    assert not code_in_title("4816636", "Filtr 48166361")
    assert not code_in_title("A1", "A1 filtr")
    assert not code_in_title("FILTR", "filtr oleju")


def test_code_tiers():
    # brak nazwy + kod = 90
    assert name_match_pct(None, "Filtr 2654407", "2654407") == 90.0
    # kod, zero slow z nazwy = 90
    assert name_match_pct("Filtr oleju Perkins", "Pompa 2654407", "2654407") == 90.0
    # kod + slowo z nazwy = 100
    assert name_match_pct("Filtr oleju Perkins", "Filtr 2654407", "2654407") == 100.0
    # sama nazwa bez kodu = max 99
    assert name_match_pct("Filtr oleju", "Filtr olej", "2654407") == 99.0
    assert name_match_pct("Filtr oleju perkins", "Filtr oleju", "2654407") == 66.7


def test_code_in_name_only_not_enough():
    # kod w nazwie, ale nie w tytule -> nie 100
    assert name_match_pct("Filtr 2654407", "Filtr 2654407x", "2654407") < 100.0
    # tylko kod pasuje (nazwa = filtr + kod, tytul ma sam kod) -> 90
    assert name_match_pct("Filtr 2654407", "Pompa 2654407", "2654407") == 90.0


def test_range_and_tiers():
    from src.core.matching import MATCH_TIERS

    for t, c in [("Filtr oleju", "Filtr oleju"), ("a b", "x")]:
        v = name_match_pct(t, c, "2654407")
        assert v is None or 0 <= v <= 100
    covered = set()
    for lo, hi, _ in MATCH_TIERS:
        covered.update(range(lo, hi + 1))
    assert covered == set(range(0, 101))
