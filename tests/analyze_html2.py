"""Analiza struktury HTML Allegro - szukanie JSON."""
from bs4 import BeautifulSoup
import re
import json

with open('data/output/test_scrape_render.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Szukaj skryptow z danymi JSON
scripts = soup.find_all('script', type='application/json')
print(f'Skrypty JSON: {len(scripts)}')

# Szukaj __NEXT_DATA__ (Next.js)
next_data = soup.find('script', id='__NEXT_DATA__')
if next_data:
    print('Znaleziono __NEXT_DATA__')
    try:
        data = json.loads(next_data.string)
        # Zapisz do pliku do analizy
        with open('data/output/next_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print('Zapisano do data/output/next_data.json')
        
        # Sprobuj znalezc oferty
        def find_offers(obj, path=''):
            """Rekurencyjnie szukaj ofert."""
            if isinstance(obj, dict):
                # Sprawdz czy to oferta
                if 'price' in obj or 'sellingMode' in obj:
                    print(f'Znaleziono oferte: {path}')
                    return [obj]
                    
                results = []
                for k, v in obj.items():
                    results.extend(find_offers(v, f'{path}.{k}'))
                return results
            elif isinstance(obj, list):
                results = []
                for i, item in enumerate(obj):
                    results.extend(find_offers(item, f'{path}[{i}]'))
                return results
            return []
        
        offers = find_offers(data)
        print(f'Znaleziono {len(offers)} potencjalnych ofert')
        
    except json.JSONDecodeError as e:
        print(f'Blad parsowania JSON: {e}')

# Szukaj innych skryptow z danymi
for script in soup.find_all('script'):
    text = script.string or ''
    if 'items' in text and 'price' in text and len(text) > 1000:
        print(f'\nZnaleziono skrypt z items/price ({len(text)} znakow)')
        # Sprobuj wyciagnac JSON
        json_match = re.search(r'(\{.*"items".*\})', text, re.DOTALL)
        if json_match:
            try:
                # Fragment moze byc za duzy, pokaz tylko poczatek
                print(f'Fragment: {json_match.group(1)[:500]}...')
            except:
                pass

# Sprawdz article
articles = soup.find_all('article')
print(f'\n--- Analiza {len(articles)} artykulow ---')

for i, article in enumerate(articles[:3]):
    print(f'\nArticle {i+1}:')
    
    # Wszystkie linki
    links = article.find_all('a')
    for link in links[:3]:
        href = link.get('href', '')
        if href:
            print(f'  Link: {href[:60]}')
    
    # Tekst
    text = article.get_text()[:200].replace('\n', ' ')
    print(f'  Tekst: {text}...')
    
    # Data atrybuty
    data_attrs = {k: v for k, v in article.attrs.items() if k.startswith('data-')}
    if data_attrs:
        print(f'  Data attrs: {list(data_attrs.keys())}')
