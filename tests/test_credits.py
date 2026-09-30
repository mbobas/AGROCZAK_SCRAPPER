"""Test śledzenia kredytów scrape.do."""
import warnings
warnings.filterwarnings('ignore')

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api.scraper import ScrapeDoClient

def main():
    client = ScrapeDoClient()
    
    # Pobierz info o kredytach
    print("Pobieranie info o kredytach...")
    info = client.get_credits_info()
    print(f"Info: {info}")
    
    # Podsumowanie
    summary = client.get_usage_summary()
    print(f"\nPodsumowanie:")
    print(f"  Sesja: {summary['session']}")
    print(f"  Konto: {summary['account']}")
    
    # Szacowanie kosztów
    print("\n--- Szacowanie kosztow ---")
    for num_products in [10, 50, 100, 200]:
        estimate = client.estimate_cost(num_products, render=True)
        remaining = estimate['remaining_credits']
        total_cost = estimate['total_cost']
        after = remaining - total_cost if remaining else 'N/A'
        enough = 'TAK' if estimate['enough_credits'] else 'NIE'
        print(f"  {num_products} produktow: {total_cost} kredytow, pozostanie: {after}, wystarczy: {enough}")

if __name__ == "__main__":
    main()
