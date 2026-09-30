"""
Allegro Price Monitor - glowny punkt wejscia.
Zrodlo danych: wylacznie scrape.do.
"""
import argparse
import sys
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Dodaj sciezke do importow
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.processor import ProductProcessor, ProcessorConfig, ProductResult
from src.core.cache import ProductCache

console = Console()


def create_data_fetcher():
    """Tworzy funkcje do pobierania danych przez scrape.do."""
    try:
        from src.api.scraper import create_scrape_fetcher, ScrapeDoClient
        import warnings
        warnings.filterwarnings('ignore', category=Warning)

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


def progress_callback(current: int, total: int, result: ProductResult):
    """Callback dla postępu - wyswietla informacje o biezacym produkcie."""
    status_icon = "✓" if result.found_on_allegro else "✗"
    match_info = ""
    if result.best_match:
        match_info = f" | Najlepsza: {result.best_match.price} PLN ({result.best_match.buyers_count} kupilo)"
    console.print(f"  [{current}/{total}] {status_icon} {result.ean}{match_info}")


def run_console_mode(args):
    """Uruchamia tryb konsolowy."""
    console.print(Panel("Allegro Price Monitor - Tryb konsolowy (scrape.do)", style="bold blue"))

    config = ProcessorConfig.from_yaml(args.config)
    console.print(f"[dim]Konfiguracja: markup {config.min_markup*100:.0f}-{config.max_markup*100:.0f}%, "
                  f"min kupujacych: {config.min_buyers}, TTL: {config.ttl_days} dni[/dim]")

    fetcher = create_data_fetcher()
    if not fetcher:
        console.print("[red]Nie mozna utworzyc polaczenia ze scrape.do![/red]")
        console.print("[yellow]Sprawdz SCRAPE_DO_TOKEN w pliku .env[/yellow]")
        return

    processor = ProductProcessor(config=config, data_fetcher=fetcher)

    if not Path(args.input).exists():
        console.print(f"[red]Plik wejsciowy nie istnieje: {args.input}[/red]")
        return

    products = processor.load_input_csv(args.input)
    console.print(f"[green]Wczytano {len(products)} produktow[/green]")

    if not products:
        console.print("[yellow]Brak produktow do sprawdzenia[/yellow]")
        return

    console.print("\n[bold]Rozpoczynam sprawdzanie...[/bold]")
    results = processor.process_batch(products, progress_callback=progress_callback)

    output_path = args.output
    if not output_path:
        date_str = datetime.now().strftime("%Y-%m-%d_%H%M")
        output_path = f"data/output/results_{date_str}.json"

    processor.save_results(output_path, results)
    console.print(f"\n[green]Wyniki zapisane do: {output_path}[/green]")

    table = Table(title="Podsumowanie")
    table.add_column("Metryka", style="cyan")
    table.add_column("Wartosc", style="green")

    table.add_row("Sprawdzonych produktow", str(len(results)))
    table.add_row("Znalezionych na Allegro", str(sum(1 for r in results if r.found_on_allegro)))
    table.add_row("Z pasujacymi ofertami", str(sum(1 for r in results if r.matching_offers)))
    table.add_row("Bledow", str(sum(1 for r in results if r.status == "error")))

    console.print(table)


def run_test_mode():
    """Uruchamia test scrape.do."""
    console.print(Panel("Allegro Price Monitor - Test scrape.do", style="bold blue"))

    console.print("\n[bold]Test scrape.do[/bold]")
    from src.api.scraper import test_scrape_do
    scrape_ok = test_scrape_do()

    console.print("\n[bold]Podsumowanie:[/bold]")
    console.print(f"  scrape.do: {'[green]OK[/green]' if scrape_ok else '[red]BLAD[/red]'}")

    if scrape_ok:
        console.print("\n[green]Mozesz scrapowac oferty Allegro przez scrape.do[/green]")
    else:
        console.print("\n[red]Sprawdz SCRAPE_DO_TOKEN w .env[/red]")


def main():
    parser = argparse.ArgumentParser(
        description="Allegro Price Monitor - sprawdzanie cen i sprzedazy produktow (scrape.do)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Dostepne komendy")

    run_parser = subparsers.add_parser("run", help="Uruchom sprawdzanie produktow")
    run_parser.add_argument("-i", "--input", required=True, help="Plik CSV z produktami (EAN;cena)")
    run_parser.add_argument("-o", "--output", help="Plik wyjsciowy JSON (domyslnie: data/output/results_DATA.json)")
    run_parser.add_argument("-c", "--config", default="config.yaml", help="Plik konfiguracji")

    subparsers.add_parser("test", help="Testuj polaczenie ze scrape.do")
    subparsers.add_parser("gui", help="Uruchom interfejs graficzny")

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
