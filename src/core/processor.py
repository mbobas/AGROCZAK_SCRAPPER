"""
Glowny procesor - logika przetwarzania listy produktow.
"""
import csv
import json
import time
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
import yaml

from .cache import ProductCache
from .matching import build_search_query, normalize


@dataclass
class InputProduct:
    ean: str
    my_price: float
    name: Optional[str] = None


@dataclass 
class AllegroOffer:
    offer_id: str
    title: str
    price: float
    currency: str = "PLN"
    seller_name: Optional[str] = None
    buyers_count: Optional[int] = None
    url: Optional[str] = None
    is_smart: bool = False


@dataclass
class ProductResult:
    ean: str
    my_price: float
    name: Optional[str] = None
    checked_at: str = ""
    found_on_allegro: bool = False
    offers: List[AllegroOffer] = field(default_factory=list)
    matching_offers: List[AllegroOffer] = field(default_factory=list)  # w przedziale cenowym
    best_match: Optional[AllegroOffer] = None
    status: str = "pending"  # pending, checked, error
    error_message: Optional[str] = None
    from_cache: bool = False
    search_mode: str = "code"  # code | name
    search_query: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["offers"] = [
            asdict(o) if hasattr(o, "__dataclass_fields__") else o for o in self.offers
        ]
        result["matching_offers"] = [
            asdict(o) if hasattr(o, "__dataclass_fields__") else o
            for o in self.matching_offers
        ]
        if self.best_match is None:
            result["best_match"] = None
        elif hasattr(self.best_match, "__dataclass_fields__"):
            result["best_match"] = asdict(self.best_match)
        else:
            result["best_match"] = self.best_match
        return result


@dataclass
class ProcessorConfig:
    min_markup: float = 0.0
    max_markup: float = 0.50
    min_buyers: int = 0
    ttl_days: int = 7
    delay_seconds: float = 6.0
    
    @classmethod
    def from_yaml(cls, path: str = "config.yaml") -> "ProcessorConfig":
        try:
            with open(path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            return cls(
                min_markup=config.get("price_threshold", {}).get("min_markup", 0.0),
                max_markup=config.get("price_threshold", {}).get("max_markup", 0.50),
                min_buyers=config.get("sales_threshold", {}).get("min_buyers", 0),
                ttl_days=config.get("cache", {}).get("ttl_days", 7),
                delay_seconds=config.get("rate_limit", {}).get("delay_between_requests", 6),
            )
        except FileNotFoundError:
            return cls()


class ProductProcessor:
    """Glowny procesor do sprawdzania produktow na Allegro."""
    
    def __init__(self, config: Optional[ProcessorConfig] = None,
                 data_fetcher: Optional[Callable] = None,
                 search_mode: str = "code"):
        self.search_mode = search_mode if search_mode in ("code", "name") else "code"
        self.config = config or ProcessorConfig.from_yaml()
        self.cache = ProductCache()
        self.data_fetcher = data_fetcher  # funkcja do pobierania danych z Allegro
        
        self._running = False
        self._paused = False
        self._current_index = 0
        self._results: List[ProductResult] = []
        self._progress_callback: Optional[Callable] = None
    
    def load_input_csv(self, path: str) -> List[InputProduct]:
        """Wczytuje liste produktow z CSV."""
        products = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                ean = row.get("ean") or row.get("EAN") or row.get("kod") or row.get("code", "")
                price = row.get("cena") or row.get("price") or row.get("my_price", "0")
                name = row.get("nazwa") or row.get("name", "")
                
                try:
                    price_float = float(str(price).replace(",", ".").replace(" ", ""))
                except ValueError:
                    price_float = 0.0
                
                if ean:
                    products.append(InputProduct(
                        ean=ean.strip(),
                        my_price=price_float,
                        name=name.strip() if name else None
                    ))
        return products
    
    def check_price_match(self, my_price: float, allegro_price: float) -> bool:
        """Sprawdza czy cena Allegro jest w przedziale marży (config)."""
        min_price = my_price * (1 + self.config.min_markup)
        max_price = my_price * (1 + self.config.max_markup)
        return min_price <= allegro_price <= max_price
    
    def check_sales(self, buyers_count: Optional[int]) -> bool:
        """Sprawdza czy produkt sie sprzedaje. min_buyers<=0 = bez wymogu (null OK)."""
        if self.config.min_buyers <= 0:
            return True
        if buyers_count is None:
            return False
        return buyers_count >= self.config.min_buyers
    
    def process_single(self, product: InputProduct) -> ProductResult:
        """Przetwarza pojedynczy produkt."""
        result = ProductResult(
            ean=product.ean,
            my_price=product.my_price,
            name=product.name,
            checked_at=datetime.now().isoformat(),
            search_mode=self.search_mode,
        )
        
        if self.search_mode == "name":
            query = build_search_query(product.name)
            cache_key = f"name::{normalize(query)}"
        else:
            query = product.ean
            cache_key = product.ean
        result.search_query = query
        
        if not query:
            result.status = "error"
            result.error_message = "Brak nazwy produktu do wyszukania"
            return result
        
        # Sprawdz cache
        cached = self.cache.get_if_valid(cache_key, self.config.ttl_days)
        if cached:
            field_names = set(ProductResult.__dataclass_fields__.keys())
            data = {k: v for k, v in cached.items() if k in field_names}
            data["from_cache"] = True
            # Nazwa i cena z biezacego wejscia (cache moze pochodzic ze starego formatu)
            data["name"] = product.name or data.get("name")
            data["my_price"] = product.my_price
            data["ean"] = product.ean
            data["search_mode"] = self.search_mode
            data["search_query"] = query
            return ProductResult(**data)
        
        if not self.data_fetcher:
            result.status = "error"
            result.error_message = "Brak skonfigurowanego fetchera danych"
            return result
        
        try:
            # Pobierz dane z Allegro
            offers_data = self.data_fetcher(query)
            
            if not offers_data:
                result.status = "checked"
                result.found_on_allegro = False
                self.cache.set(cache_key, result.to_dict())
                return result
            
            result.found_on_allegro = True
            result.offers = [AllegroOffer(**o) for o in offers_data]
            
            # Filtruj oferty spelniajace kryteria
            for offer in result.offers:
                price_ok = self.check_price_match(product.my_price, offer.price)
                sales_ok = self.check_sales(offer.buyers_count)
                
                if price_ok and sales_ok:
                    result.matching_offers.append(offer)
            
            # Wybierz najlepsza oferte (najwiecej kupujacych)
            if result.matching_offers:
                result.best_match = max(
                    result.matching_offers,
                    key=lambda o: o.buyers_count or 0
                )
            
            result.status = "checked"
            self.cache.set(cache_key, result.to_dict())
            
        except Exception as e:
            result.status = "error"
            result.error_message = str(e)
            # Bledow nie cache'ujemy — unikamy falszywego "nie znaleziono"
        
        return result
    
    def process_batch(self, products: List[InputProduct],
                      progress_callback: Optional[Callable] = None) -> List[ProductResult]:
        """Przetwarza liste produktow."""
        self._running = True
        self._paused = False
        self._results = []
        self._progress_callback = progress_callback
        
        for i, product in enumerate(products):
            if not self._running:
                break
            
            while self._paused:
                time.sleep(0.5)
                if not self._running:
                    break
            
            self._current_index = i
            result = self.process_single(product)
            self._results.append(result)
            
            if progress_callback:
                progress_callback(i + 1, len(products), result)
            
            # Rate limiting
            if i < len(products) - 1:
                time.sleep(self.config.delay_seconds)
        
        self._running = False
        return self._results
    
    def pause(self):
        self._paused = True
    
    def resume(self):
        self._paused = False
    
    def stop(self):
        self._running = False
    
    @property
    def is_running(self) -> bool:
        return self._running
    
    @property
    def is_paused(self) -> bool:
        return self._paused
    
    @property
    def current_progress(self) -> tuple:
        return (self._current_index, len(self._results))
    
    def save_results(self, path: str, results: Optional[List[ProductResult]] = None):
        """Zapisuje wyniki do pliku JSON."""
        results = results or self._results
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "generated_at": datetime.now().isoformat(),
            "config": asdict(self.config),
            "total_products": len(results),
            "found_on_allegro": sum(1 for r in results if r.found_on_allegro),
            "with_matching_offers": sum(1 for r in results if r.matching_offers),
            "products": [r.to_dict() for r in results]
        }
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def save_results_csv(self, path: str, results: Optional[List[ProductResult]] = None):
        """Zapisuje wyniki do CSV (uproszczone)."""
        results = results or self._results
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow([
                "Kod", "Moja cena", "Nazwa", "Znaleziono", 
                "Najlepsza oferta - cena", "Najlepsza oferta - kupilo osob",
                "Najlepsza oferta - URL", "Status"
            ])
            
            for r in results:
                best = r.best_match
                writer.writerow([
                    r.ean,
                    r.my_price,
                    r.name or "",
                    "Tak" if r.found_on_allegro else "Nie",
                    best.price if best else "",
                    best.buyers_count if best else "",
                    best.url if best else "",
                    r.status
                ])
