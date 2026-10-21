"""
Glowny procesor - logika przetwarzania listy produktow.
"""
import csv
import json
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable, Tuple
import yaml

from .cache import ProductCache
from .job_state import is_pause_requested, is_stop_requested, write_status
from .matching import build_search_query, normalize
from .results_io import (
    partial_results_path,
    search_mode_suffix,
    stream_save_product_dicts,
)
from .results_io import OUTPUT_DIR, ensure_output_dir

PARTIAL_SAVE_EVERY_SCRAPED = 500
CACHE_PROGRESS_EVERY = 100
CACHE_LOAD_CHUNK = 200


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
    ttl_days: int = 30
    delay_seconds: float = 0.0

    @classmethod
    def from_yaml(cls, path: str = "config.yaml") -> "ProcessorConfig":
        try:
            with open(path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            return cls(
                min_markup=config.get("price_threshold", {}).get("min_markup", 0.0),
                max_markup=config.get("price_threshold", {}).get("max_markup", 0.50),
                min_buyers=config.get("sales_threshold", {}).get("min_buyers", 0),
                ttl_days=config.get("cache", {}).get("ttl_days", 30),
                delay_seconds=float(
                    config.get("rate_limit", {}).get("delay_between_requests", 0)
                ),
            )
        except FileNotFoundError:
            return cls()


class ProductProcessor:
    """Glowny procesor do sprawdzania produktow na Allegro."""

    def __init__(
        self,
        config: Optional[ProcessorConfig] = None,
        data_fetcher: Optional[Callable] = None,
        search_mode: str = "code",
    ):
        self.search_mode = search_mode if search_mode in ("code", "name") else "code"
        self.config = config or ProcessorConfig.from_yaml()
        self.cache = ProductCache()
        self.data_fetcher = data_fetcher  # funkcja do pobierania danych z Allegro

        self._running = False
        self._paused = False
        self._current_index = 0
        self._results: List[ProductResult] = []
        self._progress_callback: Optional[Callable] = None
        self._state_lock = threading.Lock()

    def load_input_csv(self, path: str) -> List[InputProduct]:
        """Wczytuje liste produktow z CSV."""
        products = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                ean = (
                    row.get("Kod produktu")
                    or row.get("ean")
                    or row.get("EAN")
                    or row.get("kod")
                    or row.get("code")
                    or ""
                )
                price = (
                    row.get("brutto")
                    or row.get("cena")
                    or row.get("price")
                    or row.get("my_price")
                    or "0"
                )
                name = row.get("nazwa") or row.get("name") or ""

                try:
                    price_float = float(str(price).replace(",", ".").replace(" ", ""))
                except ValueError:
                    price_float = 0.0

                if ean:
                    products.append(
                        InputProduct(
                            ean=ean.strip(),
                            my_price=price_float,
                            name=name.strip() if name else None,
                        )
                    )
        return products

    def _should_stop(self) -> bool:
        if not self._running:
            return True
        if is_stop_requested():
            self._running = False
            return True
        return False

    def _is_paused(self) -> bool:
        return self._paused or is_pause_requested()

    def _save_partial(self) -> Optional[str]:
        """Strumieniowy zapis partial — bez budowania drugiej kopii listy w RAM."""
        if not any(r is not None for r in self._results):
            return None
        path = partial_results_path(self.search_mode)
        stream_save_product_dicts(self._results, path)
        return str(path)

    def _save_final(self) -> Optional[str]:
        if not any(r is not None for r in self._results):
            return None
        ensure_output_dir()
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        suffix = search_mode_suffix(self.search_mode)
        path = OUTPUT_DIR / f"results_{stamp}{suffix}.json"
        stream_save_product_dicts(self._results, path)
        return str(path)

    def _update_job_status(
        self,
        *,
        progress: int,
        total: int,
        cache_hits: int,
        scraped: int,
        current_ean: Optional[str] = None,
        error: Optional[str] = None,
        running: Optional[bool] = None,
        paused: Optional[bool] = None,
        phase: Optional[str] = None,
        final_path: Optional[str] = None,
    ) -> None:
        fields: Dict[str, Any] = {
            "progress": progress,
            "total": total,
            "cache_hits": cache_hits,
            "scraped": scraped,
            "current_ean": current_ean,
            "search_mode": self.search_mode,
            "partial_path": str(partial_results_path(self.search_mode)),
            "pid": os.getpid(),
        }
        if running is not None:
            fields["running"] = running
        if paused is not None:
            fields["paused"] = paused
        if error is not None:
            fields["error"] = error
        if phase is not None:
            fields["phase"] = phase
        if final_path is not None:
            fields["final_path"] = final_path
        write_status(**fields)

    def _emit_progress(
        self,
        callback: Optional[Callable],
        current: int,
        total: int,
        result: ProductResult,
    ) -> None:
        if callback:
            callback(current, total, result)

    def _maybe_partial_save(self, *, scraped: int = 0, force: bool = False) -> None:
        """Partial tylko na force albo co N nowo zescrapowanych (nie przy samym cache)."""
        if force or (scraped > 0 and scraped % PARTIAL_SAVE_EVERY_SCRAPED == 0):
            self._save_partial()

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

    def _cache_key_and_query(self, product: InputProduct) -> Tuple[str, Optional[str]]:
        if self.search_mode == "name":
            query = build_search_query(product.name)
            return f"name::{normalize(query)}", query
        return product.ean, product.ean

    def _result_from_cached(
        self, product: InputProduct, query: str, cached: Dict[str, Any]
    ) -> ProductResult:
        field_names = set(ProductResult.__dataclass_fields__.keys())
        data = {k: v for k, v in cached.items() if k in field_names}
        data["from_cache"] = True
        data["name"] = product.name or data.get("name")
        data["my_price"] = product.my_price
        data["ean"] = product.ean
        data["search_mode"] = self.search_mode
        data["search_query"] = query
        return ProductResult(**data)

    def resolve_from_cache_bulk(
        self, products: List[InputProduct]
    ) -> Tuple[List[Tuple[int, ProductResult]], List[Tuple[int, InputProduct]]]:
        """
        Rozdziela listę na trafienia cache i braki.
        Zwraca (hits z indeksem, misses z indeksem) — kolejność oryginalna zachowana w indeksach.
        """
        keyed: List[Tuple[int, InputProduct, str, Optional[str]]] = []
        for i, product in enumerate(products):
            cache_key, query = self._cache_key_and_query(product)
            keyed.append((i, product, cache_key, query))

        cached_map = self.cache.get_many_if_valid(
            [k for _, _, k, q in keyed if q],
            self.config.ttl_days,
        )

        hits: List[Tuple[int, ProductResult]] = []
        misses: List[Tuple[int, InputProduct]] = []
        for i, product, cache_key, query in keyed:
            if not query:
                result = ProductResult(
                    ean=product.ean,
                    my_price=product.my_price,
                    name=product.name,
                    checked_at=datetime.now().isoformat(),
                    search_mode=self.search_mode,
                    status="error",
                    error_message="Brak nazwy produktu do wyszukania",
                )
                hits.append((i, result))
                continue
            cached = cached_map.get(cache_key)
            if cached:
                hits.append((i, self._result_from_cached(product, query, cached)))
            else:
                misses.append((i, product))
        return hits, misses

    def process_single(self, product: InputProduct, *, skip_cache: bool = False) -> ProductResult:
        """Przetwarza pojedynczy produkt."""
        result = ProductResult(
            ean=product.ean,
            my_price=product.my_price,
            name=product.name,
            checked_at=datetime.now().isoformat(),
            search_mode=self.search_mode,
        )

        cache_key, query = self._cache_key_and_query(product)
        result.search_query = query

        if not query:
            result.status = "error"
            result.error_message = "Brak nazwy produktu do wyszukania"
            return result

        if not skip_cache:
            cached = self.cache.get_if_valid(cache_key, self.config.ttl_days)
            if cached:
                return self._result_from_cached(product, query, cached)

        if not self.data_fetcher:
            result.status = "error"
            result.error_message = "Brak skonfigurowanego fetchera danych"
            return result

        try:
            offers_data = self.data_fetcher(query)

            if not offers_data:
                result.status = "checked"
                result.found_on_allegro = False
                self.cache.set(cache_key, result.to_dict())
                return result

            result.found_on_allegro = True
            result.offers = [AllegroOffer(**o) for o in offers_data]

            for offer in result.offers:
                price_ok = self.check_price_match(product.my_price, offer.price)
                sales_ok = self.check_sales(offer.buyers_count)
                if price_ok and sales_ok:
                    result.matching_offers.append(offer)

            if result.matching_offers:
                result.best_match = max(
                    result.matching_offers,
                    key=lambda o: o.buyers_count or 0,
                )

            result.status = "checked"
            self.cache.set(cache_key, result.to_dict())

        except Exception as e:
            result.status = "error"
            result.error_message = str(e)

        return result

    def _resolve_cache_chunked(
        self,
        products: List[InputProduct],
        progress_callback: Optional[Callable],
    ) -> Tuple[int, int, List[Tuple[int, InputProduct]]]:
        """
        Hit/miss bez ładowania całych JSON, potem hity chunkami po CACHE_LOAD_CHUNK.
        Zwraca (done, cache_hits, misses).
        """
        total = len(products)
        keyed: List[Tuple[int, InputProduct, str, Optional[str]]] = []
        for i, product in enumerate(products):
            cache_key, query = self._cache_key_and_query(product)
            keyed.append((i, product, cache_key, query))

        self._update_job_status(
            progress=0,
            total=total,
            cache_hits=0,
            scraped=0,
            running=True,
            phase="cache_lookup",
        )
        valid_keys = self.cache.get_valid_keys(
            [k for _, _, k, q in keyed if q],
            self.config.ttl_days,
        )

        misses: List[Tuple[int, InputProduct]] = []
        hit_jobs: List[Tuple[int, InputProduct, str, str]] = []
        done = 0
        last_result: Optional[ProductResult] = None

        for i, product, cache_key, query in keyed:
            if not query:
                result = ProductResult(
                    ean=product.ean,
                    my_price=product.my_price,
                    name=product.name,
                    checked_at=datetime.now().isoformat(),
                    search_mode=self.search_mode,
                    status="error",
                    error_message="Brak nazwy produktu do wyszukania",
                )
                self._results[i] = result
                done += 1
                last_result = result
                continue
            if cache_key in valid_keys:
                hit_jobs.append((i, product, cache_key, query))
            else:
                misses.append((i, product))

        self._update_job_status(
            progress=done,
            total=total,
            cache_hits=0,
            scraped=0,
            running=True,
            phase="cache_apply",
        )

        cache_hits = 0
        for start in range(0, len(hit_jobs), CACHE_LOAD_CHUNK):
            if self._should_stop():
                break
            chunk = hit_jobs[start : start + CACHE_LOAD_CHUNK]
            cached_map = self.cache.get_many_if_valid(
                [ck for _, _, ck, _ in chunk],
                self.config.ttl_days,
            )
            for i, product, cache_key, query in chunk:
                if self._should_stop():
                    break
                cached = cached_map.get(cache_key)
                if not cached:
                    misses.append((i, product))
                    continue
                result = self._result_from_cached(product, query, cached)
                self._results[i] = result
                done += 1
                cache_hits += 1
                last_result = result
                self._current_index = done
                if done % CACHE_PROGRESS_EVERY == 0:
                    self._emit_progress(progress_callback, done, total, result)
                    self._update_job_status(
                        progress=done,
                        total=total,
                        cache_hits=cache_hits,
                        scraped=0,
                        current_ean=result.ean,
                        running=True,
                        phase="cache_apply",
                    )
            del cached_map

        if last_result is not None:
            self._emit_progress(progress_callback, done, total, last_result)
            self._update_job_status(
                progress=done,
                total=total,
                cache_hits=cache_hits,
                scraped=0,
                current_ean=last_result.ean,
                running=True,
                phase="cache_apply",
            )
            self._maybe_partial_save(force=True)

        return done, cache_hits, misses

    def _finish_job_status(
        self,
        *,
        done: int,
        total: int,
        cache_hits: int,
        scraped: int,
        error: Optional[str] = None,
    ) -> Optional[str]:
        """Partial + final JSON (stream) z wątku scrapu; zwraca ścieżkę finalną."""
        self._maybe_partial_save(force=True)
        final_path = self._save_final()
        self._update_job_status(
            progress=done,
            total=total,
            cache_hits=cache_hits,
            scraped=scraped,
            running=False,
            paused=False,
            phase="done",
            final_path=final_path,
            error=error,
        )
        write_status(stop_requested=False)
        return final_path

    def process_batch(
        self,
        products: List[InputProduct],
        progress_callback: Optional[Callable] = None,
        max_workers: int = 1,
    ) -> List[ProductResult]:
        """Przetwarza liste produktow (opcjonalnie równolegle)."""
        if max_workers and max_workers > 1:
            return self.process_batch_parallel(
                products,
                max_workers=max_workers,
                progress_callback=progress_callback,
            )

        total = len(products)
        self._running = True
        self._paused = False
        self._results = [None] * total  # type: ignore
        self._progress_callback = progress_callback
        write_status(
            running=True,
            paused=False,
            stop_requested=False,
            progress=0,
            total=total,
            cache_hits=0,
            scraped=0,
            current_ean=None,
            search_mode=self.search_mode,
            partial_path=str(partial_results_path(self.search_mode)),
            final_path=None,
            phase="cache_lookup",
            started_at=datetime.now().isoformat(),
            error=None,
            pid=os.getpid(),
        )

        cache_hits = 0
        scraped = 0
        done = 0
        try:
            done, cache_hits, misses = self._resolve_cache_chunked(
                products, progress_callback
            )

            if misses and not self._should_stop():
                self._update_job_status(
                    progress=done,
                    total=total,
                    cache_hits=cache_hits,
                    scraped=0,
                    running=True,
                    phase="scrape",
                )

            for i, product in misses:
                if self._should_stop():
                    break

                while self._is_paused():
                    self._update_job_status(
                        progress=done,
                        total=total,
                        cache_hits=cache_hits,
                        scraped=scraped,
                        current_ean=product.ean,
                        running=True,
                        paused=True,
                        phase="scrape",
                    )
                    time.sleep(0.5)
                    if self._should_stop():
                        break

                if self._should_stop():
                    break

                result = self.process_single(product, skip_cache=True)
                self._results[i] = result
                done += 1
                scraped += 1
                self._current_index = done
                self._emit_progress(progress_callback, done, total, result)
                if scraped % 10 == 0 or done == total:
                    self._update_job_status(
                        progress=done,
                        total=total,
                        cache_hits=cache_hits,
                        scraped=scraped,
                        current_ean=result.ean,
                        running=True,
                        paused=False,
                        phase="scrape",
                    )
                self._maybe_partial_save(scraped=scraped)

                delay = float(self.config.delay_seconds or 0)
                if delay > 0 and done < total:
                    time.sleep(delay)

            self._finish_job_status(
                done=done,
                total=total,
                cache_hits=cache_hits,
                scraped=scraped,
            )
        except Exception as exc:
            self._finish_job_status(
                done=done,
                total=total,
                cache_hits=cache_hits,
                scraped=scraped,
                error=str(exc),
            )
            raise
        finally:
            self._running = False

        return [r for r in self._results if r is not None]

    def process_batch_parallel(
        self,
        products: List[InputProduct],
        max_workers: int = 5,
        progress_callback: Optional[Callable] = None,
    ) -> List[ProductResult]:
        """
        Przetwarza listę: najpierw bulk cache, potem braki w ThreadPool.
        max_workers powinien być <= ConcurrentRequest z scrape.do.
        """
        workers = max(1, int(max_workers or 1))
        total = len(products)
        self._running = True
        self._paused = False
        self._results = [None] * total  # type: ignore
        self._progress_callback = progress_callback
        done_lock = threading.Lock()

        write_status(
            running=True,
            paused=False,
            stop_requested=False,
            progress=0,
            total=total,
            cache_hits=0,
            scraped=0,
            current_ean=None,
            search_mode=self.search_mode,
            partial_path=str(partial_results_path(self.search_mode)),
            final_path=None,
            phase="cache_lookup",
            started_at=datetime.now().isoformat(),
            error=None,
            pid=os.getpid(),
        )

        cache_hits = 0
        scraped = 0
        done = 0

        try:
            done, cache_hits, misses = self._resolve_cache_chunked(
                products, progress_callback
            )

            def _work(item: Tuple[int, InputProduct]) -> Tuple[int, ProductResult]:
                idx, product = item
                while self._is_paused() and not self._should_stop():
                    time.sleep(0.2)
                if self._should_stop():
                    return idx, ProductResult(
                        ean=product.ean,
                        my_price=product.my_price,
                        name=product.name,
                        checked_at=datetime.now().isoformat(),
                        search_mode=self.search_mode,
                        status="error",
                        error_message="Zatrzymano",
                    )
                return idx, self.process_single(product, skip_cache=True)

            if misses and not self._should_stop():
                self._update_job_status(
                    progress=done,
                    total=total,
                    cache_hits=cache_hits,
                    scraped=0,
                    running=True,
                    phase="scrape",
                )
                with ThreadPoolExecutor(max_workers=workers) as executor:
                    futures = {executor.submit(_work, item): item[0] for item in misses}
                    for future in as_completed(futures):
                        if self._should_stop():
                            for f in futures:
                                f.cancel()
                            break
                        idx, result = future.result()
                        self._results[idx] = result
                        with done_lock:
                            done += 1
                            scraped += 1
                            self._current_index = done
                            current_done = done
                            current_scraped = scraped
                        self._emit_progress(
                            progress_callback, current_done, total, result
                        )
                        if current_scraped % 10 == 0 or current_done >= total:
                            self._update_job_status(
                                progress=current_done,
                                total=total,
                                cache_hits=cache_hits,
                                scraped=current_scraped,
                                current_ean=result.ean,
                                running=True,
                                paused=False,
                                phase="scrape",
                            )
                        self._maybe_partial_save(scraped=current_scraped)

            self._finish_job_status(
                done=done,
                total=total,
                cache_hits=cache_hits,
                scraped=scraped,
            )
        except Exception as exc:
            self._finish_job_status(
                done=done,
                total=total,
                cache_hits=cache_hits,
                scraped=scraped,
                error=str(exc),
            )
            raise
        finally:
            self._running = False

        return [r for r in self._results if r is not None]

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
            "products": [r.to_dict() for r in results],
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
            writer.writerow(
                [
                    "Kod",
                    "Moja cena",
                    "Nazwa",
                    "Znaleziono",
                    "Najlepsza oferta - cena",
                    "Najlepsza oferta - kupilo osob",
                    "Najlepsza oferta - URL",
                    "Status",
                ]
            )

            for r in results:
                best = r.best_match
                writer.writerow(
                    [
                        r.ean,
                        r.my_price,
                        r.name or "",
                        "Tak" if r.found_on_allegro else "Nie",
                        best.price if best else "",
                        best.buyers_count if best else "",
                        best.url if best else "",
                        r.status,
                    ]
                )
