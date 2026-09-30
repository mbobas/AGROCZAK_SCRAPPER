"""Analiza struktury HTML Allegro."""
from bs4 import BeautifulSoup
import re
import json

with open('data/output/test_scrape_render.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Sprawdz ile jest artykulow
articles = soup.find_all('article')
print(f'Article: {len(articles)}')

# Szukaj div z ofertami
divs_with_offer = soup.find_all('div', attrs={'data-analytics-click-value': True})
print(f'Div z data-analytics: {len(divs_with_offer)}')

# Szukaj linkow do ofert
links = soup.find_all('a', href=re.compile(r'/oferta/'))
print(f'Linki do ofert: {len(links)}')

# Pokaz przyklad linku
if links:
    link = links[0]
    href = link.get('href', '')
    print(f'Przyklad href: {href[:80]}')
    print(f'Tekst linku: {link.get_text()[:100]}')
    
    # Znajdz rodzica - container oferty
    container = link
    for _ in range(10):
        parent = container.find_parent()
        if parent:
            container = parent
            # Szukaj ceny i kupujacych w tym kontenerze
            text = container.get_text()
            if 'kupi' in text.lower() and 'zł' in text:
                print(f'\nZnaleziono kontener na poziomie: {container.name}')
                # Szukaj ceny
                price_match = re.search(r'(\d+[,\.]\d{2})\s*zł', text)
                if price_match:
                    print(f'Cena: {price_match.group(1)} zł')
                # Szukaj kupujacych
                buyers_match = re.search(r'(\d+)\s*os', text)
                if buyers_match:
                    print(f'Kupujacych: {buyers_match.group(1)}')
                break

# Znajdz wszystkie kontenery ofert
print('\n--- Szukanie wszystkich ofert ---')

# Metoda 1: Szukaj sekcji z wieloma linkami do ofert
main_section = soup.find('section') or soup.find('main') or soup.find('div', class_=re.compile(r'listing'))
if main_section:
    print(f'Glowna sekcja: {main_section.name}')

# Metoda 2: Znajdz wszystkie elementy z linkiem do oferty i cena
offers_found = []
for link in links[:20]:  # Pierwsze 20
    # Idz w gore drzewa az znajdziesz element z cena
    container = link
    for _ in range(8):
        parent = container.find_parent()
        if parent:
            container = parent
            text = container.get_text()
            # Sprawdz czy ma cene i kupujacych
            price_match = re.search(r'(\d+[,\.]\d{2})\s*zł', text)
            buyers_match = re.search(r'(\d+)\s*os[oó]b', text, re.IGNORECASE)
            if price_match:
                offers_found.append({
                    'href': link.get('href', '')[:60],
                    'title': link.get_text()[:50],
                    'price': price_match.group(1),
                    'buyers': buyers_match.group(1) if buyers_match else None,
                    'container_tag': container.name,
                    'container_class': container.get('class', [])[:3]
                })
                break

print(f'\nZnaleziono {len(offers_found)} ofert z cenami')
for i, offer in enumerate(offers_found[:5]):
    print(f'\n{i+1}. {offer["title"]}...')
    print(f'   Cena: {offer["price"]} zł')
    print(f'   Kupilo: {offer["buyers"]}')
    print(f'   Container: {offer["container_tag"]} class={offer["container_class"]}')
