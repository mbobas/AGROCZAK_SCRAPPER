# Duże joby + cache — problem, objawy, co zawiodło

Skrót dla kolejnego agenta. Kontekst: Streamlit dashboard (`src/gui/dashboard.py`) + scrap Allegro przez scrape.do, cache SQLite (`data/cache.db`).

## Objawy

- UI „zamraża się” na postępie równym liczbie hitów cache (np. 456/5000), a w tle cache/logi dalej rosną.
- Po kliknięciu **Start** na dużym zakresie (np. 1–10 100 przy ~10k w cache) Streamlit **umiera**: przeglądarka `ERR_CONNECTION_REFUSED` na `/_stcore/health`, w terminalu `Stopping...`.
- `data/job_status.json` zostaje z `running: true`, `phase: "cache_lookup"`, `progress: 0`.
- Kredyty scrape.do się nie ruszają (job pada zanim dojdzie do missów albo UI nie polluje).
- Szum w konsoli (Grammarly, `toLowerCase`, sandbox `about:srcdoc`) — **nie** jest przyczyną; to skutek padniętego serwera / rozszerzeń.

## Root cause (ustalone)

1. **Faza cache przy dużym N** ładowała prawie cały cache do RAM naraz (`get_many_if_valid` na ~10k kluczy ≈ 50 MB JSON → setki MB obiektów Pythona w tym samym procesie co Streamlit) → OOM / zabicie procesu.
2. **Kolejka UI** dostawała pełne `result.to_dict()` dla każdego hitu → lawina eventów, ciężki `session_state`, pad websocketu; wątek scrapu żył dalej (daemon).
3. **Autozapis JSON tylko na `done` w żywej sesji Streamlit** — po zerwaniu UI finalny plik nie powstawał (cache i tak rósł).
4. **Partial co 100 podczas fazy cache** (rosnący dump całej listy × dziesiątki razy) + **wczytywanie partial do `session_state` w trakcie joba** dobijało RAM/dysk.

Typowy rozmiar: cache ~10k wpisów ≈ 50 MB raw JSON; pełny `results_*.json` ≈ 40–50 MB.

## Podejścia, które zawiodły / były niewystarczające

| Podejście | Dlaczego słabo |
|-----------|----------------|
| Zostawić job w tle przy „zamarzniętym” pasku | Działa scrap/cache, ale UI i autozapis JSON giną po `ConnectionReset` / refreshu. |
| Samo `job_status.json` + poll UI bez zmiany ładowania cache | Status zostawał na `cache_lookup` / `progress: 0`, bo proces padał w trakcie bulk-load. |
| Partial co 100 ukończonych (także w fazie cache) | Przy 10k hitach setki coraz większych zapisów JSON → zabicie dysku/RAM. |
| Ładowanie `results_partial_*.json` do sesji Streamlit w trakcie joba | Przy dużym pliku UI pada mimo że worker żyje. |
| Finalny `json.dumps(cała_lista)` w pamięci | Dublowanie RAM przy domykaniu joba ~10k. |
| Szukanie błędu w logach Grammarly / `toLowerCase` | Fałszywy trop; serwer już nie działa. |
| Samo odświeżenie przeglądarki „żeby wznowić pasek” | `session_state` i kolejka giną; bez statusu na dysku / żywego wątku nie ma reconnectu. |

## Podejście, które działa (stan kodu)

Pliki kluczowe: `src/core/cache.py`, `src/core/processor.py`, `src/core/job_state.py`, `src/core/results_io.py`, `src/gui/dashboard.py`.

1. **Hit/miss bez payloadu** — `ProductCache.get_valid_keys()` (tylko `ean` + `checked_at`).
2. **Dociąganie hitów chunkami** (`CACHE_LOAD_CHUNK = 200`) w `_resolve_cache_chunked`.
3. **Lekkie eventy na kolejce** (`type=progress`, bez pełnych ofert).
4. **Partial**: raz po fazie cache; w trakcie scrape co ~500 nowych; zapis **strumieniowy** (`stream_save_product_dicts`).
5. **Final JSON z wątku scrapu** (nie z UI); UI pokazuje ścieżkę, nie ładuje 10k do sesji.
6. **`data/job_status.json`**: `phase` (`cache_lookup` / `cache_apply` / `scrape` / `done`), progress, `final_path`; po refresh UI może pokazać job + Stop przez `stop_requested`.
7. Martwy status po restarcie Streamlit: `is_stale_running()` (PID) → clear.

## Operacyjnie

- Po padnięciu procesu: wyczyść / reconciluj `data/job_status.json` zanim odpalisz kolejny Start.
- Duże wyniki oglądaj w **Analiza wyników** / pliku z `data/output/`, nie w tabeli zakładki Scrapowanie.
- Logi konsoli przeglądarki (Grammarly, sandbox) ignoruj przy diagnozie crasha — patrz terminal Streamlit + `job_status.json` + rozmiar cache.

## Smoke (szybki check)

```text
# ~pełny cache z dysku, bez sieci (fetcher zwraca [])
ProductProcessor.process_batch(produkty_z_cache, max_workers=1)
# oczekiwane: phase→done, final_path istnieje, proces nie pada
```

Legenda CSV (osobna kosmetyka): plik Agroczak to `Kod produktu;nazwa;brutto` (GUI mapuje też `ean;cena;nazwa`).
