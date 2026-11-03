from src.api.scraper import (
    _buyers_count_from_listing_item,
    _offer_from_listing_item,
)


def test_buyers_from_label():
    item = {
        "alt": "Filtr oleju Perkins 2654407",
        "offerId": "1",
        "price": {"mainPrice": {"amount": "45.00"}},
        "url": "/oferta/x-1",
        "productPopularity": {"label": "35 osób kupiło ostatnio"},
        "seller": {"login": "s"},
        "delivery": {},
    }
    assert _buyers_count_from_listing_item(item) == 35
    offer = _offer_from_listing_item(item)
    assert offer is not None
    assert offer.buyers_count == 35
    assert offer.price == 45.0


def test_buyers_from_label_parts_when_label_missing():
    item = {
        "productPopularity": {
            "label": "",
            "labels": [
                {
                    "labelParts": [
                        {"text": "28 osób"},
                        {"text": "kupiło ostatnio"},
                    ]
                }
            ],
        }
    }
    assert _buyers_count_from_listing_item(item) == 28


def test_buyers_none_when_no_popularity():
    assert _buyers_count_from_listing_item({"cartQuantity": 2}) is None
