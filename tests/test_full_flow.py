"""Test pelnego flow - wyszukiwanie po EAN."""
import warnings
warnings.filterwarnings('ignore')

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api.scraper import ScrapeDoClient, search_allegro_by_ean

# Test wyszukiwania po EAN
client = ScrapeDoClient()
info = client.get_credits_info()
print(f"Kredyty przed: {info.get('RemainingMonthlyRequest', 'N/A')}")

# Szukaj produktu po EAN
ean = '5902719471797'  # Przykladowy EAN
print(f"\nSzukam EAN: {ean}")

offers = search_allegro_by_ean(ean, client, render=True)
print(f"Znaleziono {len(offers)} ofert\n")

for i, offer in enumerate(offers[:5]):
    title = offer.title[:40] if offer.title else "Brak tytulu"
    print(f"{i+1}. {title}...")
    print(f"   Cena: {offer.price} PLN")
    print(f"   Kupilo: {offer.buyers_count}")
    print(f"   URL: {offer.url[:60]}..." if offer.url else "   URL: brak")
    print()

info = client.get_credits_info()
print(f"Kredyty po: {info.get('RemainingMonthlyRequest', 'N/A')}")
