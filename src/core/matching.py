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


def name_match_pct(my_name: Optional[str], offer_title: Optional[str]) -> Optional[float]:
    """Procent slow z my_name znalezionych w offer_title. None gdy brak nazwy."""
    if not my_name or not str(my_name).strip():
        return None
    tokens = name_tokens(str(my_name))
    if not tokens:
        return None
    title_tokens = [_clean(t) for t in tokenize(offer_title or "")]
    title_tokens = [t for t in title_tokens if t]
    title_codes = {_code_key(t) for t in title_tokens}
    hits = sum(1 for t in tokens if _token_matches(t, title_tokens, title_codes))
    return round(hits / len(tokens) * 100, 1)
