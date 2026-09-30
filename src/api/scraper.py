"""
Scraper do Allegro - scrape.do lub wlasny scraper.
"""
import os
import re
import json
from dataclasses import dataclass
from typing import Optional, List
from urllib.parse import quote_plus
import requests
from dotenv import load_dotenv

load_dotenv()


@dataclass
class OfferData:
    offer_id: str
    title: str
    price: float
    currency: str
    seller_name: str
    buyers_count: Optional[int]  # "X osob kupilo te oferte"
    url: str
    is_smart: bool = False
    delivery_price: Optional[float] = None


class ScraperError(Exception):
    pass


class ScrapeDoClient:
    """Klient do scrape.do API."""
    
    BASE_URL = "https://api.scrape.do"
    
    def __init__(self, token: Optional[str] = None, verify_ssl: bool = True):
        self.token = token or os.getenv("SCRAPE_DO_TOKEN")
        self.verify_ssl = verify_ssl
        if not self.token:
            raise ValueError("SCRAPE_DO_TOKEN musi byc ustawiony")
    
    def scrape(self, url: str, render: bool = True) -> str:
        """
        Scrapuje strone przez scrape.do.
        render=True uzywaj dla stron z JavaScript (kosztuje wiecej kredytow).
        """
        params = {
            "token": self.token,
            "url": url,
            "render": str(render).lower(),
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=60, verify=self.verify_ssl)
        except requests.exceptions.SSLError:
            # Retry bez weryfikacji SSL (Windows issue)
            response = requests.get(self.BASE_URL, params=params, timeout=60, verify=False)
        
        if response.status_code != 200:
            raise ScraperError(f"scrape.do zwrocil {response.status_code}: {response.text[:200]}")
        
        return response.text
    
    def get_credits_info(self) -> dict:
        """Sprawdza ile kredytow zostalo."""
        url = f"{self.BASE_URL}/info?token={self.token}"
        try:
            response = requests.get(url, timeout=10, verify=self.verify_ssl)
        except requests.exceptions.SSLError:
            response = requests.get(url, timeout=10, verify=False)
        if response.status_code == 200:
            return response.json()
        return {"error": f"Status {response.status_code}"}


def parse_allegro_search_html(html: str) -> List[OfferData]:
    """
    Parsuje HTML strony wynikow wyszukiwania Allegro.
    Wyciaga dane z JSON w skrypcie lub z artykulow HTML.
    """
    offers = []
    
    # Metoda 1: Wyciagnij dane z JSON w skrypcie (najlepsza metoda)
    json_match = re.search(r'"items":\s*\{"elements":\s*\[(.*?)\]\s*\}', html, re.DOTALL)
    if json_match:
        try:
            # Znajdz caly obiekt __listing_StoreState
            store_match = re.search(r'\{"__listing_StoreState":(.*?)\}\s*</script>', html, re.DOTALL)
            if store_match:
                import json
                try:
                    store_data = json.loads('{"__listing_StoreState":' + store_match.group(1) + '}')
                    items = store_data.get('__listing_StoreState', {}).get('items', {}).get('elements', [])
                    
                    for item in items:
                        try:
                            # Wyciagnij dane
                            offer_id = item.get('offerId', '') or item.get('id', '')
                            title = item.get('alt', '') or item.get('title', {})
                            if isinstance(title, dict):
                                title = title.get('text', '')
                            
                            # Cena - moze byc w roznych miejscach
                            price_data = item.get('price', {})
                            price = 0.0
                            price_str = '0'
                            
                            if isinstance(price_data, dict):
                                # Nowy format: price.mainPrice.amount
                                main_price = price_data.get('mainPrice', {})
                                if isinstance(main_price, dict):
                                    price_str = main_price.get('amount', '0')
                                # Stary format: price.normal.amount lub price.amount
                                if price_str == '0':
                                    price_str = price_data.get('normal', {}).get('amount', '0')
                                if price_str == '0':
                                    price_str = price_data.get('amount', '0')
                            else:
                                price_str = str(price_data)
                            
                            try:
                                price = float(str(price_str).replace(',', '.').replace(' ', ''))
                            except (ValueError, TypeError):
                                pass
                            
                            # URL - konstruuj z offerId
                            offer_id_str = item.get('offerId', '') or item.get('id', '')
                            url = item.get('url', '')
                            # Jesli URL prowadzi do events/clicks, skonstruuj prawidlowy URL oferty
                            if not url or 'events/clicks' in url:
                                if offer_id_str:
                                    # Slug z tytulu
                                    slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower())[:50] if title else 'oferta'
                                    url = f'https://allegro.pl/oferta/{slug}-{offer_id_str}'
                            elif not url.startswith('http'):
                                url = 'https://allegro.pl' + url
                            
                            # Kupujacy - productPopularity lub popularity
                            buyers_count = None
                            popularity = item.get('productPopularity') or item.get('popularity', {})
                            if isinstance(popularity, dict):
                                label = popularity.get('label', '')
                                if label:
                                    # Wyciagnij liczbe z "183 osoby kupiły"
                                    num_match = re.search(r'(\d+)', str(label))
                                    if num_match:
                                        buyers_count = int(num_match.group(1))
                            
                            # Sprzedawca
                            seller = item.get('seller', {})
                            seller_name = seller.get('login', '') if isinstance(seller, dict) else None
                            
                            # Smart
                            delivery = item.get('delivery', {})
                            is_smart = delivery.get('smart', False) if isinstance(delivery, dict) else False
                            
                            if title and price > 0:
                                offers.append(OfferData(
                                    offer_id=str(offer_id),
                                    title=title,
                                    price=price,
                                    currency="PLN",
                                    seller_name=seller_name,
                                    buyers_count=buyers_count,
                                    url=url,
                                    is_smart=is_smart,
                                ))
                        except Exception:
                            continue
                            
                except json.JSONDecodeError:
                    pass
        except Exception:
            pass
    
    # Metoda 2: Fallback - parsuj artykuly HTML
    if not offers:
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            articles = soup.find_all('article')
            
            for article in articles:
                try:
                    text = article.get_text()
                    
                    # Tytul - pierwszy znaczacy tekst
                    title_parts = [t.strip() for t in text.split('\n') if len(t.strip()) > 20]
                    title = title_parts[0] if title_parts else None
                    
                    # Cena
                    price = 0.0
                    price_match = re.search(r'(\d+[,\.]\d{2})\s*zł', text)
                    if price_match:
                        price = float(price_match.group(1).replace(',', '.'))
                    
                    # Kupujacy
                    buyers_count = None
                    buyers_match = re.search(r'(\d+)\s*os[oó]b', text, re.IGNORECASE)
                    if buyers_match:
                        buyers_count = int(buyers_match.group(1))
                    
                    if title and price > 0:
                        offers.append(OfferData(
                            offer_id="",
                            title=title[:100],
                            price=price,
                            currency="PLN",
                            seller_name=None,
                            buyers_count=buyers_count,
                            url="",
                            is_smart='smart' in text.lower(),
                        ))
                except Exception:
                    continue
        except ImportError:
            pass
    
    return offers


def parse_allegro_offer_html(html: str) -> Optional[OfferData]:
    """
    Parsuje HTML strony pojedynczej oferty Allegro.
    Wyciaga: tytul, cene, sprzedawce, "X osob kupilo".
    """
    from html.parser import HTMLParser
    
    offer_data = {
        "offer_id": None,
        "title": None,
        "price": None,
        "currency": "PLN",
        "seller_name": None,
        "buyers_count": None,
        "url": None,
        "is_smart": False,
    }
    
    # Tytul - zwykle w <h1>
    title_match = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
    if title_match:
        offer_data["title"] = title_match.group(1).strip()
    
    # Cena - szukamy wzorca z formatem "123,99 zł"
    price_match = re.search(r'(\d+[\s,]?\d*)\s*zł', html)
    if price_match:
        price_str = price_match.group(1).replace(" ", "").replace(",", ".")
        try:
            offer_data["price"] = float(price_str)
        except ValueError:
            pass
    
    # "X osob kupilo te oferte" - kluczowa informacja
    buyers_match = re.search(r'(\d+)\s*os[oó]b[ay]?\s*kupi[łl][oayi]', html, re.IGNORECASE)
    if buyers_match:
        offer_data["buyers_count"] = int(buyers_match.group(1))
    
    # Smart! badge
    if "SMART" in html or "smart" in html.lower():
        offer_data["is_smart"] = True
    
    # Sprzedawca - zwykle w sekcji "od [nazwa]"
    seller_match = re.search(r'od\s+<[^>]+>([^<]+)</a>', html)
    if seller_match:
        offer_data["seller_name"] = seller_match.group(1).strip()
    
    # Offer ID z URL
    offer_id_match = re.search(r'/oferta/[^-]+-(\d+)', html)
    if offer_id_match:
        offer_data["offer_id"] = offer_id_match.group(1)
    
    if offer_data["title"] and offer_data["price"]:
        return OfferData(**offer_data)
    
    return None


def search_allegro_by_ean(ean: str, scraper: ScrapeDoClient, render: bool = True) -> List[OfferData]:
    """
    Wyszukuje produkty na Allegro po kodzie EAN.
    Zwraca liste ofert z informacjami o sprzedazy.
    
    Args:
        ean: Kod EAN produktu
        scraper: Instancja ScrapeDoClient
        render: Czy renderowac JavaScript (True = wiecej kredytow, lepsze dane)
    """
    search_url = f"https://allegro.pl/listing?string={quote_plus(ean)}"
    
    try:
        html = scraper.scrape(search_url, render=render)
        return parse_allegro_search_html(html)
    except ScraperError as e:
        print(f"Blad scrapowania: {e}")
        return []


def create_scrape_fetcher(render: bool = True) -> callable:
    """
    Tworzy funkcje do pobierania danych przez scrape.do.
    Uzywana jako data_fetcher w ProductProcessor.
    """
    scraper = ScrapeDoClient()
    
    def fetch(ean: str) -> List[dict]:
        offers = search_allegro_by_ean(ean, scraper, render=render)
        return [
            {
                "offer_id": o.offer_id,
                "title": o.title,
                "price": o.price,
                "currency": o.currency,
                "seller_name": o.seller_name,
                "buyers_count": o.buyers_count,
                "url": o.url,
                "is_smart": o.is_smart,
            }
            for o in offers
        ]
    
    return fetch


def test_scrape_do():
    """Testuje scrape.do na stronie Allegro."""
    from rich.console import Console
    from rich.panel import Panel
    
    console = Console()
    
    console.print(Panel("Test scrape.do", style="bold blue"))
    
    try:
        client = ScrapeDoClient()
        
        # Sprawdz kredyty
        console.print("[yellow]Sprawdzanie kredytow...[/yellow]")
        info = client.get_credits_info()
        console.print(f"  Info: {info}")
        
        # Test prostego scrapowania (bez render - mniej kredytow)
        console.print("\n[yellow]Test scrapowania strony Allegro (bez JS)...[/yellow]")
        test_url = "https://allegro.pl/listing?string=lampa+robocza+LED"
        
        try:
            html = client.scrape(test_url, render=False)
            console.print(f"[green]Sukces![/green] Otrzymano {len(html)} znakow HTML")
            
            # Sprawdz czy sa dane o "kupilo"
            if "kupi" in html.lower():
                console.print("[green]HTML zawiera informacje o zakupach![/green]")
            else:
                console.print("[yellow]HTML nie zawiera 'kupilo' - moze wymagac render=True[/yellow]")
            
            # Sprawdz czy wyglada jak zablokowany
            if "captcha" in html.lower() or "robot" in html.lower():
                console.print("[red]Wykryto CAPTCHA lub blokade![/red]")
                return False
            
            return True
            
        except ScraperError as e:
            console.print(f"[red]Blad:[/red] {e}")
            return False
            
    except ValueError as e:
        console.print(f"[red]Blad konfiguracji:[/red] {e}")
        console.print("[yellow]Utworz plik .env z SCRAPE_DO_TOKEN[/yellow]")
        return False


if __name__ == "__main__":
    test_scrape_do()
