import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.matching import name_match_pct


def test_no_name():
    assert name_match_pct(None, "Filtr") is None
    assert name_match_pct("  ", "Filtr") is None


def test_full_and_partial():
    assert name_match_pct("Filtr oleju oryginał Perkins", "Filtr oleju Perkins 2654407") == 100.0
    assert name_match_pct("filtr oleju silnika perkins", "Filtr oleju Perkins") == 75.0


def test_inflection_and_diacritics():
    assert name_match_pct("Filtr oleju", "Filtra olej") == 100.0
    assert name_match_pct("Podkładka stal", "podkladka stal 76") == 100.0


def test_code():
    assert name_match_pct("Filtr paliwa 4816636", "Filtr paliwa 4816636") == 100.0
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


def test_code_gives_100():
    assert name_match_pct(None, "Filtr 2654407", "2654407") == 100.0
    assert name_match_pct("Filtr oleju Perkins", "Pompa 2654407", "2654407") == 100.0
    assert name_match_pct("Filtr oleju", "Filtr olej", "2654407") == 100.0
    assert name_match_pct("Filtr oleju perkins", "Filtr oleju", "2654407") == 66.7
