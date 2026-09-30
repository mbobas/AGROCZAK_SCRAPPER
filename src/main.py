"""
Allegro Price Monitor - glowny punkt wejscia.
"""
import argparse
import sys
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.table import Table

# Dodaj sciezke do importow
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api.allegro import AllegroClient, AllegroAPIError
from src.api.scraper import ScrapeDoClient, ScraperError
from src.core.processor import ProductProcessor, ProcessorConfig, InputProduct, ProductResult
from src.core.cache import ProductCache

console = Console()


def create_data_fetcher(mode: str = "api"):
    """Tworzy funkcje do pobierania danych w zaleznosci od trybu."""
    
    if mode == "api":
        try:
            client = AllegroClient()
            client.get_token()
            
            def fetch_api(ean: str):
                try:
                    result = client.search_offers(phrase=ean)
                    items = result.get("items", {})
                    offers = items.get("promoted", []) + items.get("regular", [])
                    
                    return [{
                        "offer_id": o.get("id", ""),
                        "title": o.get("name", ""),
                        "price": float(o.get("sellingMode", {}).get("price", {}).get("amount", 0)),
                        "currency": o.get("sellingMode", {}).get("price", {}).get("currency", "PLN"),
                        "seller_name": o.get("seller", {}).get("login", ""),
                        "buyers_count": o.get("popularity", {}).get("soldCount"),
                        "url": f"https://allegro.pl/oferta/{o.get('id', '')}",
                        "is_smart": o.get("delivery", {}).get("smart", False),
                    } for o in offers]
                except AllegroAPIError:
                    return []
            
            return fetch_api
            
        except Exception as e:
            console.print(f"[yellow]API Allegro niedostepne: {e}[/yellow]")
            return None
    
    elif mode == "scrape_do":
        try:
            from src.api.scraper import create_scrape_fetcher, ScrapeDoClient
            import warnings
            warnings.filterwarnings('ignore', category=Warning)
            
            # Sprawdz kredyty
            client = ScrapeDoClient()
            info = client.get_credits_info()
            remaining = info.get('RemainingMonthlyRequest', 0)
            console.print(f"[dim]scrape.do: {remaining} kredytow pozostalo[/dim]")
            
            if remaining < 10:
                console.print("[red]Za malo kredytow scrape.do![/red]")
                return None
            
            return create_scrape_fetcher(render=True)
            
        except Exception as e:
            console.print(f"[yellow]scrape.do niedostepne: {e}[/yellow]")
            return None
    
    return None


def progress_callback(current: int, total: int, result: ProductResult):
    """Callback dla postępu - wyswietla informacje o biezacym produkcie."""
    status_icon = "✓" if result.found_on_allegro else "✗"
    match_info = ""
    if result.best_match:
        match_info = f" | Najlepsza: {result.best_match.price} PLN ({result.best_match.buyers_count} kupilo)"
    console.print(f"  [{current}/{total}] {status_icon} {result.ean}{match_info}")


def run_console_mode(args):
    """Uruchamia tryb konsolowy."""
    console.print(Panel("Allegro Price Monitor - Tryb konsolowy", style="bold blue"))
    
    # Wczytaj konfiguracje
    config = ProcessorConfig.from_yaml(args.config)
    console.print(f"[dim]Konfiguracja: markup {config.min_markup*100:.0f}-{config.max_markup*100:.0f}%, "
                  f"min kupujacych: {config.min_buyers}, TTL: {config.ttl_days} dni[/dim]")
    
    # Utworz fetcher
    fetcher = create_data_fetcher(args.source)
    if not fetcher:
        console.print("[red]Nie mozna utworzyc polaczenia z Allegro![/red]")
        console.print("[yellow]Sprawdz plik .env i credentiale[/yellow]")
        return
    
    # Utworz procesor
    processor = ProductProcessor(config=config, data_fetcher=fetcher)
    
    # Wczytaj dane wejsciowe
    if not Path(args.input).exists():
        console.print(f"[red]Plik wejsciowy nie istnieje: {args.input}[/red]")
        return
    
    products = processor.load_input_csv(args.input)
    console.print(f"[green]Wczytano {len(products)} produktow[/green]")
    
    if not products:
        console.print("[yellow]Brak produktow do sprawdzenia[/yellow]")
        return
    
    # Przetwarzaj
    console.print("\n[bold]Rozpoczynam sprawdzanie...[/bold]")
    results = processor.process_batch(products, progress_callback=progress_callback)
    
    # Zapisz wyniki
    output_path = args.output
    if not output_path:
        date_str = datetime.now().strftime("%Y-%m-%d_%H%M")
        output_path = f"data/output/results_{date_str}.json"
    
    processor.save_results(output_path, results)
    console.print(f"\n[green]Wyniki zapisane do: {output_path}[/green]")
    
    # Podsumowanie
    table = Table(title="Podsumowanie")
    table.add_column("Metryka", style="cyan")
    table.add_column("Wartosc", style="green")
    
    table.add_row("Sprawdzonych produktow", str(len(results)))
    table.add_row("Znalezionych na Allegro", str(sum(1 for r in results if r.found_on_allegro)))
    table.add_row("Z pasujacymi ofertami", str(sum(1 for r in results if r.matching_offers)))
    table.add_row("Bledow", str(sum(1 for r in results if r.status == "error")))
    
    console.print(table)


def run_test_mode():
    """Uruchamia testy API i scrape.do."""
    console.print(Panel("Allegro Price Monitor - Tryb testowy", style="bold blue"))
    
    # Test API
    console.print("\n[bold]1. Test API Allegro[/bold]")
    from src.api.allegro import test_api_access
    api_ok = test_api_access()
    
    # Test scrape.do
    console.print("\n[bold]2. Test scrape.do[/bold]")
    from src.api.scraper import test_scrape_do
    scrape_ok = test_scrape_do()
    
    # Podsumowanie
    console.print("\n[bold]Podsumowanie:[/bold]")
    console.print(f"  API Allegro /offers/listing: {'[green]OK[/green]' if api_ok else '[red]NIEDOSTEPNE[/red]'}")
    console.print(f"  scrape.do: {'[green]OK[/green]' if scrape_ok else '[red]NIEDOSTEPNE[/red]'}")
    
    if api_ok:
        console.print("\n[green]Mozesz uzyc trybu API (--source api)[/green]")
    elif scrape_ok:
        console.print("\n[yellow]Uzyj trybu scrape.do (--source scrape_do)[/yellow]")
    else:
        console.print("\n[red]Brak dostepnych zrodel danych![/red]")


def main():
    parser = argparse.ArgumentParser(
        description="Allegro Price Monitor - sprawdzanie cen i sprzedazy produktow"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Dostepne komendy")
    
    # Komenda: run
    run_parser = subparsers.add_parser("run", help="Uruchom sprawdzanie produktow")
    run_parser.add_argument("-i", "--input", required=True, help="Plik CSV z produktami (EAN;cena)")
    run_parser.add_argument("-o", "--output", help="Plik wyjsciowy JSON (domyslnie: data/output/results_DATA.json)")
    run_parser.add_argument("-c", "--config", default="config.yaml", help="Plik konfiguracji")
    run_parser.add_argument("-s", "--source", choices=["api", "scrape_do"], default="api",
                          help="Zrodlo danych: api lub scrape_do")
    
    # Komenda: test
    test_parser = subparsers.add_parser("test", help="Testuj polaczenie z API/scrape.do")
    
    # Komenda: gui
    gui_parser = subparsers.add_parser("gui", help="Uruchom interfejs graficzny")
    
    # Komenda: cache
    cache_parser = subparsers.add_parser("cache", help="Zarzadzanie cache")
    cache_parser.add_argument("action", choices=["stats", "clear", "clear-expired"],
                             help="Akcja: stats, clear, clear-expired")
    
    args = parser.parse_args()
    
    if args.command == "run":
        run_console_mode(args)
    elif args.command == "test":
        run_test_mode()
    elif args.command == "gui":
        console.print("[yellow]Uruchamianie GUI...[/yellow]")
        console.print("Uzyj: streamlit run src/gui/dashboard.py")
    elif args.command == "cache":
        cache = ProductCache()
        if args.action == "stats":
            stats = cache.get_stats()
            console.print(f"Produktow w cache: {stats['total_products']}")
            console.print(f"Najstarsze sprawdzenie: {stats['oldest_check']}")
            console.print(f"Najnowsze sprawdzenie: {stats['newest_check']}")
        elif args.action == "clear":
            cache.clear_all()
            console.print("[green]Cache wyczyszczony[/green]")
        elif args.action == "clear-expired":
            config = ProcessorConfig.from_yaml()
            removed = cache.clear_expired(config.ttl_days)
            console.print(f"[green]Usunieto {removed} wygaslych wpisow[/green]")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
