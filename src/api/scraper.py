"""
Scraper do Allegro - scrape.do lub wlasny scraper.
"""
import os
import re
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
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


@dataclass
class ScrapeStats:
    """Statystyki zużycia scrape.do."""
    total_requests: int = 0
    total_credits_used: int = 0
    remaining_credits: Optional[int] = None
    max_monthly_credits: Optional[int] = None
    concurrent_limit: Optional[int] = None
    last_request_cost: Optional[int] = None
    last_updated: Optional[str] = None
    requests_history: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            "total_requests": self.total_requests,
            "total_credits_used": self.total_credits_used,
            "remaining_credits": self.remaining_credits,
            "max_monthly_credits": self.max_monthly_credits,
            "concurrent_limit": self.concurrent_limit,
            "last_request_cost": self.last_request_cost,
            "last_updated": self.last_updated,
            "requests_history": self.requests_history[-100:],  # Ostatnie 100
        }
    
    @property
    def usage_percent(self) -> float:
        if self.max_monthly_credits and self.remaining_credits is not None:
            used = self.max_monthly_credits - self.remaining_credits
            return (used / self.max_monthly_credits) * 100
        return 0.0


class ScraperError(Exception):
    pass


class ScrapeDoClient:
    """Klient do scrape.do API z śledzeniem zużycia."""
    
    BASE_URL = "https://api.scrape.do"
    INFO_RATE_LIMIT = 10  # max 10 zapytań /info na minutę
    
    def __init__(self, token: Optional[str] = None, verify_ssl: bool = True):
        self.token = token or os.getenv("SCRAPE_DO_TOKEN")
        self.verify_ssl = verify_ssl
        self.stats = ScrapeStats()
        self._last_info_check: Optional[datetime] = None
        
        if not self.token:
            raise ValueError("SCRAPE_DO_TOKEN musi byc ustawiony")
    
    def _make_request(self, url: str, params: dict = None, timeout: int = 60) -> requests.Response:
        """Wykonuje request z obsługą SSL."""
        try:
            return requests.get(url, params=params, timeout=timeout, verify=self.verify_ssl)
        except requests.exceptions.SSLError:
            return requests.get(url, params=params, timeout=timeout, verify=False)
    
    def _update_stats_from_headers(self, response: requests.Response, url: str):
        """Aktualizuje statystyki na podstawie headerów odpowiedzi."""
        headers = response.headers
        
        # Koszt tego requestu
        request_cost = headers.get('Scrape.do-Request-Cost') or headers.get('Scrape-Do-Request-Cost')
        if request_cost:
            try:
                cost = int(request_cost)
                self.stats.last_request_cost = cost
                self.stats.total_credits_used += cost
            except ValueError:
                pass
        
        # Pozostałe kredyty
        remaining = headers.get('Scrape.do-Remaining-Credits') or headers.get('Scrape-Do-Remaining-Credits')
        if remaining:
            try:
                self.stats.remaining_credits = int(remaining)
            except ValueError:
                pass
        
        # Aktualizuj historię
        self.stats.total_requests += 1
        self.stats.last_updated = datetime.now().isoformat()
        self.stats.requests_history.append({
            "timestamp": self.stats.last_updated,
            "url": url[:100],
            "cost": self.stats.last_request_cost,
            "remaining": self.stats.remaining_credits,
            "status": response.status_code,
        })
        
        # Ogranicz historię do 100 wpisów
        if len(self.stats.requests_history) > 100:
            self.stats.requests_history = self.stats.requests_history[-100:]
    
    def scrape(self, url: str, render: bool = True) -> str:
        """
        Scrapuje strone przez scrape.do.
        
        Koszty:
        - render=False: 1 kredyt (datacenter proxy)
        - render=True: 5 kredytów (headless browser)
        """
        params = {
            "token": self.token,
            "url": url,
            "render": str(render).lower(),
        }
        
        response = self._make_request(self.BASE_URL, params=params, timeout=60)
        
        # Aktualizuj statystyki z headerów
        self._update_stats_from_headers(response, url)
        
        if response.status_code != 200:
            raise ScraperError(f"scrape.do zwrocil {response.status_code}: {response.text[:200]}")
        
        return response.text
    
    def get_credits_info(self, force: bool = False) -> dict:
        """
        Sprawdza ile kredytów zostało.
        
        Ten endpoint NIE kosztuje kredytów, ale ma limit 10 zapytań/minutę.
        Zwraca:
            - IsActive: bool
            - ConcurrentRequest: int
            - MaxMonthlyRequest: int
            - RemainingConcurrentRequest: int
            - RemainingMonthlyRequest: int
        """
        url = f"{self.BASE_URL}/info?token={self.token}"
        response = self._make_request(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Aktualizuj statystyki
            self.stats.remaining_credits = data.get('RemainingMonthlyRequest')
            self.stats.max_monthly_credits = data.get('MaxMonthlyRequest')
            self.stats.concurrent_limit = data.get('ConcurrentRequest')
            self.stats.last_updated = datetime.now().isoformat()
            self._last_info_check = datetime.now()
            
            return data
        elif response.status_code == 429:
            return {"error": "Rate limit - max 10 zapytań/minutę na /info"}
        return {"error": f"Status {response.status_code}"}
    
    def get_usage_summary(self) -> dict:
        """Zwraca podsumowanie zużycia."""
        return {
            "session": {
                "requests": self.stats.total_requests,
                "credits_used": self.stats.total_credits_used,
                "last_cost": self.stats.last_request_cost,
            },
            "account": {
                "remaining": self.stats.remaining_credits,
                "max_monthly": self.stats.max_monthly_credits,
                "usage_percent": round(self.stats.usage_percent, 1),
            },
            "last_updated": self.stats.last_updated,
        }
    
    def estimate_cost(self, num_products: int, render: bool = True) -> dict:
        """
        Szacuje koszt sprawdzenia podanej liczby produktów.
        
        Koszty dla Allegro (nie jest na liście specjalnych domen):
        - render=True: 5 kredytów/zapytanie
        - render=False: 1 kredyt/zapytanie (ale może brakować danych)
        """
        cost_per_request = 5 if render else 1
        total_cost = num_products * cost_per_request
        
        remaining = self.stats.remaining_credits
        can_process = remaining // cost_per_request if remaining else None
        
        return {
            "cost_per_request": cost_per_request,
            "total_cost": total_cost,
            "remaining_credits": remaining,
            "can_process": can_process,
            "enough_credits": remaining >= total_cost if remaining else None,
        }


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
