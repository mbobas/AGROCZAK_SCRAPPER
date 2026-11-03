# Allegro Price Monitor

Aplikacja do monitorowania cen i sprzedaży produktów na Allegro na podstawie kodów EAN.

Historia zmian: [CHANGELOG.md](CHANGELOG.md).

## Funkcje

- Wyszukiwanie po kodzie produktu lub nazwie (scrape.do → listing Allegro)
- Cena oferty z listingu; sprzedaż z etykiety **„N osób kupiło ostatnio”** (popularność **produktu**, ~30 dni, wielu sprzedawców — nie zawsze „kupiło tę ofertę”)
- JSON ze scrapu = **pełny listing**. Cięcie pod klienta jest w **Analizie wyników** (lokalnie, 0 kredytów)
- Dopasowanie: **100%** = kod w tytule + słowo z nazwy; **90%** = sam kod; sama nazwa max **99%**
- Analiza (domyślnie od 2026-10-30): min. **1 kupujący**, dopasowanie **≥ 90%**, marża **bez limitu**. Kolumny **Cena lidera / Kupujących max / Tytuł lidera** vs **Cena min / Tytuł najtańszej**
- Cache SQLite (`data/cache.db`); GUI Streamlit + CLI; zużycie kredytów scrape.do

## Wymagania

- Python 3.10+
- Konto scrape.do (darmowe: 1000 kredytów/miesiąc)
- Opcjonalnie: credentiale Allegro API

## Instalacja

### Windows

```powershell
# Utwórz wirtualne środowisko
python -m venv .venv

# Aktywuj środowisko
.\.venv\Scripts\Activate.ps1

# Zainstaluj zależności
pip install -r requirements.txt
```

### Linux / macOS

```bash
# Utwórz wirtualne środowisko
python3 -m venv .venv

# Aktywuj środowisko
source .venv/bin/activate

# Zainstaluj zależności
pip install -r requirements.txt
```

## Konfiguracja

1. Skopiuj `.env.example` do `.env`:

```bash
cp .env.example .env
```

2. Uzupełnij token scrape.do w pliku `.env`:

```env
SCRAPE_DO_TOKEN=twoj_token_z_scrape_do
```

3. (Opcjonalnie) Dostosuj `config.yaml`. Progi przy **scrapie** zbierają szeroko (`min_buyers: 0`, marża 0–50% tylko do `matching_offers` w JSON). **Filtry dla Piotra ustawiaj w Analizie**, nie tu.

## Użycie

### Tryb konsolowy

```bash
# Test połączenia
python src/main.py test

# Sprawdź produkty z pliku CSV
python src/main.py run -i data/input/produkty.csv -s scrape_do

# Zarządzanie cache
python src/main.py cache stats
python src/main.py cache clear-expired
```

### Tryb GUI (Streamlit)

```bash
streamlit run src/gui/dashboard.py
```

Otworzy się przeglądarka z interfejsem na `http://localhost:8501`.

**Scrapowanie** — sidebar (marża, min. kupujących) dotyczy **kolejnego joba**, nie tabeli Analizy.

**Analiza wyników** — wczytaj `results_*.json` z `data/output` (albo Upload). Domyślne filtry: kupujący ≥ 1, match ≥ 90%, marża −∞…+∞. CSV podsumowania i ofert spłaszczonych idzie z tych filtrów.

Nie mylić z diagnostyką: `data/logs/diagnose/` **nie** pojawia się na liście Analizy.

Próbka 30 kodów (przed/po scrapie, do ręcznego porównania): `data/output/results_sample_30_szukanie_po_kodzie.json`, `sample_30_after_listing.json`, `sample_30_compare.csv`. Szczegóły w changelogu.

## Deploy (Streamlit Cloud)

> **WAŻNE — widoczność repozytorium**  
> Żeby Streamlit Cloud **odświeżył się po pushu** i wciągnął nowe zmiany, repozytorium GitHub **musi być publiczne** w momencie deployu / redeployu.  
> Po udanym wdrożeniu możesz (i tak należy) **z powrotem ustawić repo na private**.  
> Typowy rytuał: `public` → push / Redeploy w Streamlit → sprawdź, że działa → `private`.

Bez publicznego repo Streamlit często **nie widzi** nowych commitów i zostaje na starej wersji aplikacji.

## Format pliku wejściowego

Plik CSV z separatorem `;`:

```csv
ean;cena;nazwa
5902719471797;100.00;Lampa LED
5060512512509;50.00;Produkt 2
```

Obsługiwany jest też format `Kod produktu;nazwa;brutto` (nazwa opcjonalna).

Gdy jest nazwa, **dopasowanie %** = udział znaczących słów z nazwy w tytule oferty.
Kod w tytule (np. `SW-378311` = `SW378311`, min. 5 znaków z cyfrą) + słowo z nazwy → 100% (`kod+nazwa`); sam kod → 90% (`tylko kod`).
Liczone lokalnie, bez kredytów.

Kolumny:
- `Kod produktu` / `ean` / `EAN` / `kod` / `code` - kod produktu (wymagane)
- `brutto` - Twoja cena (alias `cena`)
- `cena` / `price` / `my_price` - Twoja cena (wymagane)
- `nazwa` / `name` - nazwa produktu (opcjonalne)

## Koszty scrape.do (Allegro)

Dla Allegro w praktyce obowiązuje stawka jak **residential (`super`)**, nawet przy `render=false`
(potwierdzone Usage History + [Request Costs](https://scrape.do/documentation/request-costs/)).
Wiążący jest header `Scrape.do-Request-Cost`.

| Tryb | Kredyty/zapytanie | Uwagi |
|------|-------------------|-------|
| `render=false` (domyślnie) | **~10** | Jak residential — najtańszy sensowny tryb na Allegro |
| `render=true` | **~25** | Residential + headless — pełniejszy listing |

Aplikacja scrapuje **równolegle** do limitu **Concurrent Requests** z planu
(np. Hobby = **10**). Cache: bulk odczyt, bez delay — ponowne kody w TTL ≈ 0 kred.

Szacunek: 16 000 kodów × 10 ≈ **160 000** kredytów (pierwszy przebieg, render OFF).
Pełne ponowne scrapowanie 16k na koncie ~1000 kr. **nie ma sensu** — filtruj istniejący JSON w Analizie.

Karta pojedynczej oferty (`/oferta/{id}`) to kolejne ~10 kr. i ma sens tylko przy match 100%, z limitem (patrz próbka 30 w changelogu).

### Cache

- Plik: `data/cache.db`. Przycisk „Wyczyść cache” w GUI kasuje **wszystko**.
- Kopie (przywrócenie = skopiuj bak na `cache.db` przy wyłączonym scrapie):
  - `data/cache.db.bak_20261030_1755`
  - `data/cache.db.bak_20261030_2004` (16 811, z odświeżoną trzydziestką)
- Hit w TTL = 0 kredytów; po `cache clear` te same kody idą znów na scrape.do.

### Tryb wyszukiwania (Kod / Nazwa)

W zakładce Scrapowanie przełącznik „Szukaj po” wybiera, czy fraza do Allegro to kod
produktu, czy nazwa z kolumny `nazwa`. Cache osobno dla obu trybów; kolumna „Tryb”
w wynikach pokazuje, jak szukano.

## Struktura projektu

```
AGROCZAK_SCRAPPER/
├── .env                    # Credentiale (nie commituj!)
├── .env.example            # Szablon credentiali
├── config.yaml             # Konfiguracja aplikacji
├── requirements.txt        # Zależności Python
├── src/
│   ├── main.py            # Punkt wejścia CLI
│   ├── api/
│   │   ├── allegro.py     # Klient API Allegro
│   │   └── scraper.py     # scrape.do + parser HTML
│   ├── core/
│   │   ├── processor.py   # Job scrapu
│   │   ├── results_io.py  # Filtry Analizy, CSV, lider sprzedaży
│   │   ├── matching.py    # Dopasowanie kod/nazwa
│   │   └── cache.py       # SQLite
│   └── gui/
│       └── dashboard.py
├── data/
│   ├── cache.db           # Cache (nie commituj bak-ów z danymi klienta jeśli nie trzeba)
│   ├── output/            # results_*.json, próbka 30, verify_*.csv
│   └── logs/diagnose/     # HTML/JSON diagnostyki (nie lista Analizy)
├── CHANGELOG.md
└── tests/                 # m.in. build_sample_30, rescrape_sample_30
```

## Rozwiązywanie problemów

### Windows: Błąd SSL
```
SSLError: certificate verify failed
```
Aplikacja automatycznie pomija weryfikację SSL dla scrape.do na Windows.

### Brak kredytów scrape.do
```
401: You have no credits
```
Sprawdź stan konta na https://scrape.do/dashboard

### API Allegro zwraca 403
Endpoint `/offers/listing` wymaga weryfikacji aplikacji, która jest obecnie wstrzymana przez Allegro. Użyj trybu `scrape_do`.

## Licencja

Prywatne użycie.
