"""
Testy API i scrapera.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api.allegro import AllegroClient, AllegroAPIError, test_api_access
from src.api.scraper import ScrapeDoClient, test_scrape_do


def test_allegro_token():
    """Test pobierania tokena z Allegro."""
    print("Test: Pobieranie tokena Allegro...")
    try:
        client = AllegroClient()
        token = client.get_token()
        print(f"  OK: Token uzyskany, wazny {token.expires_in}s")
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def test_allegro_products():
    """Test wyszukiwania produktow (katalog)."""
    print("Test: Wyszukiwanie produktow w katalogu...")
    try:
        client = AllegroClient()
        result = client.search_products(ean="5902719471797")
        products = result.get("products", [])
        print(f"  OK: Znaleziono {len(products)} produktow")
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def test_allegro_offers():
    """Test wyszukiwania ofert publicznych."""
    print("Test: Wyszukiwanie ofert publicznych (/offers/listing)...")
    try:
        client = AllegroClient()
        result = client.search_offers(phrase="lampa LED")
        items = result.get("items", {})
        total = len(items.get("promoted", [])) + len(items.get("regular", []))
        print(f"  OK: Znaleziono {total} ofert")
        return True
    except AllegroAPIError as e:
        if e.status_code == 403:
            print(f"  EXPECTED FAIL: Brak dostepu (403) - aplikacja niezweryfikowana")
        else:
            print(f"  FAIL: {e}")
        return False
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def test_scrape_do_credits():
    """Test sprawdzania kredytow scrape.do."""
    print("Test: Sprawdzanie kredytow scrape.do...")
    try:
        client = ScrapeDoClient()
        info = client.get_credits_info()
        print(f"  OK: {info}")
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def run_all_tests():
    """Uruchamia wszystkie testy."""
    print("=" * 50)
    print("TESTY ALLEGRO PRICE MONITOR")
    print("=" * 50)
    
    results = []
    
    results.append(("Token Allegro", test_allegro_token()))
    results.append(("Katalog produktow", test_allegro_products()))
    results.append(("Oferty publiczne", test_allegro_offers()))
    results.append(("scrape.do kredyty", test_scrape_do_credits()))
    
    print("\n" + "=" * 50)
    print("PODSUMOWANIE")
    print("=" * 50)
    
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {name}: {status}")
    
    passed_count = sum(1 for _, p in results if p)
    print(f"\nWynik: {passed_count}/{len(results)} testow przeszlo")


if __name__ == "__main__":
    run_all_tests()
