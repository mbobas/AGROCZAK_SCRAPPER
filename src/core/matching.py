"""
Dopasowanie nazwy produktu (z pliku zrodlowego) do tytulu oferty Allegro.
Wynik = udzial znaczacych slow z naszej nazwy znalezionych w tytule oferty (0-100).
"""
from __future__ import annotations

import re
import unicodedata
from typing import List, Optional

STOP_WORDS = {
    "do", "i", "z", "na", "w", "o", "od", "po", "dla", "ze", "oraz", "lub", "a",
    "oryginal", "oryginalny", "zamiennik", "nowy", "nowa", "szt", "mm",
}

_PL_MAP = str.maketrans({"ł": "l", "Ł": "l", "ø": "o", "Ø": "o"})
MIN_PREFIX = 5

CODE_AND_NAME_PCT = 100.0  # kod w tytule + slowo z nazwy
CODE_ONLY_PCT = 90.0  # kod w tytule, bez slow z nazwy
NAME_ONLY_MAX_PCT = 99.0  # sama nazwa, bez kodu

# (od %, do %, opis) - od najwyzszego; zrodlo legendy w UI
MATCH_TIERS = [
    (100, 100, "kod w tytule + słowo z nazwy"),
    (90, 90, "kod w tytule, bez słów z nazwy"),
    (75, 99, "większość słów z nazwy (bez kodu max 99)"),
    (50, 74, "połowa słów — do ręcznego sprawdzenia"),
    (0, 49, "słabe dopasowanie, prawdopodobnie inny produkt"),
]


def match_legend_text() -> str:
    return " · ".join(
        (f"**{lo}%**" if lo == hi else f"**{lo}–{hi}%**") + f" {desc}"
        for lo, hi, desc in MATCH_TIERS
    )


def normalize(text: str) -> str:
    text = (text or "").translate(_PL_MAP)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text.lower()


def tokenize(text: str) -> List[str]:
    return [t for t in re.split(r"[^a-z0-9\-/\.]+", normalize(text)) if t]


def _clean(token: str) -> str:
    return token.strip("-/.")


def _code_key(token: str) -> str:
    return re.sub(r"[^a-z0-9]", "", token)


def name_tokens(name: str) -> List[str]:
    out: List[str] = []
    for t in tokenize(name):
        t = _clean(t)
        if len(t) < 2 or t in STOP_WORDS:
            continue
        out.append(t)
    return out


def _token_matches(token: str, title_tokens: List[str], title_codes: set) -> bool:
    if any(c.isdigit() for c in token):
        key = _code_key(token)
        return bool(key) and (key in title_codes)
    for tt in title_tokens:
        if tt == token:
            return True
        if any(c.isdigit() for c in tt):
            continue
        common = 0
        for a, b in zip(tt, token):
            if a != b:
                break
            common += 1
        need = max(MIN_PREFIX, int(0.8 * min(len(tt), len(token)) + 0.999))
        if min(len(tt), len(token)) < MIN_PREFIX:
            need = min(len(tt), len(token))
            if len(tt) != len(token) and need < 4:
                continue
        if common >= need:
            return True
    return False


def name_match_pct(
    my_name: Optional[str], offer_title: Optional[str], code: Optional[str] = None
) -> Optional[float]:
    """
    Dopasowanie nazwy/kodu do tytulu oferty (0-100):
      - kod w tytule + >= 1 slowo z nazwy (poza samym kodem): 100
      - kod w tytule, bez slow z nazwy / brak nazwy: 90
      - bez kodu w tytule: procent slow z nazwy, max 99
      - brak nazwy i kodu w tytule: None
    """
    has_code = code_in_title(code, offer_title)
    tokens = name_tokens(str(my_name)) if my_name and str(my_name).strip() else []
    if not tokens:
        return CODE_ONLY_PCT if has_code else None

    title_tokens = [_clean(t) for t in tokenize(offer_title or "")]
    title_tokens = [t for t in title_tokens if t]
    title_codes = {_code_key(t) for t in title_tokens}
    code_key = _code_key(normalize(str(code or "")))
    hits = 0
    word_hits = 0  # trafienia bez samego kodu produktu
    for t in tokens:
        if _token_matches(t, title_tokens, title_codes):
            hits += 1
            if not (code_key and _code_key(t) == code_key):
                word_hits += 1
    if has_code:
        return CODE_AND_NAME_PCT if word_hits > 0 else CODE_ONLY_PCT
    pct = round(hits / len(tokens) * 100, 1)
    return max(0.0, min(NAME_ONLY_MAX_PCT, pct))


_NOISE = {"oryginal", "oryginalny", "zamiennik", "szt"}


def build_search_query(name: Optional[str]) -> str:
    """Fraza do wyszukiwarki Allegro: nazwa bez szumu (oryginal, zamiennik, symbole)."""
    if not name:
        return ""
    raw = re.sub(r"[Øø()\[\],;:]", " ", str(name))
    words = [w for w in raw.split() if normalize(w).strip("-/.") not in _NOISE]
    return " ".join(words).strip()


def code_in_title(code: Optional[str], title: Optional[str]) -> bool:
    """True gdy caly kod produktu wystepuje w tytule (SW-378311 == SW378311 == sw 378311)."""
    key = _code_key(normalize(str(code or "")))
    if len(key) < 5 or not any(c.isdigit() for c in key):
        return False
    parts = [p for p in re.split(r"[^a-z0-9]+", normalize(title or "")) if p]
    for i in range(len(parts)):
        joined = ""
        for p in parts[i:]:
            joined += p
            if joined == key:
                return True
            if len(joined) >= len(key):
                break
    return False
