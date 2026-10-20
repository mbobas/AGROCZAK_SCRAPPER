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
