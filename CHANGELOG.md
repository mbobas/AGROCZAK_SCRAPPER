# Changelog

Format: datowane wpisy od najnowszych. Uzupełniamy przy kolejnych iteracjach.

## 2026-10-30

### Analiza (to, co idzie do CSV dla klienta)

- Domyślne filtry w zakładce **Analiza wyników**: min. **1 kupujący**, dopasowanie **≥ 90%** (kod w tytule), marża **bez limitu** (−∞…+∞). Scrap nadal zbiera szeroko; tniemy przy eksporcie.
- Podsumowanie: kolumny **Kupujących max**, **Cena lidera**, **Tytuł lidera** (oferta z największą liczbą kupujących po filtrach). `Najtańsza oferta` przemianowana na **Tytuł najtańszej** (to był tytuł, nie cena).
- Przyczyna zgłoszenia Piotra: CSV nie miał rozjechanych kolumn. Podsumowanie brało **najtańszą ofertę z całego listingu** (często bez kupujących / inny produkt). Przykład `2654407`: VASCO 15,92 zł vs Donaldson **45 zł / 35 kupujących**.
- Przeliczenie starego JSON 16k nowymi filtrami: 16 010 kodów → **3183** z sprzedażą i kodem; 207 k ofert → **7218**. Pliki: `data/output/verify_summary_selling.csv`, `verify_offers_selling.csv`.

### Scrapowanie / parser kupujących

- `config.yaml`: `min_buyers: 0` przy scrapie **zostaje** — JSON ma pełny listing.
- Parser listingu: oprócz `productPopularity.label` czyta `labelParts` / tooltip. Na próbce scrape.do **nie ma lepszego pola**. Etykieta to zwykle **„N osób kupiło ostatnio” produkt u wielu sprzedających (~30 dni)**, nie „kupiło tę ofertę”.
- `render=true` na listingu prawie nic nie dodaje (np. 33 vs 37 ofert z liczbą); nie włączamy domyślnie.
- Parser karty oferty (`parse_allegro_offer_html`): JSON-LD, cena, regex „kupiło tę ofertę”. Bez JS karta często zwraca **tę samą liczbę co listing**. Na żywej stronie bywa **druga** etykieta (np. UCP206: 83 produkt vs **30 tę ofertę**) — `render=false` jej nie zawsze widzi.

### Próbka 30 kodów (listing + max 20 kart ofert)

- Źródło „najgorszych”: match **100%** i **brak kupujących** we wszystkich takich ofertach (`oferty_200k.csv`), nie śmieć z match &lt; 50%.
- Skład: 10 worst (`GRAE40NPPB`, pasy SPB…) + 10 ze sprzedażą (`UCF207`, `UCP206`…) + 10 losowych (seed `20261030`).
- Pliki (zostają przy czyszczeniu cache):
  - `data/output/results_sample_30_szukanie_po_kodzie.json` — stan **przed** (do wczytania w Analizie)
  - `sample_30_before.json` — kopia
  - `sample_30_after_listing.json` — świeży listing
  - `sample_30_after_offers.json` — po kartach ofert
  - `sample_30_compare.csv` — stara vs nowa cena/kupujący
  - `sample_30_meta.json` — lista kodów
- ~30 listingów × 10 kr. + 20 kart × 10 kr. ≈ **500** kredytów.
- Wniosek z próby: **cena listing = cena karty**. Gdzie listing ma kupujących, karta bez JS pokazuje to samo. Puste na listingu często puste i na karcie.

### Cache

- **Nie czyścić** 16k przy diagnostyce. Klucze próbki można skasować osobno (`ProductCache.delete_keys`).
- Kopie: `data/cache.db.bak_20261030_1755` (sprzed odświeżenia 30), `data/cache.db.bak_20261030_2004` (pełny 16 811 z tymi 30).
- 2026-10-30 wieczór: roboczy `cache.db` **wyzerowany** (próba ręczna kilku kodów). Przywrócenie: skopiuj bak na `data/cache.db` przy wyłączonym scrapie.

### Testy / skrypty (nie CI)

- `tests/build_sample_30.py` — budowa próbki 30 z JSON 16k.
- `tests/rescrape_sample_30.py` — listing + `--offers-only`.
- `tests/diagnose_listing_buyers.py` — wcześniejsza próbka pól popularity (wyniki w `data/logs/diagnose/`, **nie** w liście Analizy).
- `tests/export_selling_filters.py` — CSV z filtrami rynkowymi na 16k.
- Unit: lider sprzedaży, golden `2654407` / `ES8T`, parser `labelParts`.

## Starsze (skrót, przed tą iteracją)

- Duże joby: worker poza Streamlit, cache chunkami, strumieniowy JSON — patrz `docs/LARGE_CACHE_JOB_LESSONS.md`.
- Dopasowanie: 100 = kod+słowo, 90 = sam kod, nazwa max 99.
- Analiza: filtry marży/kupujących na ofertach, nie tylko na produkcie.
