"""Sprawdz strukture JSON - szukaj URL."""
import json
import re

with open('data/output/test_scrape_render.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Znajdz JSON
store_match = re.search(r'\{"__listing_StoreState":(.*?)\}\s*</script>', html, re.DOTALL)
if store_match:
    store_data = json.loads('{"__listing_StoreState":' + store_match.group(1) + '}')
    items = store_data.get('__listing_StoreState', {}).get('items', {}).get('elements', [])
    
    if items:
        item = items[0]
        print("Klucze pierwszego itemu:")
        for key in sorted(item.keys()):
            val = item[key]
            if isinstance(val, str) and len(val) > 100:
                val = val[:100] + "..."
            print(f"  {key}: {val}")
