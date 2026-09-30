Allegro
REST API
Szukaj w Allegro REST API
mbobas


Jak zacząćJak zacząć
PoradnikiPoradniki
FAQ
Co nowegoCo nowego
Dokumentacja
Regulamin
Kontakt
Zarządzaj APIZarządzaj API
Allegro REST API
Informacje podstawowe
REST API
Metody HTTP
Protokół komunikacyjny
Reprezentacja danych (JSON)
Dostęp do API
User-Agent
Uwierzytelnianie i autoryzacja
Parametry
Wersjonowanie zasobów
Metody w wersji beta
Wersja językowa
Statusy HTTP
Obsługa błędów
Stronicowanie
Filtrowanie
Sortowanie
Data i czas
Cena i waluta
Identyfikatory zasobów
Ograniczenie liczby zapytań (limity)
Środowisko testowe
Środowisko testowe - regulamin
Informacje podstawowe

Co musisz wiedzieć, żeby rozpocząć pracę z REST API Allegro.

Informacje podstawowe
Co musisz wiedzieć, żeby rozpocząć pracę z REST API Allegro.

REST API
Platforma Allegro udostępnia klientom funkcjonalności w ramach API w oparciu o architekturę REST. Wykorzystuje do tego celu protokół HTTP wraz z jego metodami: GET, POST, PUT, PATCH, DELETE. Elementy platformy Allegro zostały podzielone na zasoby np. /sale/offers, /sale/categories, /order/checkout-forms, itd. Dostęp do poszczególnych zasobów następuje poprzez wywołanie wybranej metody HTTP na adres: https://api.allegro.pl, dodając ścieżkę do wybranego zasobu.

Przykładowe pobranie informacji o kategorii Allegro z identyfikatorem 2:

 GET https://api.allegro.pl/sale/categories/2
Jeśli chcemy pobrać więcej niż jeden zasób, pomijamy w ścieżce identyfikator. Przykładowe pobranie listy kategorii Allegro:

 GET https://api.allegro.pl/sale/categories

Jeśli chcesz pobrać całą dokumentację zasobów w formie swagger.yaml kliknij tutaj.

Metody HTTP
Każdy z zasobów API korzystać może z następujących metod HTTP:

GET: Wykorzystywana do pobierania danych. Wszystkie metody GET mogą być wołane wielokrotnie, gdyż nie modyfikują żadnych zasobów Allegro.
POST: Wykorzystywana do utworzenia nowego zasobu (np. utworzenie nowej oferty tworzy zasób typu /sale/product-offers). Dwukrotne wywołanie metody POST na zasobie /sale/product-offers spowoduje stworzenie dwóch ofert na Allegro.
PUT: Wykorzystywana do edycji zasobu (np. edycja liczby sztuk w ofertach). Dwukrotne wywołanie metody PUT na tym samym zasobie jest bezpieczne.
PATCH: Wykorzystywana do częściowej edycji zasobu (np. edycja ceny, bez konieczności przesyłania całego modelu oferty).
DELETE: Wykorzystywana do usuwania zasobów (np. usunięcie draftu oferty).
Protokół komunikacyjny
Dostęp do REST API odbywa się poprzez połączenie HTTPS do serwera api.allegro.pl. Wszystkie dane, wysyłane i odbierane z serwera są w formacie JSON.

 $ curl -i https://api.allegro.pl

 HTTP/1.1 404 Not Found
 Connection: keep-alive
 Trace-Id: 2bc7afc1740c86f7
 Content-Type: application/json; charset=utf-8
 Content-Length: 165
 Date: Tue, 08 Sep 2015 07:59:45 GMT
 X-Frame-Options: SAMEORIGIN

 {"errors":[{"code":"NotFoundException","message":"Not found","details":null,"path":null,"userMessage":"Funkcja niedostępna. Skontaktuj się z autorem aplikacji."}]}
Każda odpowiedź zawiera m.in. nagłówek Trace-Id, którego wartość jednoznacznie identyfikuje zapytanie HTTP klienta. W przypadku zgłaszania problemu z zapytaniem HTTP należy przekazać wartość Trace-Id w zgłoszeniu.

Reprezentacja danych (JSON)
Wszystkie dane wysyłane są i odbierane z API w formacie JSON. Podstawowym elementem tego formatu jest pole, którego nazwa jest oddzielona od wartości pola dwukropkiem. Pola rozdziela przecinek. Kolejnym elementem jest obiekt JSON, zawierający się w nawiasach klamrowych. Tablice w formacie JSON są zapisywane z wykorzystaniem nawiasów kwadratowych. Puste pola (z wartością null) są każdorazowo załączane do odpowiedzi - nie są ukrywane.

 {
  "offers": [
    {
      "id": "123",
      "title": "test"
    },
    {
      "id": "456",
      "title": null
    }
  ]
 }
Dostęp do API
Dostęp do API uzyskasz po zarejestrowaniu swojej aplikacji.

User-Agent
Zgodnie z art. 3.4(c) Regulaminu REST API, udzielenie autoryzacji na rzecz Oprogramowania REST API wymaga zastosowania rozwiązań technicznych pozwalających na wiarygodną i jednoznaczną identyfikację Twojej aplikacji.

Dlatego zanim zaczniesz korzystać z Allegro API, musisz skonfigurować własny identyfikator User-Agent.

Co to jest User-Agent?

W kontekście API, User-Agent to nagłówek HTTP, który jest przesyłany przez klienta (aplikację wysyłającą żądanie) do serwera. Nagłówek User-Agent służy aplikacjom zewnętrznym do rozpoznania typu programu klienckiego.

Dlaczego wymagamy implementacji własnego identyfikatora User-Agent?

Chcemy umożliwić naszym systemom monitorującym:

precyzyjną identyfikację źródła ruchu,
ścieżkę kontaktu z właścicielem aplikacji bezpośrednio na poziomie analizy logów serwerowych, co minimalizuje ryzyko prewencyjnego blokowania adresu IP aplikacji w przypadku wykrycia niestandardowej aktywności.
Co musisz zrobić?

Skonfiguruj identyfikator User-Agent zgodnie z poniższą strukturą:

Identyfikacja aplikacji: Pierwszy człon musi zawierać unikalną nazwę systemu/aplikacji oraz aktualną wersję produkcyjną (np. TestApplication/1.1.0). Nazwa musi być spójna z nazwą zarejestrowanej aplikacji.
Adres URL: Musisz wskazać dedykowaną stronę informacyjną lub repozytorium, gdzie administratorzy zewnętrzni mogą zapoznać się z celem działania aplikacji (np. +https://firma.com/TestApplication-info).
Przykładowa struktura identyfikatora User-Agent:

NazwaAplikacji/Wersja (+AdresURL_Dokumentacji)
Prawidłowo skonfigurowany nagłówek powinien przyjąć postać:

TestApplication/1.1.0 (+https://firma.com/TestApplication-info)
Jak mogę sprawdzić poprawność nagłówka user-agent?

Skorzystaj z naszego narzędzia do generowania oraz sprawdzania poprawności nagłówka User-Agent. Znajdziesz je na stronie: https://apps.developer.allegro.pl/user-agent.


Ważne! Nie modyfikuj zawartości nagłówka User-Agent (nie dotyczy wersji oprogramowania), ponieważ będzie on używany jako czynnik umieszczania na białej liście.

Uwierzytelnianie i autoryzacja
Wszystkie żądania zasobów REST API wymagają przekazania tokena OAuth w nagłówku Authorization. Więcej o autoryzacji za pomocą OAuth przeczytasz w dedykowanym temu tematowi artykule.

Parametry
Wiele metod API może przyjmować opcjonalne parametry. Zapytania HTTP typu GET przyjmują parametry, które są umieszczone w adresie zasobu, którego dotyczy zapytanie. Jeśli nazwa parametru odpowiada polu wewnątrz obiektu, części tej nazwy są rozdzielone kropkami:

 https://api.allegro.pl/sale/offers?product.id.empty=true
Pozostałe typy zapytań HTTP, takie jak POST i PUT, mają parametry umieszczone w treści zapytania, a nie w adresie:

curl -X POST
  'https://api.allegro.pl/sale/product-offers'
  -H 'Authorization: Bearer {token}'
  -H 'Accept: application/vnd.allegro.public.v1+json'
  -H 'Content-Type: application/vnd.allegro.public.v1+json'
  -d '{
  "productSet": [{
    "product": {
      "id": "5902719471797",        
      "idType": "GTIN"
    }}],
    "sellingMode": {
      "price": {
        "amount": "220.85",    
        "currency": "PLN"
      }
    },
    "stock": {
      "available": 10               
    },
     "publication": {
      "status": "INACTIVE"
    }
  }'
Zapytania typu DELETE nie przyjmują parametrów umieszczonych w treści, jednak może się zdarzyć, że przyjmą parametry w adresie zasobu.

Wersjonowanie zasobów
Metody REST mogą być wersjonowane. Wywołując metodę należy podać numer wersji zasobu (można go podejrzeć w dokumentacji metody).

Wersję metody wybieramy przez ustawienie np. _v1_ w nagłowkach Accept lub Content-Type:

 application/vnd.allegro.public.v1+json
Wyjątkiem są metody DELETE oraz end-point OAuth (https://allegro.pl/auth), które nie są wersjonowane.

Metody w wersji beta
Metody w wersji beta to zasoby, nad którymi jeszcze pracujemy. Mogą one nie realizować pełnej funkcjonalności, często być zmieniane oraz łamać kompatybilność wsteczną.

Wersja beta metody oznaczona jest podobnie do wersji produkcyjnej. Jedyną różnicą jest to, że w nazwie typu danych znajduje się słowo beta:

 application/vnd.allegro.beta.v1+json
Zasoby w tej wersji są odpowiednio oznaczone w dokumentacji.

Przykład wywołania zasobu w wersji pierwszej, stabilnej:

 https://api.allegro.pl/sale/delivery-methods \
 -H 'Authorization: Bearer {token}' \
 -H 'accept: application/vnd.allegro.beta.v1+json'
Przykład wywołania zasobu w wersji drugiej, beta:

 https://api.allegro.pl/sale/delivery-methods \
 -H 'Authorization: Bearer {token}' \
 -H 'accept: application/vnd.allegro.beta.v2+json'
Wersja językowa
Jeżeli chcesz być pewny, że wszystkie teksty zwracane będą w języku polskim, wysyłaj z każdym żądaniem nagłówek:

 Accept-Language: pl-PL
Natomiast jeżeli preferujesz język angielski, wysyłaj nagłówek:

 Accept-Language: en-US

W zależności od zasobów w Allegro API, obsługujemy również wartości: cs-CZ, sk-SK, hu-HU i uk-UA.

Statusy HTTP
Każde żądanie do API zwraca status HTTP informujący o wyniku przetwarzania. Poniższa lista zawiera najczęściej używane statusy:

200 OK: Zwracany w przypadku powodzenia metody GET i PUT.
201 Created: Potwierdza utworzenie dokumentu za pomocą metody POST.
202 Accepted: Określa, że żądanie zostało zaakceptowane przez serwer, ale jego przetwarzanie jeszcze się nie zakończyło (dotyczy przetwarzania asynchronicznego).
204 No Content: Zwracany przy powodzeniu operacji, kiedy żądanie nie zwraca żadnych danych (np. metoda DELETE).
304 Not Modified: Oznacza brak zmian w żądaniu HTTP - brak przekierowania.
400 Bad Request: Wysłano niepoprawne dane JSON.
401 Unauthorized: Użytkownik nie jest uwierzytelniony z powodu nieprawidłowego lub brakującego tokenu.
403 Forbidden: Użytkownik jest uwierzytelniony, ale nie ma praw do danego zasobu.
404 Not Found: Odpytywany zasób nie istnieje w API.
406 Not Acceptable: W nagłówku Accept przekazany został nieobsługiwany przez zasób typ danych lub wskazano nieprawidłową wersję zasobu.
415 Unsupported Media Type: W nagłówku Accept przekazany został nieobsługiwany przez zasób typ danych.
422 Unprocessable Entity: Wysłano niepoprawne wartości pól, np. walidacja obiektu zwróciła błąd, albo któreś z pól nie spełnia kryteriów nałożonych na nie przez zasób.
429 Too Many Requests: Klient przekroczył limit liczby żądań.
503 Service Unavailable: Połączenie z serwisem nie jest możliwe.
Obsługa błędów
Każde błędne wywołanie API jest sygnalizowanie statusem odpowiedzi HTTP większym lub równym 400 oraz treścią odpowiedzi. Wyróżniamy dwa możliwe formaty błędów.

Pierwszy z nich wystąpi w przypadku wszelkich problemów z żądaniem. Zawiera on tablicę błędów errors, opisującą przyczynę problemu:

 {
    "errors": [
        {
            "code": "NotAcceptableException",
            "message": "An error has occurred",
            "details": null,
            "path": null,
            "userMessage": "Żądanie zawiera błędne dane. Skontaktuj się z autorem aplikacji."
            "metadata": {}
        }
    ]
 } 
Błędy w tym formacie opisane są następującymi polami:

message: Wewnętrzna informacja o błędzie dla programisty. Ułatwia zlokalizowanie przyczyny problemu.
code: Kod błędu reprezentowany jako string. Na jego podstawie aplikacja może zdecydować, czy błąd wymaga specjalnej obsługi (np. pokazania dialogu CAPTCHA przy błędnym podaniu hasła logowania).
userMessage: Informacja o błędzie przyjazna dla użytkownika aplikacji, w większości przypadków obsługa błędu będzie polegać na pokazaniu użytkownikowi komunikatu z tego pola.
path: Ścieżka do pola zawierającego błąd (pojawia się dla błędów walidacji pól i parametrów).
details: Szczegóły błędu (jeśli są dostępne).
Drugi format jest ściśle powiązany z uwierzytelnianiem według standardu OAuth2. Może wystąpić np. kiedy spróbujesz pobrać zasób bez tokenu dostępowego. Więcej informacji na temat standardu OAuth2 znajdziesz w naszym poradniku oraz w specyfikacji OAuth2 definiującej poniższy format błędu.

 {
        "error": "unauthorized",
        "error_description": "Full authentication is required to access this resource"
 }
Powyższe pola oznaczają:

error: Kod błędu ze specyfikacji OAuth2.
error_description: Dodatkowe informacje opisujące błąd w języku naturalnym.

Ten format odpowiedzi występuje wyłącznie w przypadku błędów 401 Unauthorized.

Stronicowanie
Do pobrania konkretnej strony listy wynikowej służą parametry:

offset: Określa numer porcji zwracanych danych i jest numerowany od 0.
limit: Określa liczbę elementów na stronie, nie może być większy niż maksymalny limit obsługiwany przez zasób.
page.id: Określa ID strony z kolejnymi wynikami w przypadku paginacji opartej na kursorze.
Przykład pobrania pierwszej paczki ofert:

 GET /sale/offers?limit=100&offset=0
Przykład pobrania kolejnej paczki ofert:

 GET /sale/offers?limit=100&offset=100
Przykład pobrania kolejnej paczki produktów z paginacją opartą na kursorze:

 GET /sale/products?page.id=MjAyNC0wOS0xMFQwNjo0OTowMi40NTBa
Filtrowanie
Zasoby dostepne w API mogą realizować filtrowanie - polega ono na przekazaniu w parametrach umieszczonych w adresie zasobu nazw pól, które biorą udział w filtrowaniu.

Przykład wyświetlenia listy tylko aktywnych ofert:

 GET /sale/offers?publication.status=ACTIVE
Sortowanie
Aby uruchomić wyszukiwanie z sortowaniem, przy wywołaniu zasobu należy przekazać dodatkowo parametr sort (zakładając, że dany zasób obsługuje sortowanie jego listy wynikowej). Jeżeli wynik sortowania ma zostać odwrócony, nazwę pola należy poprzedzić myślnikiem. Jeśli wynik ma być posortowany po więcej niż jednym polu, w parametrze należy przekazać listę pól rozdzielonych przecinkami.

Przykład pobrania listy ofert uszeregowanych rosnąco według liczby przedmiotów:

 GET /sale/offers?sort=stock.sold
Przykład pobrania listy ofert uszeregowanych malejąco według liczby przedmiotów:

 GET /sale/offers?sort=-stock.sold
Przykład pobrania listy ofert uszeregowanych malejąco według sprzedanej liczby przedmiotów, a następnie rosnąco według dostępnej liczby przedmiotów:

 GET /sale/offers?sort=-stock.sold,stock.available
Data i czas
Wszystkie pola daty i czasu prezentowane są w standardzie ISO 8601:

 YYYY-MM-DDTHH:MM:SSZ
Pomiędzy datą, jaką prezentujemy w Moim Allegro a REST API, występuje różnica 1 (czas zimowy) lub 2 (czas letni) godzin ze względu na różne strefy czasowe:

REST API: +00:00Z - “Czas Zulu”, czas uniwersalny;
Moje Allegro: +01:00 lub +02:00 - lokalna strefa czasowa.

Niektóre pola, np. "handlingTime" lub "duration" wymagają, abyś podał czas w określonej formie - przykładowo: P3D (3 dni); P5D (5 dni); P7D (7 dni). Zanim uzupełnisz strukturę sprawdź w dokumentacji danego zasobu jakie są dostępne wartości w danym polu.

Cena i waluta
Cena i waluta przekazywane i zwracane są w postaci dwóch pól:

amount: Łańcuch znaków (string) wyrażający wartość liczbową – cenę.
currency: Trzyliterowy kod waluty, zgodny ze standardem ISO 4217.
Przykład:

 {
  "buyNowPrice": {
    "amount": "10.23",
    "currency": "PLN"
  }
 }
Identyfikatory zasobów
API zwraca identyfikatory zasobów zawsze w postaci łańcuchów znaków, w większości przypadków w formacie UUID. Zalecamy przechowanie identyfikatorów właśnie w stringach, nawet jeśli API zwróci jako identyfikator liczbę w cudzysłowach, ponieważ w przyszłości może to ulec zmianie.

Przykład:

 "bg645d84-75b4-431b-adb2-eb6b9e546059"

Jeśli korzystasz z takich zasobów, które wymagają {commandId}, jak na przykład zasób do grupowej edycji ofert - PUT /sale/offer-modification-commands/{commandId} w polu commandId wskaż identyfikator pod jakim zapiszemy to polecenie.

CommandId to identyfikator danego requesta, na jego podstawie sprawdzisz stan realizacji twojego żądania. Wykorzystaj do tego odpowiedni zasób, np. GET /sale/offer-modification-commands/{commandId}.

Pamiętaj, aby identyfikator polecenia był unikatowy. Wymagamy identyfikatorów w standardzie UUID.

Więcej na ten temat znajdziesz tutaj.

Ograniczenie liczby zapytań (limity)
W usłudze Allegro REST API (produkcyjnej oraz testowej) obowiązuje główny limit nakładany na Client ID (lub Software Statement ID w przypadku DCR) - 9000 zapytań na minutę.

Gdy przekroczysz limit:

na minutę zablokujemy twój Client ID,
zwrócimy odpowiedź ze statusem: 429 Too Many Requests.
Po upływie wskazanego czasu automatycznie przywrócimy dostęp do usługi dla twojego Client ID.

Dla niektórych zasobów stosujemy dodatkowe, niższe limity liczby żądań. W takich przypadkach informacje o dodatkowym limicie znajdziesz w opisie zasobu w dokumentacji REST API Allegro.

Leaky Bucket
Dla wybranych zasobów REST API stosujemy dodatkowy mechanizm, który ogranicza liczbę zapytań dla danego użytkownika (user.id). Wykorzystujemy algorytm Leaky Bucket. Gdy użytkownik przekroczy dozwoloną liczbę wywołań na minutę (RPM), wydłużamy czas odpowiedzi. W przypadku zbyt dużej liczby równoległych zapytań w imieniu tego samego użytkownika serwer odpowie błędem HTTP: 429 Too Many Requests.

Środowisko testowe
Czym jest Sandbox?
Allegro Sandbox to środowisko testowe. Możesz na nim bezpiecznie testować REST API platformy Allegro. Środowisko odwzorowuje wszystkie najważniejsze funkcje serwisu Allegro - możesz m.in.:

aktywować konto,
wystawić ofertę,
przejść cały proces zakupowy,
korzystać z wyszukiwarki,
wystawić ocenę sprzedawcy.
Dzięki symulatorowi sprawdzisz na nim również szybkie płatności online.

Jak to działa?
Sandbox działa na tej samej zasadzie, co środowisko produkcyjne. Ze środowiska testowego możesz korzystać, tak jak z Allegro.pl:

przez interfejs graficzny (https://allegro.pl.allegrosandbox.pl dla allegro.pl oraz https://allegro.xy.allegrosandbox.pl dla zagranicznych domen serwisu, gdzie "xy" to kod kraju, np. https://allegro.cz.allegrosandbox.pl dla allegro.cz),
przez REST API (za pomocą https://api.allegro.pl.allegrosandbox.pl).
Środowisko testowe udostępniliśmy dla wszystkich. Aby otrzymać stały dostęp do środowiska, przejdź pod jego adres i kliknij w "Załóż konto", a następnie aktywuj je.

Pamiętaj, by podczas aktywacji podać rzeczywiste dane adresowe - czyli taki kod pocztowy, ulicę i miasto, które do siebie pasują, np.:

ulica: Grunwaldzka 182,
kod pocztowy: 60-166,
miasto: Poznań.
W przeciwnym przypadku aktywacja może się nie udać.

Środowisko testowe jest odrębne względem środowiska produkcyjnego.

Różnice między produkcyjnym a testowym REST API:

Produkcja:

Adres wywołania metod - https://api.allegro.pl/
Rejestracja aplikacji - https://apps.developer.allegro.pl/
Adres do autoryzacji - https://allegro.pl/auth/oauth/
Sandbox:

Adres wywołania metod - https://api.allegro.pl.allegrosandbox.pl/
Rejestracja aplikacji - https://apps.developer.allegro.pl.allegrosandbox.pl/
Adres do autoryzacji - https://allegro.pl.allegrosandbox.pl/auth/oauth/

Przestrzegaj zasad, które obowiązują w naszym serwisie testowym.
Pamiętaj o odpytywaniu odpowiedniego adresu wywoływania zasobów.
Na środowisku testowym obowiązują takie same limity liczby zapytań, jak w serwisie produkcyjnym.
Przerwy serwisowe zapowiadamy na stronie z aktualnościami.
Na środowisku testowym usuniemy dodane przez ciebie zdjęcia po 7 dniach.
Raz na kwartał aktualizujemy listę parametrów i kategorii. Usuwamy wtedy wszystkie oferty z Sandboxa.
Powiadomienia e-mail wysłane w ramach serwisu testowego mają tytuł "Message from WebAPI Sandbox environment", a sama treść powiadomienia załączona jest w pliku .eml w wiadomości.
Na środowisku testowym nie musisz włączać dwustopniowego logowania, aby zarejestrować aplikację. Jeśli chciałbyś jednak to zrobić, użyj kodu 123456 - na Sandboxie nie wysyłamy SMS-ów.
Środowisko testowe - regulamin
Zasady korzystania z testowej wersji interfejsu programistycznego Serwisu Allegro
W ramach strony allegro.pl.allegrosandbox.pl masz możliwość nieodpłatnego testowania interfejsu programistycznego Serwisu Allegro (REST API) w ramach jednego środowiska (dalej “Usługa”).
Usługa świadczona jest przez Allegro sp. z o.o. z siedzibą w Poznaniu, przy ul. Wierzbięcice 1B, 61-569 Poznań, wpisana do rejestru przedsiębiorców prowadzonego przez Sąd Rejonowy Poznań - Nowe Miasto i Wilda w Poznaniu, VIII Wydział Gospodarczy Krajowego Rejestru Sądowego pod numerem KRS: 0000635012, kapitał zakładowy: 40 000 000 złotych, posiadająca numer identyfikacji podatkowej NIP 525-26-74-798, REGON 365331553 (dalej “Spółka”).
Rozpoczęcie korzystania przez Ciebie z Usługi jest równoznaczne z akceptacją niniejszych Zasad.
Celem Usługi jest umożliwienie Ci zapoznania się ze sposobem jej świadczenia przez Spółkę.
Spółka informuje, co rozumiesz i akceptujesz, iż dane w ramach Usługi nie podlegają żadnej formie kopii zapasowych.
Spółka ma prawo usunąć wszelkie przetwarzane przez Ciebie przy wykorzystaniu Usługi dane, w szczególności jeżeli naruszasz niniejsze Zasady.
Nie możesz wykorzystywać Usługi do przetwarzania materiałów zawierających treści o charakterze bezprawnym, w szczególności materiałów stanowiących lub zawierających wirusy komputerowe lub jakiekolwiek inne oprogramowanie, którego działanie skutkuje naruszeniem prawa.
Ponadto, nie możesz podejmować jakichkolwiek działań mających wpływ na systemy zabezpieczeń systemów informatycznych Serwisu Allegro lub osób trzecich, a także działać w sposób powodujący utratę stabilności pracy lub przeciążenie systemów informatycznych bezpośrednio lub pośrednio zaangażowanych przy świadczeniu Usługi. Działania, które możesz przeprowadzać to wyłącznie testy systemów bezpieczeństwa, jednakże pod warunkiem, że będą zgodne z naszym programem Bug Bounty (app.intigriti.com/programs/allegro/allegrobugbounty/detail).
Pamiętaj, że ponosisz pełną odpowiedzialność za działania własne oraz osób, którym udostępniłeś w sposób celowy lub wskutek zaniedbania dane niezbędne do korzystania z Usługi.
Spółka zastrzega, że nie gwarantuje i nie ponosi jakiejkolwiek odpowiedzialności za jakiekolwiek szkody spowodowane utrudnieniem lub brakiem możliwości korzystania z Usługi, w tym także za utratę lub zniekształcenie jakichkolwiek danych przez Ciebie przetwarzanych przy wykorzystaniu Usługi.
Z uwagi na specyfikę i charakter przedmiotowej Usługi, pamiętaj aby w formularzach nie podawać prawdziwych danych osobowych.
Ostatnia aktualizacja: 05.01.2024 r.

Zgłoś błąd lub zasugeruj zmianę

Czy ten artykuł był dla Ciebie przydatny?


Tak

Nie
Allegro
Serwisy Grupy Allegro

Allegro.cz
Allegro.sk
Allegro.hu
Onedelivery.cz