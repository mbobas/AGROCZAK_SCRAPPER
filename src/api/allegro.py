"""
Klient API Allegro - obsluga autentykacji i zapytan do API.
"""
import base64
import os
from dataclasses import dataclass
from typing import Optional
import requests
from dotenv import load_dotenv

load_dotenv()


@dataclass
class AllegroToken:
    access_token: str
    token_type: str
    expires_in: int


class AllegroAPIError(Exception):
    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(f"[{status_code}] {code}: {message}")


class AllegroClient:
    AUTH_URL = "https://allegro.pl/auth/oauth/token"
    API_URL = "https://api.allegro.pl"
    
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        self.client_id = client_id or os.getenv("ALLEGRO_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("ALLEGRO_CLIENT_SECRET")
        self._token: Optional[AllegroToken] = None
        
        if not self.client_id or not self.client_secret:
            raise ValueError("ALLEGRO_CLIENT_ID i ALLEGRO_CLIENT_SECRET musza byc ustawione")
    
    def _get_auth_header(self) -> str:
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"
    
    def get_token(self) -> AllegroToken:
        """Pobiera token Client Credentials Flow."""
        headers = {
            "Authorization": self._get_auth_header(),
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"grant_type": "client_credentials"}
        
        response = requests.post(self.AUTH_URL, headers=headers, data=data)
        
        if response.status_code != 200:
            error_data = response.json()
            raise AllegroAPIError(
                response.status_code,
                error_data.get("error", "unknown"),
                error_data.get("error_description", "Unknown error")
            )
        
        token_data = response.json()
        self._token = AllegroToken(
            access_token=token_data["access_token"],
            token_type=token_data["token_type"],
            expires_in=token_data["expires_in"]
        )
        return self._token
    
    def _get_headers(self) -> dict:
        if not self._token:
            self.get_token()
        return {
            "Authorization": f"Bearer {self._token.access_token}",
            "Accept": "application/vnd.allegro.public.v1+json",
            "Accept-Language": "pl-PL",
        }
    
    def search_offers(self, phrase: str = None, ean: str = None, 
                      category_id: str = None, limit: int = 20) -> dict:
        """
        Wyszukuje oferty na Allegro (endpoint /offers/listing).
        Wymaga zweryfikowanej aplikacji - moze zwrocic 403.
        """
        params = {"limit": limit}
        if phrase:
            params["phrase"] = phrase
        if category_id:
            params["category.id"] = category_id
        
        url = f"{self.API_URL}/offers/listing"
        response = requests.get(url, headers=self._get_headers(), params=params)
        
        if response.status_code != 200:
            error_data = response.json()
            errors = error_data.get("errors", [{}])
            first_error = errors[0] if errors else {}
            raise AllegroAPIError(
                response.status_code,
                first_error.get("code", "unknown"),
                first_error.get("message", "Unknown error")
            )
        
        return response.json()
    
    def search_products(self, ean: str = None, phrase: str = None, 
                        mode: str = "GTIN", limit: int = 20) -> dict:
        """
        Wyszukuje produkty w katalogu Allegro (endpoint /sale/products).
        Ten endpoint jest dostepny dla wszystkich aplikacji.
        """
        params = {"limit": limit}
        if ean:
            params["phrase"] = ean
            params["mode"] = mode
        elif phrase:
            params["phrase"] = phrase
        
        url = f"{self.API_URL}/sale/products"
        response = requests.get(url, headers=self._get_headers(), params=params)
        
        if response.status_code != 200:
            error_data = response.json()
            errors = error_data.get("errors", [{}])
            first_error = errors[0] if errors else {}
            raise AllegroAPIError(
                response.status_code,
                first_error.get("code", "unknown"),
                first_error.get("message", "Unknown error")
            )
        
        return response.json()


def test_api_access():
    """Testuje dostep do API Allegro."""
    from rich.console import Console
    from rich.panel import Panel
    
    console = Console()
    
    console.print(Panel("Test API Allegro", style="bold blue"))
    
    try:
        client = AllegroClient()
        console.print("[yellow]Pobieranie tokena...[/yellow]")
        token = client.get_token()
        console.print(f"[green]Token uzyskany![/green] Wazny przez {token.expires_in}s")
        
        console.print("\n[yellow]Test 1: /sale/products (katalog produktow)...[/yellow]")
        try:
            result = client.search_products(ean="5902719471797")
            products = result.get("products", [])
            console.print(f"[green]Sukces![/green] Znaleziono {len(products)} produktow")
            if products:
                console.print(f"  Przyklad: {products[0].get('name', 'brak nazwy')}")
        except AllegroAPIError as e:
            console.print(f"[red]Blad:[/red] {e}")
        
        console.print("\n[yellow]Test 2: /offers/listing (publiczne oferty)...[/yellow]")
        try:
            result = client.search_offers(phrase="lampa robocza LED")
            items = result.get("items", {}).get("promoted", []) + result.get("items", {}).get("regular", [])
            console.print(f"[green]Sukces![/green] Masz dostep do /offers/listing!")
            console.print(f"  Znaleziono {len(items)} ofert")
            return True
        except AllegroAPIError as e:
            if e.status_code == 403:
                console.print(f"[red]Brak dostepu (403):[/red] {e.code}")
                console.print("[yellow]Aplikacja nie jest zweryfikowana - /offers/listing niedostepny[/yellow]")
            else:
                console.print(f"[red]Blad:[/red] {e}")
            return False
            
    except ValueError as e:
        console.print(f"[red]Blad konfiguracji:[/red] {e}")
        console.print("[yellow]Utworz plik .env z ALLEGRO_CLIENT_ID i ALLEGRO_CLIENT_SECRET[/yellow]")
        return False
    except Exception as e:
        console.print(f"[red]Nieoczekiwany blad:[/red] {e}")
        return False


if __name__ == "__main__":
    test_api_access()
