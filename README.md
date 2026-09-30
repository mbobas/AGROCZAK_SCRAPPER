# Allegro Price Monitor

Aplikacja do monitorowania cen i sprzedaży produktów na Allegro.

## Wymagania

- Python 3.10+
- Credentiale Allegro API (client_id, client_secret)
- Opcjonalnie: token scrape.do

## Instalacja

```bash
pip install -r requirements.txt
```

## Konfiguracja

1. Skopiuj `.env.example` do `.env` i uzupełnij credentiale:

```env
ALLEGRO_CLIENT_ID=twoj_client_id
ALLEGRO_CLIENT_SECRET=twoj_client_secret
SCRAPE_DO_TOKEN=twoj_token  # opcjonalnie
```

2. Dostosuj `config.yaml` według potrzeb.

## Użycie

### Tryb konsolowy

```bash
# Uruchom testy połączenia
python src/main.py test

# Sprawdź produkty z pliku CSV
python src/main.py run -i data/input/produkty.csv -o wyniki.json

# Zarządzanie cache
python src/main.py cache stats
python src/main.py cache clear-expired
```

### Tryb GUI (Streamlit)

```bash
streamlit run src/gui/dashboard.py
```

## Format pliku wejściowego

CSV z separatorem `;`:

```csv
ean;cena;nazwa
5902719471797;100.00;Lampa LED
5060512512509;50.00;Produkt 2
```

## Struktura projektu

```
AGROCZAK_SCRAPPER/
├── .env                    # Credentiale (nie commituj!)
├── config.yaml             # Konfiguracja aplikacji
├── requirements.txt        # Zależności Python
├── src/
│   ├── main.py            # Punkt wejścia CLI
│   ├── api/
│   │   ├── allegro.py     # Klient API Allegro
│   │   └── scraper.py     # Scraper (scrape.do)
│   ├── core/
│   │   ├── processor.py   # Logika przetwarzania
│   │   └── cache.py       # Cache wyników (SQLite)
│   └── gui/
│       └── dashboard.py   # Interfejs Streamlit
├── data/
│   ├── input/             # Pliki wejściowe
│   └── output/            # Wyniki
└── tests/
    └── test_api.py        # Testy
```

## Uwagi

- **API Allegro `/offers/listing`**: Endpoint do wyszukiwania publicznych ofert jest dostępny tylko dla zweryfikowanych aplikacji. Jeśli otrzymujesz błąd 403, użyj trybu scrape.do.
- **Rate limiting**: Domyślnie 10 zapytań na minutę (6s opóźnienia). Dostosuj w `config.yaml`.
- **Cache**: Wyniki są cache'owane w SQLite (domyślnie 7 dni ważności).
