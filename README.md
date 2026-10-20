# Allegro Price Monitor

Aplikacja do monitorowania cen i sprzedaży produktów na Allegro na podstawie kodów EAN.

## Funkcje

- Wyszukiwanie produktów po kodzie EAN
- Sprawdzanie cen na Allegro
- Informacja o sprzedaży ("X osób kupiło")
- Filtrowanie po marży cenowej (np. 12-15%)
- Analiza wyników: filtry (marża z końcami -∞/+∞, min. kupujących, dopasowanie nazwy) działają na poziomie ofert; min. kupujących = 0 przepuszcza oferty bez danych, od 1 je ukrywa
- Cache wyników (SQLite)
- Tryb konsolowy i GUI (Streamlit)
- Śledzenie zużycia kredytów scrape.do

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

3. (Opcjonalnie) Dostosuj `config.yaml`:

```yaml
price_threshold:
  min_markup: 0.12  # 12%
  max_markup: 0.15  # 15%

sales_threshold:
  min_buyers: 1     # minimum "X osób kupiło"

cache:
  ttl_days: 7       # ważność danych w dniach
```

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

Otworzy się przeglądarka z interfejsem na `http://localhost:8501`

## Format pliku wejściowego

Plik CSV z separatorem `;`:

```csv
ean;cena;nazwa
5902719471797;100.00;Lampa LED
5060512512509;50.00;Produkt 2
```

Obsługiwany jest też format `Kod produktu;nazwa;brutto` (nazwa opcjonalna).

Gdy podana jest nazwa, w analizie wyników liczone jest **dopasowanie %**: udział
znaczących słów z nazwy znalezionych w tytule oferty Allegro (np. 3 z 4 słów = 75%).
W zakładce „Analiza wyników” można filtrować suwakiem „Min. dopasowanie nazwy”.
Jeśli tytuł oferty zawiera cały kod produktu (np. `SW-378311` = `SW378311`; kod min. 5 znaków z cyfrą),
dopasowanie to automatycznie 100% (kolumna „Powód” = `kod`).
Liczone lokalnie, bez dodatkowych kredytów.

Kolumny:
- `Kod produktu` / `ean` / `EAN` / `kod` / `code` - kod produktu (wymagane)
- `brutto` - Twoja cena (alias `cena`)
- `cena` / `price` / `my_price` - Twoja cena (wymagane)
- `nazwa` / `name` - nazwa produktu (opcjonalne)

## Koszty scrape.do

| Tryb | Kredyty/zapytanie | Uwagi |
|------|-------------------|-------|
| `render=true` | 5 | Z JavaScript - pełne dane (włącz w sidebarze lub `--render` w CLI) |
| `render=false` | 1 | Bez JS - **domyślnie**, może brakować danych |

Darmowy plan: **1000 kredytów/miesiąc** = ~1000 produktów (render OFF) lub ~200 (render ON)

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
│   │   ├── processor.py   # Logika przetwarzania
│   │   └── cache.py       # Cache wyników (SQLite)
│   └── gui/
│       └── dashboard.py   # Interfejs Streamlit
├── data/
│   ├── input/             # Pliki wejściowe
│   └── output/            # Wyniki
└── tests/                 # Testy
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
