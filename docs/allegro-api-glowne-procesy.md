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
Główne procesy
Wystawienie oferty powiązanej z produktem
Zarządzanie ofertą
Promowanie oferty
Obsługa zamówień i zwrotów
Zarządzanie przesyłkami przez Wysyłam z Allegro
Zarządzanie komunikacją z klientami
Główne procesy

Opis głównych procesów, które obsłużysz za pomocą Allegro API.

Poniżej znajdziesz opis głównych procesów, które obsłużysz za pomocą Allegro API. Zbiór wszystkich zasobów, znajdziesz natomiast w naszej dokumentacji.

Za najważniejsze procesy, które z perspektywy Allegro powinny zostać obsłużone w integracji w pierwszej kolejności, uważamy:

wystawianie, zarządzanie i promowanie ofert,
obsługa zamówień i zwrotów,
zarządzanie komunikacją z klientami.
Wystawienie oferty powiązanej z produktem
Za pomocą zasobów /sale/product-offers w łatwy sposób, za pomocą jednego żądania, wystawisz aktywną ofertę powiązaną z produktem. Jeśli wskażesz nam dany produkt lub na podstawie przekazanych danych rozpoznamy, że produkt istnieje w naszej bazie, to pobierzemy jego dane i uwzględnimy je w wystawionej ofercie.

W naszym poradniku szczegółowo opisaliśmy, jak wystawić ofertę powiązaną z produktem, a poniżej znajdziesz listę podstawowych zasobów związanych procesem:

POST /sale/product-offers - utwórz ofertę powiązaną z produktem,
GET /sale/products - wyszukaj produkt,
GET /sale/product-offers/{offerId} - pobierz szczegóły oferty,
GET /sale/product-offers/{offerId}/parts - pobierz wybrane elementy oferty,
GET /sale/product-offers/{offerId}/operations/{operationId} - sprawdź status publikacji / edycji oferty.
Zarządzanie ofertą
Każdą ofertę możesz edytować (prócz zarchiwizowanej), np. zmienić cenę przedmiotu, liczbę dostępnych sztuk lub status publikacji. Za pomocą dziennika zdarzeń możesz także śledzić modyfikacje w ofertach zalogowanego sprzedawcy, które wydarzyły się w ciągu ostatnich 24 godzin.

W naszym poradniku szczegółowo opisaliśmy, jak zarządzać ofertą, a poniżej znajdziesz listę podstawowych zasobów związanych procesem:

GET /sale/offer-events - pobierz dziennik zdarzeń w ofertach,
GET /sale/offers - pobierz listę ofert,
GET /sale/product-offers/{offerId} - pobierz szczegółowe dane oferty,
PATCH /sale/product-offers/{offerId} - edytuj ofertę (zamiast całej struktury, możesz przekazać wyłącznie te pola, które chcesz edytować),
PUT /sale/offer-price-change-commands/{commandId} - zmień grupowo cenę w ofertach,
GET /sale/offer-price-change-commands/{commandId}/tasks - pobierz szczegółowy raport z grupowej zmiany ceny,
PUT /sale/offer-quantity-change-commands/{commandId} - zmień grupowo liczbę przedmiotów w ofertach,
GET /sale/offer-quantity-change-commands/{commandId}/tasks - pobierz szczegółowy raport z grupowej zmiany liczby przedmiotów
PUT /sale/offer-modification-commands/{commandId} - zmień grupowo np. cenniki dostaw,
GET /sale/offer-modification-commands/{commandId}/tasks - pobierz szczegółowy raport z grupowej edycji ofert,
PUT /sale/offer-publication-commands/{commandId} - zakończ lub wznów ofertę,
GET /sale/offer-publication-commands/{commandId}/tasks - pobierz szczegółowy raport z grupowej edycji statusu oferty.
Promowanie oferty
Ofertę możesz przypisać do jednej z kampanii marketingowych Allegro, dzięki czemu zyska specjalne oznaczenie i tym samym może wzbudzić większe zainteresowanie wśród kupujących.

W naszym poradniku szczegółowo opisaliśmy, jak przypisać ofertę do kampanii, a poniżej znajdziesz listę podstawowych zasobów związanych z procesem:

GET /sale/badge-campaigns - pobierz listę dostępnych kampanii,
POST /sale/badges - zgłoś ofertę do danego oznaczenia,
GET /sale/badge-applications/{applicationId} - pobierz szczegóły danego zgłoszenia.
Obsługa zamówień i zwrotów
W ramach zasobów do obsługi zamówień pobierzesz wszelkie dane potrzebne do realizacji zamówienia, a także wykonasz akcje posprzedażowe, jak np. zwrot płatności do kupującego czy wniosek o zwrot prowizji w przypadku, gdy transakcja ostatecznie nie dojdzie do skutku.

W naszym poradniku szczegółowo opisaliśmy, jak obsługiwać zamówienia, a poniżej znajdziesz listę podstawowych zasobów związanych z procesem:

GET /order/events - pobierz dziennik zdarzeń,
GET /order/event-stats - pobierz informacje o ostatnim zdarzeniu,
GET /order/checkout-forms/{id} - pobierz szczegóły zamówienia,
PUT /order/checkout-forms/{id}/fulfillment - zmień status realizacji zamówienia,
POST /order/checkout-forms/{id}/shipments - dodaj numer przesyłki do zamówienia,
GET /order/customer-returns/{customerReturnId} - pobierz szczegółowe informacje o zwrocie,
POST /order/customer-returns/{customerReturnId}/rejection - odmów zwrotu wpłaty,
POST /payments/refunds - zrealizuj zwrot płatności,
POST /order/refund-claims - utwórz wniosek o rabat transakcyjny.
Zarządzanie przesyłkami przez Wysyłam z Allegro
Wysyłam z Allegro to narzędzie, które ułatwia zarządzanie przesyłkami w Allegro. Sprzedawcy mogą utworzyć w nim i wydrukować etykiety oraz zamówić odbiór paczek przez przewoźników ze wskazanego adresu.

W naszym poradniku szczegółowo opisaliśmy jak zarządzać przesyłkami w ramach Wysyłam z Allegro, a poniżej znajdziesz listę podstawowych zasobów związanych z procesem:

GET /shipment-management/delivery-services - pobierz listę dostępnych usług dostawy,
POST /shipment-management/shipments/create-commands - utwórz nową paczkę,
GET /shipment-management/shipments/create-commands/{commandId} - sprawdź status utworzenia paczki,
GET /shipment-management/shipments/{shipmentId} - pobierz szczegółowe dane paczki,
POST /shipment-management/shipments/cancel-commands - anuluj paczkę,
GET /shipment-management/shipments/cancel-commands/{commandId} - sprawdź status anulowania paczki,
POST /shipment-management/pickup-proposals - pobierz propozycje dat i godzin odbioru paczek przez kuriera,
POST /shipment-management/pickups/create-commands - zamów odbiór paczek przez kuriera,
GET /shipment-management/pickups/create-commands/{commandId} - sprawdź status zamówienia odbioru paczek,
POST /shipment-management/label - pobierz etykiety,
POST /shipment-management/protocol - pobierz protokoły nadania.
Zarządzanie komunikacją z klientami
W ramach zasobów do obsługi dyskusji i reklamacji sprzedający mogą łatwo nawiązać kontakt z kupującymi oraz wygodnie i szybko rozwiązać problem transakcyjny.

W naszym poradniku szczegółowo opisaliśmy, jak zarządzać dyskusjami i reklamacjami, a poniżej znajdziesz listę podstawowych zasobów związanych z procesem:

GET /sale/issues - pobierz wszystkie dyskusje i reklamacje,
GET /sale/issues/{issueId} - pobierz szczegółowe informacje o dyskusji/reklamacji,
GET /sale/issues/{issueId}/chat - pobierzesz wszystkie wiadomości z dyskusji/reklamacji,
POST /sale/issues/{issueId}/message - dodaj nową wiadomość w dyskusji/reklamacji, w tym wiadomość o sposobie odbioru produktu od kupującego
POST /sale/issues/{issueId}/status - zmień status reklamacji, zaakceptuj roszczenie klienta, zmień rozwiązanie lub odrzuć roszczenie
POST /sale/issues/attachments - prześlij deklarację załącznika,
PUT /sale/issues/attachments/{attachmentId} - prześlij załącznik na nasze serwery,
GET /sale/issues/attachments/{attachmentId} - pobierz załącznik z dyskusji/reklamacji.
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