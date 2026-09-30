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
Dokumentacja

Offer
User's offer information
Offer management
Offer translations
Categories and parameters
Images and attachments
Products
Batch offer modification
Automatic pricing
Offer tags
Tax settings
Compatibility List
Rebates and promotions
Offer bundles
Flexible bundles
Badge campaigns
Allegro Prices
AlleDiscount
Offer rating
Classifieds
Pricing
Deposits
Ingredients
Orders
Order management
Payments
Post Purchase Issues
Shipment management
Customer returns
Commission refunds
Sale settings
After sale services
Delivery
Additional services
Additional services translations
Size tables
Points of service
Contacts
Responsible persons
Responsible producers
One Fulfillment
Advance Ship Notices
Fulfillment Stock
Fulfillment Parcels
Fulfillment Products
Fulfillment Returns
Fulfillment Removal
Fulfillment Warehouse
Tax Identification Number
Affiliate
Conversions
Others
Information about user
Information about marketplaces
Message Center
Billing
Auctions and Bidding
Charity
Public user information
get
Get any user's ratings summary
redocly logoAPI docs by Redocly
Allegro REST API (latest)
URL: https://github.com/allegro/allegro-api/issues
Terms of Service
https://developer.allegro.pl/about

Documentation is generated from this OpenAPI 3.0 specification file. To start working with our API, you can also check our official Allegro REST API public collection in Postman.

User's offer information
Get all data of the particular product-offer
Use this resource to retrieve all data of the particular product-offer. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
offerId
required
string
Offer identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Offer returned successfully
400 Invalid offer ID format
401 Unauthorized
403 Forbidden
404 Not Found

get
/sale/product-offers/{offerId}
Response samples
200400401403404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"productSet": [
{}
],
"id": "12394584234",
"name": "Test offer name",
"category": {
"id": "257931"
},
"attachments": [
{}
],
"fundraisingCampaign": {
"id": "string"
},
"additionalServices": {
"id": "string"
},
"delivery": {
"handlingTime": "PT24H",
"shippingRates": {},
"additionalInfo": "Example additional info",
"shipmentDate": "2019-08-24T14:15:22Z"
},
"publication": {
"duration": "PT24H",
"startingAt": "2031-01-04T11:01:59Z",
"status": "INACTIVE",
"republish": false,
"endingAt": "2031-01-04T11:01:59Z",
"endedBy": "USER",
"marketplaces": {}
},
"additionalMarketplaces": {
"allegro-cz": {}
},
"b2b": {
"buyableOnlyByBusiness": false
},
"compatibilityList": {
"type": "MANUAL",
"items": []
},
"language": "pl-PL",
"validation": {
"errors": [],
"warnings": [],
"validatedAt": "2019-08-24T14:15:22Z"
},
"warnings": [ ],
"afterSalesServices": {
"impliedWarranty": {},
"returnPolicy": {},
"warranty": {}
},
"discounts": {
"wholesalePriceList": {}
},
"stock": {
"available": 99,
"unit": "UNIT"
},
"parameters": [
{}
],
"contact": {
"id": "11a2df7f-8237-4625-baa2-cb7541f39946"
},
"createdAt": "2019-05-29T12:00:00Z",
"updatedAt": "2019-05-29T12:00:00Z",
"aiCoCreatedContent": {
"images": []
},
"payments": {
"invoice": "VAT"
},
"sellingMode": {
"format": "BUY_NOW",
"price": {},
"minimalPrice": {},
"startingPrice": {}
},
"location": {
"city": "Poznań",
"countryCode": "PL",
"postCode": "00-999",
"province": "WIELKOPOLSKIE"
},
"images": [
"https://a.allegroimg.com/original/12068b/359d04074521b79df1b2807a6727"
],
"description": {
"sections": []
},
"external": {
"id": "AH-129834"
},
"sizeTable": {
"id": "string"
},
"taxSettings": {
"rates": [],
"subject": "GOODS",
"exemption": "MONEY_EQUIVALENT"
},
"messageToSellerSettings": {
"mode": "OPTIONAL",
"hint": "Choose size"
}
}
Get selected data of the particular product-offer
Use this resource to retrieve selected data of the particular product-offer. The model and functionality is a subset of the full product offer get endpoint (GET /sale/product-offers/{offerId}), but it is faster and more reliable. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
offerId
required
string
Offer identifier.

query Parameters
include
required
Array of strings
Items Enum: "stock" "price"
Selection of parts intended to retrieve. Multiple parts can be specified at the same time.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Offer returned successfully
400 Invalid offer ID format or unsupported part name
401 Unauthorized - access to this resource requires authorization
403 Access to offer is forbidden for this account
404 Offer not found

get
/sale/product-offers/{offerId}/parts
Response samples
200400401403404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "12394584234",
"stock": {
"available": 99
},
"sellingMode": {
"price": {}
},
"additionalMarketplaces": {
"marketplaceId1": {},
"marketplaceId2": {}
}
}
Get seller's offers
Use this resource to get the list of the seller's offers. You can use different query parameters to filter the list. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
offer.id	
Array of strings
Example: offer.id=16885969603
Offer ID.

name	
string
Example: name=iPhone 15
The text to search in the offer title.

sellingMode.price.amount.gte	
number >= 0
Example: sellingMode.price.amount.gte=9.99
The lower threshold of price.

If additionally a publication.marketplace is provided, searches using the price on the given marketplace.

sellingMode.price.amount.lte	
number >= 1
Example: sellingMode.price.amount.lte=125.99
The upper threshold of price.

If additionally a publication.marketplace is provided, searches using the price on the given marketplace.

sellingMode.priceAutomation.rule.id	
string
Example: sellingMode.priceAutomation.rule.id=66950bc04a57a95dfad0891d
The ID of price automation rule. Returns offers with given price automation rule ID.

If additionally a publication.marketplace is provided, searches using the price automation rule on the given marketplace.

sellingMode.priceAutomation.rule.id.empty	
boolean
Allows to filter offers by existence of price automation rule ID. Passing 'false' will return offers with any price automation rule, passing 'true' will return offers without any price automation rules.

If additionally a publication.marketplace is provided, searches using the price automation rule on the given marketplace.

publication.status	
Array of strings
Items Enum: "INACTIVE" "ACTIVE" "ACTIVATING" "ENDED"
Example: publication.status=INACTIVE
The publication status of the offer. Passing more than one value will search for offers with any of the given statuses. By default all statuses are included. Example: publication.status=INACTIVE&publication.status=ACTIVE - returns offers with status INACTIVE or ACTIVE.

publication.marketplace	
string (MarketplaceId)
Example: publication.marketplace=allegro-pl
Either the base marketplace or an additional marketplace of the offer.

When passing the parameter publication.marketplace, searches for offers with the given marketplace as either its base marketplace or one of its additional marketplaces. When the parameter is omitted, searches for offers with all marketplaces.

In addition to searching, passing the parameter also influences the functionality of other query parameter by searching and sorting by data (e.g. price) on the given marketplace.

sellingMode.format	
Array of strings
Items Enum: "BUY_NOW" "ADVERTISEMENT" "AUCTION"
Example: sellingMode.format=BUY_NOW
The offer's selling format. Passing more than one value will search for offers with any of the given formats. By default all formats are included. Example: sellingMode.format=BUY_NOW&sellingMode.format=ADVERTISEMENT - returns offers with with format BUY_NOW or ADVERTISEMENT.

external.id	
Array of strings <= 100 items [ items <= 100 characters ]
Example: external.id=EXTERNAL_ID_122
The ID from the client's external system. Passing more than one value will search for offers with any of the given IDs. By default no ID is included. Example: external.id=1233&external.id=1234 - returns offers with ID 1233 or 1234. Single ID length shouldn't exceed 100 characters.

delivery.shippingRates.id	
string <uuid>
Example: delivery.shippingRates.id=2991e29e-5fbc-46f5-963a-65c326ba65c2
The ID of shipping rates. Returns offers with given shipping rates ID.

delivery.shippingRates.id.empty	
boolean
Allows to filter offers by existence of shipping rates ID.

sort	
string
Enum: "sellingMode.price.amount" "-sellingMode.price.amount" "stock.sold" "-stock.sold" "stock.available" "-stock.available"
Example: sort=sellingMode.price.amount
The results' sorting order. No prefix in the value means ascending order. - prefix means descending order. If you don't provide the sort parameter, the list is sorted by offer creation time, descending.

If additionally a publication.marketplace is provided, sorts by price and stock.sold using the data on the given marketplace.

limit	
integer <int32> [ 1 .. 1000 ]
Default: 20
Example: limit=100
The maximum number of offers returned in the response.

offset	
integer <int32> [ 0 .. 9999999 ]
Example: offset=101
Index of the first returned offer from all search results. Maximum sum of offset and limit is 10 000 000.

category.id	
string
Example: category.id=20285
The identifier of the category, where you want to search for offers.

product.id.empty	
boolean
Example: product.id.empty=true
Allows to filter offers by existence of product ID.

productizationRequired	
boolean
Example: productizationRequired=true
Allows to search for offers from categories where productization is required.

b2b.buyableOnlyByBusiness	
boolean
Allows to search for offers buyable only by businesses.

fundraisingCampaign.id	
string <uuid>
Example: fundraisingCampaign.id=e2307b4f-6903-4be6-85e6-19e8ea303760
ID of the charity fundraising campaign that benefits from this offer.

fundraisingCampaign.id.empty	
boolean
Allows to search for charity or commercial offers.

afterSalesServices.returnPolicy.id	
string <uuid>
The ID of return policy. Returns offers with given return policy ID.

isFulfillment	
boolean
Example: isFulfillment=true
Allows to search for offers handled by the Allegro Warehouse (One Fulfillment).

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 The list of offers returned successfully.
400 The request query parameters are invalid.
403 The user has no rights to query offers or provided token is invalid.

get
/sale/offers
Response samples
200400403
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"offers": [
{}
],
"count": 1,
"totalCount": 1234
}
Get Smart! classification report of the particular offer
Use this resource to get a full Smart! offer classification report of one of your offers. Please keep in mind you have to meet Smart! seller conditions first - for more details, use GET /sale/smart. To learn more about Smart! offer requirements, see our knowledge base article: PL / EN. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
offerId
required
string
Offer identifier.

query Parameters
marketplaceId	
string
Example: marketplaceId=allegro-pl
Marketplace for which offer classification report will be returned. If not specified, the result of the offer's base marketplace will be returned.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Successfully returned offer Smart! classification report
400 Bad Request
401 Unauthorized action
403 Offer does not belong to seller
404 Not Found
422 Unprocessable entity
The offer is being created in our system and we are not able to process it yet. Try again later.
Provided marketplaceId is not supported.

get
/sale/offers/{offerId}/smart
Response samples
200400401403404422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"classification": {
"fulfilled": true,
"lastChanged": "2017-05-17T08:36:57.292+02:00"
},
"scheduledForReclassification": true,
"conditions": [
{},
{}
]
}
Get events about the seller's offers
Use this endpoint to get events from the last 24 hours concerning changes in the authorized seller's offers. At present we support the following events:

OFFER_ACTIVATED - offer is visible on site and available for purchase, occurs when offer status changes from ACTIVATING to ACTIVE.
OFFER_CHANGED - occurs when offer's fields have been changed e.g. description or photos, but does not apply to shipping rates and dispatch time.
OFFER_ENDED - offer is no longer available for purchase, occurs when offer status changes from ACTIVE to ENDED.
OFFER_STOCK_CHANGED - stock in an offer was changed either via purchase or by seller.
OFFER_PRICE_CHANGED - occurs when price in an offer was changed.
OFFER_ARCHIVED - offer is no longer available on listing and has been archived.
OFFER_BID_PLACED - bid was placed on the offer.
OFFER_BID_CANCELED - bid for offer was canceled.
OFFER_TRANSLATION_UPDATED - translation of offer was updated.
OFFER_VISIBILITY_CHANGED - visibility of offer was changed on marketplaces.
OFFER_DELIVERY_COUNTRIES_BLOCKED - the offer has been blocked in selected countries.
Returned events may occur by actions made via browser or API. The resource allows you to get events concerning active offers and offers scheduled for activation (status ACTIVE and ACTIVATING). Returned events do not concern offers in INACTIVE and ENDED status (the exception is OFFER_ARCHIVED event). External id is returned for all event types except OFFER_BID_PLACED and OFFER_BID_CANCELED. Please note that one change may result in more than one event. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
from	
string <= 256 characters
Example: from=MTEzMjQzODU3NA
The ID of the last seen event. Events that occured after the given event will be returned.

limit	
integer [ 1 .. 1000 ]
Default: 100
The number of events that will be returned in the response.

type	
Array of strings
Items Enum: "OFFER_ACTIVATED" "OFFER_CHANGED" "OFFER_ENDED" "OFFER_STOCK_CHANGED" "OFFER_PRICE_CHANGED" "OFFER_ARCHIVED" "OFFER_BID_PLACED" "OFFER_BID_CANCELED" "OFFER_TRANSLATION_UPDATED" "OFFER_VISIBILITY_CHANGED" "OFFER_DELIVERY_COUNTRIES_BLOCKED"
The types of events that will be returned in the response. All types of events are returned by default.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "en-US"
Example: en-US
Expected language of messages.

Responses
200 The list of offer events returned successfully.
400 Invalid parameters supplied in the request.
401 Unauthorized

get
/sale/offer-events
Response samples
200400401
Content type
application/vnd.allegro.public.v1+json
Example

offer event
offer event

Copy
Expand allCollapse all
{
"offerEvents": [
{}
]
}
Offer management
Create offer based on product
Use this resource to create offer based on product. Read more: PL / EN. Note that requests may be limited.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
productSet	
Array of objects
b2b	
object (B2b)
Defines offer properties for buyers with company account (Allegro Biznes).

attachments	
Array of objects (ProductOfferAttachment)
An array of offer attachments.

fundraisingCampaign	
object (ProductOfferFundraisingCampaignRequest)
additionalServices	
object (ProductOfferAdditionalServicesRequest)
Offer additional services.

stock
required
object (SaleProductOffersRequestStock)
delivery	
object
publication	
object (SaleProductOfferPublicationRequest)
additionalMarketplaces	
object (AdditionalMarketplacesRequest)
Selected information about the offer in each additional service. This field does not contain information about the base marketplace of the offer.
Possible values of marketplaceId can be obtained from GET /marketplaces resource.
See Allegro foreign marketplaces for more details regarding this field.

compatibilityList	
object
For the /sale/product-offers resources you can send only definition of the MANUAL compatibility list. If compatibility list is provided for the product assigned to the offer, it will be used automatically.

language	
string <BCP-47 language code>
Declared base language of the offer.

aiCoCreatedContent	
object (AiCoCreatedContent)
Information about content declared as generated using AI.

category	
object (OfferCategoryRequest)
Category in which the offer is listed for sale. You can indicate a category from the product's 'similar categories' to set the offer's category.

name	
string [ 12 .. 75 ] characters
Name (title) of an offer. Must contain between 12 and 75 characters (including spaces) and consist of at least 3 words. Read more: PL / EN .

parameters	
Array of objects (ParameterProductOfferRequest)
afterSalesServices	
object (AfterSalesServicesProductOfferRequest)
The definitions of the different after sales services assigned to the offer.

sizeTable	
object or null
The size table information. You can enter the size tabe identifier or name.

contact	
object
Identifier of contact data for sales format ADVERTISEMENT (classified ad). You can enter the contact identifier or name.

discounts	
object (DiscountsProductOfferRequest)
payments	
object (Payments)
sellingMode	
object (SellingMode)
Information on the offer's selling mode.

location	
object (Location)
for offer with a delivery method it is a parcel dispatch location. For offers with personal pick-up it is a pick-up location, additionally we recommend to use points of service (https://developer.allegro.pl/documentation/#tag/Points-of-service)

images	
Array of strings
description	
object (StandardizedDescription)
The description section cannot have more than 40000 bytes in length.

external	
object (ExternalId)
The information on the offer in an external system.

taxSettings	
object or null
Tax settings for offer. Available settings can be found under "get all tax settings for category" resource.

messageToSellerSettings	
object or null
Defines message to the seller settings options.

Responses
201 Offer created successfully.
202 The product-offer creation request has been accepted for processing, but the processing has not been completed.
400 Bad request
401 Unauthorized
403 Forbidden - not allowed to access.
422 Unprocessable Entity

post
/sale/product-offers
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"productSet": [
{}
],
"b2b": {
"buyableOnlyByBusiness": false
},
"attachments": [
{}
],
"fundraisingCampaign": {
"id": "e2307b4f-6903-4be6-85e6-19e8ea303760",
"name": "We are collecting food for animals from the shelter"
},
"additionalServices": {
"id": "string",
"name": "string"
},
"stock": {
"available": 99,
"unit": "UNIT"
},
"delivery": {
"handlingTime": "PT24H",
"shippingRates": null,
"additionalInfo": "Example additional info",
"shipmentDate": "2019-08-24T14:15:22Z"
},
"publication": {
"duration": "PT24H",
"startingAt": "2031-01-04T11:01:59Z",
"status": "INACTIVE",
"republish": false,
"endingAt": "2031-01-04T11:01:59Z"
},
"additionalMarketplaces": {
"allegro-cz": {}
},
"compatibilityList": {
"items": []
},
"language": "pl-PL",
"aiCoCreatedContent": {
"images": []
},
"category": {
"id": "257931"
},
"name": "Test offer name",
"parameters": [
{}
],
"afterSalesServices": {
"impliedWarranty": {},
"returnPolicy": {},
"warranty": {}
},
"sizeTable": {
"id": "string",
"name": "Nike shoes size table"
},
"contact": {
"id": "11a2df7f-8237-4625-baa2-cb7541f39946",
"name": "Piotr"
},
"discounts": {
"wholesalePriceList": {}
},
"payments": {
"invoice": "VAT"
},
"sellingMode": {
"format": "BUY_NOW",
"price": {},
"minimalPrice": {},
"startingPrice": {}
},
"location": {
"city": "Poznań",
"countryCode": "PL",
"postCode": "00-999",
"province": "WIELKOPOLSKIE"
},
"images": [
"https://a.allegroimg.com/original/12068b/359d04074521b79df1b2807a6727"
],
"description": {
"sections": []
},
"external": {
"id": "AH-129834"
},
"taxSettings": {
"rates": [],
"subject": "GOODS",
"exemption": "MONEY_EQUIVALENT"
},
"messageToSellerSettings": {
"mode": "OPTIONAL",
"hint": "Choose size"
}
}
Response samples
201202400401403422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"productSet": [
{}
],
"id": "12394584234",
"name": "Test offer name",
"category": {
"id": "257931"
},
"attachments": [
{}
],
"fundraisingCampaign": {
"id": "string"
},
"additionalServices": {
"id": "string"
},
"delivery": {
"handlingTime": "PT24H",
"shippingRates": {},
"additionalInfo": "Example additional info",
"shipmentDate": "2019-08-24T14:15:22Z"
},
"publication": {
"duration": "PT24H",
"startingAt": "2031-01-04T11:01:59Z",
"status": "INACTIVE",
"republish": false,
"endingAt": "2031-01-04T11:01:59Z",
"endedBy": "USER",
"marketplaces": {}
},
"additionalMarketplaces": {
"allegro-cz": {}
},
"b2b": {
"buyableOnlyByBusiness": false
},
"compatibilityList": {
"type": "MANUAL",
"items": []
},
"language": "pl-PL",
"validation": {
"errors": [],
"warnings": [],
"validatedAt": "2019-08-24T14:15:22Z"
},
"warnings": [ ],
"afterSalesServices": {
"impliedWarranty": {},
"returnPolicy": {},
"warranty": {}
},
"discounts": {
"wholesalePriceList": {}
},
"stock": {
"available": 99,
"unit": "UNIT"
},
"parameters": [
{}
],
"contact": {
"id": "11a2df7f-8237-4625-baa2-cb7541f39946"
},
"createdAt": "2019-05-29T12:00:00Z",
"updatedAt": "2019-05-29T12:00:00Z",
"aiCoCreatedContent": {
"images": []
},
"payments": {
"invoice": "VAT"
},
"sellingMode": {
"format": "BUY_NOW",
"price": {},
"minimalPrice": {},
"startingPrice": {}
},
"location": {
"city": "Poznań",
"countryCode": "PL",
"postCode": "00-999",
"province": "WIELKOPOLSKIE"
},
"images": [
"https://a.allegroimg.com/original/12068b/359d04074521b79df1b2807a6727"
],
"description": {
"sections": []
},
"external": {
"id": "AH-129834"
},
"sizeTable": {
"id": "string"
},
"taxSettings": {
"rates": [],
"subject": "GOODS",
"exemption": "MONEY_EQUIVALENT"
},
"messageToSellerSettings": {
"mode": "OPTIONAL",
"hint": "Choose size"
}
}
Edit an offer
Use this resource to edit offer. This resource allows you to edit each field independently, so use it if you want to change only, for example, the price or the quantity in an offer. Read more: PL / EN. Note that requests may be limited.

Authorizations:
bearer-token-for-user
path Parameters
offerId
required
string
The offer identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
productSet	
Array of objects
b2b	
object (B2b)
Defines offer properties for buyers with company account (Allegro Biznes).

attachments	
Array of objects (ProductOfferAttachment)
An array of offer attachments.

fundraisingCampaign	
object (ProductOfferFundraisingCampaignRequest)
additionalServices	
object (ProductOfferAdditionalServicesRequest)
Offer additional services.

compatibilityList	
object
For the /sale/product-offers resources you can send only definition of the MANUAL compatibility list. If compatibility list is provided for the product assigned to the offer, it will be used automatically.

delivery	
object
stock	
object (SaleProductOffersRequestStock)
publication	
object (SaleProductOfferPublicationRequest)
additionalMarketplaces	
object (AdditionalMarketplacesRequest)
Selected information about the offer in each additional service. This field does not contain information about the base marketplace of the offer.
Possible values of marketplaceId can be obtained from GET /marketplaces resource.
See Allegro foreign marketplaces for more details regarding this field.

language	
string <BCP-47 language code>
Declared base language of the offer.

aiCoCreatedContent	
object (AiCoCreatedContent)
Information about content declared as generated using AI.

category	
object (OfferCategoryRequest)
Category in which the offer is listed for sale. You can indicate a category from the product's 'similar categories' to set the offer's category.

name	
string [ 12 .. 75 ] characters
Name (title) of an offer. Must contain between 12 and 75 characters (including spaces) and consist of at least 3 words. Read more: PL / EN .

parameters	
Array of objects (ParameterProductOfferRequest)
afterSalesServices	
object (AfterSalesServicesProductOfferRequest)
The definitions of the different after sales services assigned to the offer.

sizeTable	
object or null
The size table information. You can enter the size tabe identifier or name.

contact	
object
Identifier of contact data for sales format ADVERTISEMENT (classified ad). You can enter the contact identifier or name.

discounts	
object (DiscountsProductOfferRequest)
payments	
object (Payments)
sellingMode	
object (SellingMode)
Information on the offer's selling mode.

location	
object (Location)
for offer with a delivery method it is a parcel dispatch location. For offers with personal pick-up it is a pick-up location, additionally we recommend to use points of service (https://developer.allegro.pl/documentation/#tag/Points-of-service)

images	
Array of strings
description	
object (StandardizedDescription)
The description section cannot have more than 40000 bytes in length.

external	
object (ExternalId)
The information on the offer in an external system.

taxSettings	
object or null
Tax settings for offer. Available settings can be found under "get all tax settings for category" resource.

messageToSellerSettings	
object or null
Defines message to the seller settings options.

Responses
200 Offer edited successfully.
202 The request to edit product-offer has been accepted for processing, but the processing has not been completed.
400 Bad request
401 Unauthorized
403 Forbidden - not allowed to access.
404 Not Found. Offer not found.
409 Conflict. The current state of the offer does not allow to perform the request (e.g. The previous edition of the offer is still being processed).
422 Unprocessable Entity

patch
/sale/product-offers/{offerId}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"productSet": [
{}
],
"b2b": {
"buyableOnlyByBusiness": false
},
"attachments": [
{}
],
"fundraisingCampaign": {
"id": "e2307b4f-6903-4be6-85e6-19e8ea303760",
"name": "We are collecting food for animals from the shelter"
},
"additionalServices": {
"id": "string",
"name": "string"
},
"compatibilityList": {
"items": []
},
"delivery": {
"handlingTime": "PT24H",
"shippingRates": null,
"additionalInfo": "Example additional info",
"shipmentDate": "2019-08-24T14:15:22Z"
},
"stock": {
"available": 99,
"unit": "UNIT"
},
"publication": {
"duration": "PT24H",
"startingAt": "2031-01-04T11:01:59Z",
"status": "INACTIVE",
"republish": false,
"endingAt": "2031-01-04T11:01:59Z"
},
"additionalMarketplaces": {
"allegro-cz": {}
},
"language": "pl-PL",
"aiCoCreatedContent": {
"images": []
},
"category": {
"id": "257931"
},
"name": "Test offer name",
"parameters": [
{}
],
"afterSalesServices": {
"impliedWarranty": {},
"returnPolicy": {},
"warranty": {}
},
"sizeTable": {
"id": "string",
"name": "Nike shoes size table"
},
"contact": {
"id": "11a2df7f-8237-4625-baa2-cb7541f39946",
"name": "Piotr"
},
"discounts": {
"wholesalePriceList": {}
},
"payments": {
"invoice": "VAT"
},
"sellingMode": {
"format": "BUY_NOW",
"price": {},
"minimalPrice": {},
"startingPrice": {}
},
"location": {
"city": "Poznań",
"countryCode": "PL",
"postCode": "00-999",
"province": "WIELKOPOLSKIE"
},
"images": [
"https://a.allegroimg.com/original/12068b/359d04074521b79df1b2807a6727"
],
"description": {
"sections": []
},
"external": {
"id": "AH-129834"
},
"taxSettings": {
"rates": [],
"subject": "GOODS",
"exemption": "MONEY_EQUIVALENT"
},
"messageToSellerSettings": {
"mode": "OPTIONAL",
"hint": "Choose size"
}
}
Response samples
200202400401403404409422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"productSet": [
{}
],
"id": "12394584234",
"name": "Test offer name",
"category": {
"id": "257931"
},
"attachments": [
{}
],
"fundraisingCampaign": {
"id": "string"
},
"additionalServices": {
"id": "string"
},
"delivery": {
"handlingTime": "PT24H",
"shippingRates": {},
"additionalInfo": "Example additional info",
"shipmentDate": "2019-08-24T14:15:22Z"
},
"publication": {
"duration": "PT24H",
"startingAt": "2031-01-04T11:01:59Z",
"status": "INACTIVE",
"republish": false,
"endingAt": "2031-01-04T11:01:59Z",
"endedBy": "USER",
"marketplaces": {}
},
"additionalMarketplaces": {
"allegro-cz": {}
},
"b2b": {
"buyableOnlyByBusiness": false
},
"compatibilityList": {
"type": "MANUAL",
"items": []
},
"language": "pl-PL",
"validation": {
"errors": [],
"warnings": [],
"validatedAt": "2019-08-24T14:15:22Z"
},
"warnings": [ ],
"afterSalesServices": {
"impliedWarranty": {},
"returnPolicy": {},
"warranty": {}
},
"discounts": {
"wholesalePriceList": {}
},
"stock": {
"available": 99,
"unit": "UNIT"
},
"parameters": [
{}
],
"contact": {
"id": "11a2df7f-8237-4625-baa2-cb7541f39946"
},
"createdAt": "2019-05-29T12:00:00Z",
"updatedAt": "2019-05-29T12:00:00Z",
"aiCoCreatedContent": {
"images": []
},
"payments": {
"invoice": "VAT"
},
"sellingMode": {
"format": "BUY_NOW",
"price": {},
"minimalPrice": {},
"startingPrice": {}
},
"location": {
"city": "Poznań",
"countryCode": "PL",
"postCode": "00-999",
"province": "WIELKOPOLSKIE"
},
"images": [
"https://a.allegroimg.com/original/12068b/359d04074521b79df1b2807a6727"
],
"description": {
"sections": []
},
"external": {
"id": "AH-129834"
},
"sizeTable": {
"id": "string"
},
"taxSettings": {
"rates": [],
"subject": "GOODS",
"exemption": "MONEY_EQUIVALENT"
},
"messageToSellerSettings": {
"mode": "OPTIONAL",
"hint": "Choose size"
}
}
Check the processing status of a POST or PATCH request
The URI for the resource given by Location header of POST /sale/product-offers and PATCH /sale/product-offers/{offerId}. Use this resource to check processing status of a POST or PATCH request. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
offerId
required
string
Offer identifier.

operationId
required
string
Operation identifier provided in location header of POST or PATCH request.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
202 The request processing has not been completed.
303 The processing of product-offer has been completed. The Location header provide information about the location of processed resource.
400 Syntactically incorrect request
401 Unauthorized
403 Forbidden
404 Not Found
422 Unprocessable Entity

get
/sale/product-offers/{offerId}/operations/{operationId}
Response samples
202422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"offer": {
"id": "123456789"
},
"operation": {
"id": "b572cdd0-7f2c-4800-9165-15795bd95f3c",
"status": "IN_PROGRESS",
"startedAt": "2019-05-29T12:00:00Z"
}
}
Delete a draft offer
Use this resource to delete a draft offer. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
offerId
required
string
Offer identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
204 No content
401 Unauthorized
403 Forbidden
404 Not Found

delete
/sale/offers/{offerId}
Modify the Buy Now price in an offer
Use this resource to change the Buy Now price in a single offer. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
offerId
required
string
The offer identifier.

commandId
required
string
The unique command id generated by you.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
id	
string
The unique command id generated by you. This should be the same UUID as used in the path.

input
required
object (ChangePriceInput)
The input of the command, i.e. the new Buy Now price for the offer.

Responses
200 The command was created successfully and is queued for processing.
default An immediate error response is returned whether the command input data is not valid or there is an internal problem with our systems.

put
/offers/{offerId}/change-price-commands/{commandId}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "6365996a-6cae-11e9-a923-1681be663d3e",
"input": {
"buyNowPrice": {}
}
}
Response samples
200default
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "6365996a-6cae-11e9-a923-1681be663d3e",
"input": {
"buyNowPrice": {}
},
"output": {
"status": "SUCCESSFUL",
"errors": []
}
}
Batch offer publish / unpublish
Use this resource to modify multiple offers publication at once. Read more: PL / EN. This resource is rate limited to 250 000 offer changes per hour or 9000 offer changes per minute.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
publicationChangeCommandDto

offerCriteria	
Array of objects (OfferCriterium)
List of offer criteria

publication	
object (Publication_modification)
Contains publication's fields to change

Responses
201 Command was registered
400 Semantically incorrect request or provided conditions not correct
401 Unauthorized
403 Forbidden
404 Not Found
409 Command id was already used
422 Unprocessable Entity

put
/sale/offer-publication-commands/{commandId}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"offerCriteria": [
{}
],
"publication": {
"action": "ACTIVATE",
"scheduledFor": "2019-08-24T14:15:22Z"
}
}
Response samples
201
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "b9b8ef16-2709-411e-ac94-2be7e3ba25e7",
"createdAt": "2017-05-17T08:36:57.292Z",
"completedAt": "2017-05-17T08:36:57.292Z",
"taskCount": {
"failed": 0,
"success": 0,
"total": 0
}
}
Publish command summary
Use this resource to retrieve information about the offer listing statuses. You will receive a summary with a number of correctly listed offers and errors. Read more: PL / EN. This resource is rate limited to retrieving information about 270 000 offer changes per minute.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Report was generated and successfully returned
401 Unauthorized
403 Forbidden
404 Command not found

get
/sale/offer-publication-commands/{commandId}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "b9b8ef16-2709-411e-ac94-2be7e3ba25e7",
"createdAt": "2017-05-17T08:36:57.292Z",
"completedAt": "2017-05-17T08:36:57.292Z",
"taskCount": {
"failed": 0,
"success": 0,
"total": 0
}
}
Publish command detailed report
Use this resource to retrieve information about the offer statuses on the site (Defaults: limit = 100, offset = 0). Read more: PL / EN. This resource is rate limited to retrieving information about 270 000 offer changes per minute.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command identifier.

query Parameters
limit	
integer <int32> [ 1 .. 1000 ]
Default: 100
Example: limit=200
The limit of elements in the response.

offset	
integer <int32> [ 0 .. 999 ]
Default: 0
Example: offset=201
The offset of elements in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Task status successfully returned
400 Bad request
401 Unauthorized
403 Forbidden
404 Command not found
422 Unprocessable Entity

get
/sale/offer-publication-commands/{commandId}/tasks
Response samples
200400
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"tasks": [
{}
]
}
Get all available offer promotion packages
Use this resource to retrieve all available offer promotion packages. Read more: PL / EN.

Authorizations:
bearer-token-for-applicationbearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Offer promotion packages returned successfully.
401 Unauthorized

get
/sale/offer-promotion-packages
Response samples
200401
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"marketplaceId": "allegro-pl",
"basePackages": [
{}
],
"extraPackages": [
{}
],
"additionalMarketplaces": [
{}
]
}
Modify offer promotion packages
Use this resource to modify offer promotion packages. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
offerId
required
string
Example: 9991337999
Offer identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
request

modifications	
Array of objects (PromoOptionsModification)
Promotion package modifications to be applied.

additionalMarketplaces	
Array of objects (AdditionalMarketplacePromoOptionsModification)
Promotion package modifications to be applied on additional marketplaces.

Responses
200 Offer promotion packages modified successfully.
401 Unauthorized
403 Offer does not belong to seller.
422 Offer does not exist or unsupported package name or unsupported change type.

post
/sale/offers/{offerId}/promo-options-modification
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"modifications": [
{}
],
"additionalMarketplaces": [
{}
]
}
Response samples
200401403422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"offerId": "9991337999",
"marketplaceId": "allegro-pl",
"basePackage": {
"id": "emphasized1d",
"validFrom": "2020-01-01T00:00:00Z",
"validTo": "2020-01-01T00:00:00Z",
"nextCycleDate": "2020-01-01T00:00:00Z"
},
"extraPackages": [
{}
],
"pendingChanges": {
"basePackage": {}
},
"additionalMarketplaces": [
{}
]
}
Get offer promotion packages
Use this resource to get promotion packages assigned to an offer. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
offerId
required
string
Example: 9991337999
Offer identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Offer promotion packages returned successfully
401 Unauthorized
403 Offer does not belong to seller.

get
/sale/offers/{offerId}/promo-options
Response samples
200401403
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"offerId": "9991337999",
"marketplaceId": "allegro-pl",
"basePackage": {
"id": "emphasized1d",
"validFrom": "2020-01-01T00:00:00Z",
"validTo": "2020-01-01T00:00:00Z",
"nextCycleDate": "2020-01-01T00:00:00Z"
},
"extraPackages": [
{}
],
"pendingChanges": {
"basePackage": {}
},
"additionalMarketplaces": [
{}
]
}
Get promo options for seller's offers
Use this resource to retrieve promo options for seller offers. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
limit	
integer <int32> [ 1 .. 5000 ]
Default: 5000
Limit of promo options per page.

offset	
integer <int64> >= 0
Default: 0
Distance between the beginning of the document and the point from which promo options are returned.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Promo options for seller offers successfully returned.
400 Bad request
401 Unauthorized

get
/sale/offers/promo-options
Response samples
200400401
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"promoOptions": [
{}
],
"count": 3,
"totalCount": 256
}
Batch offer promotion package modification
Use this resource to modify promotion packages on multiple offers at once. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Example: aca8103b-14eb-4855-b9b3-de5bef06bd30
Command identifier. Must be a UUID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Promotion packages modification command request.

offerCriteria	
Array of objects (OfferCriterium)
Offer choice criteria.

modification	
object (PromoOptionsCommandModification)
additionalMarketplaces	
Array of objects (AdditionalMarketplacePromoOptionsCommandModification)
Responses
201 Command was registered
401 Unauthorized
409 Command id already in use.
422 Size of batch should be between 1 and 1000 offers or unsupported modification time.

put
/sale/offers/promo-options-commands/{commandId}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"offerCriteria": [
{}
],
"modification": {
"basePackage": {},
"extraPackages": [],
"modificationTime": "END_OF_CYCLE"
},
"additionalMarketplaces": [
{}
]
}
Response samples
201401409422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "9b84e1bc-5341-45e7-837e-4250720e606f",
"taskCount": {
"failed": 0,
"success": 0,
"total": 0
}
}
Modification command summary
Use this resource to find out how many offers were edited within one {commandId}. You will receive a summary with a number of successfully edited offers and errors. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Summary successfully returned.
401 Unauthorized
403 Batch modification command does not belong to seller.
404 Batch modification command does not exist.

get
/sale/offers/promo-options-commands/{commandId}
Response samples
200401403404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "9b84e1bc-5341-45e7-837e-4250720e606f",
"taskCount": {
"failed": 0,
"success": 0,
"total": 0
}
}
Modification command detailed result
Use this resource to retrieve the result of an offer modification command. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command identifier.

query Parameters
limit	
integer [ 1 .. 1000 ]
Default: 100
The limit of returned items.

offset	
integer >= 0
Default: 0
The offset of returned items.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Report successfully returned.
401 Unauthorized
403 Batch modification command does not belong to seller.
404 Batch modification command does not exist.

get
/sale/offers/promo-options-commands/{commandId}/tasks
Response samples
200401403404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"tasks": [
{}
],
"modification": {
"basePackage": {},
"extraPackages": [],
"modificationTime": "END_OF_CYCLE"
},
"additionalMarketplaces": [
{}
]
}
Get offers with missing parameters
Use this resource to get information about required parameters or parameters scheduled to become required that are not filled in offers. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
offer.id	
Array of strings
List of offer ids. If empty all offers with unfilled parameters will be returned.

parameterType	
string
Enum: "REQUIRED" "REQUIREMENT_PLANNED"
Filter by parameter type.

offset	
integer <int32> >= 0
Default: 0
The offset of elements in the response.

limit	
integer <int32> [ 1 .. 1000 ]
Default: 100
The limit of elements in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Unfilled offer parameters were returned successfully.
400 Bad Request
401 Unauthorized
403 Forbidden

get
/sale/offers/unfilled-parameters
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"offers": [
{}
],
"count": 3,
"totalCount": 256
}
Offer translations
Get offer translations
Get offer translation for given language or all present. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
offerId
required
string
Offer identifier.

query Parameters
language	
string <BCP-47 language code>
Example: language=en-US
Language for translation to retrieve. If not provided, all translations as well as base content for offer will be returned.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 The list of offer translations returned successfully.
401 Unauthorized
403 Forbidden
404 Not Found

get
/sale/offers/{offerId}/translations
Response samples
200401403404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"translations": [
{}
]
}
Update offer translation
Update manual translation for offer. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
language
required
string <BCP-47 language code>
Example: en-US
Language of the provided translation.

offerId
required
string
Offer identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Request with manual translation for offer, must contain at least one translated offer element (title, description or safety information).

description	
object (ManualDescriptionTranslation)
Manual offer description translation

title	
object (ManualTitleTranslation)
Manual offer title translation

safetyInformation	
object (ManualSafetyInformationTranslation)
Manual offer products safety information translations. Updating this resource is in accordance with RFC7396 - all or nothing.'

Responses
200 Update successful
401 Unauthorized
403 Forbidden
422 Unprocessable Entity

patch
/sale/offers/{offerId}/translations/{language}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"description": {
"translation": {}
},
"title": {
"translation": "Shoes size 42 black"
},
"safetyInformation": {
"products": []
}
}
Response samples
401403422
Content type
application/vnd.allegro.public.v1+json

Copy
{
"error": "unauthorized",
"error_description": "Full authentication is required to access this resource"
}
Delete offer translation
Delete single element or entire manual translation. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
language
required
string <BCP-47 language code>
Example: en-US
Language of the translation to delete.

offerId
required
string
Offer identifier.

query Parameters
element	
string
Enum: "title" "description" "safety_information"
Example: element=title
Offer element for which translation should be deleted. If not provided, translations for all elements will be deleted.

products.id	
string <uuid>
Example: products.id=0e810d4a-bbee-495c-8979-866bb06d3904
ProductId for which safety information translation should be deleted. If not provided, safety information translations for all products in offer will be deleted.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Delete successful
204 No Content
401 Unauthorized
403 Forbidden

delete
/sale/offers/{offerId}/translations/{language}
Response samples
401403
Content type
application/vnd.allegro.public.v1+json

Copy
{
"error": "unauthorized",
"error_description": "Full authentication is required to access this resource"
}
Categories and parameters
Get IDs of Allegro categories
Use this resource to traverse the Allegro categories tree. It returns the list of the given category's children or a list of the main Allegro categories. Read more: PL / EN.

Authorizations:
bearer-token-for-applicationbearer-token-for-user
query Parameters
parent.id	
string
Default: "954b95b6-43cf-4104-8354-dea4d9b10ddf"
Example: parent.id=954b95b6-43cf-4104-8354-dea4d9b10ddf
The ID of the category which children should be returned. If omitted, the list of main Allegro categories will be returned.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 The list of categories returned successfully.
404 The category with the given ID does not exist.

get
/sale/categories
Response samples
200404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"categories": [
{}
]
}
Get a category by ID
Use this resource to get the details of a specific category. Read more: PL / EN.

Authorizations:
bearer-token-for-applicationbearer-token-for-user
path Parameters
categoryId
required
string
Example: 6061
The category ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 The details of a category returned successfully.
404 The category with the given ID does not exist.

get
/sale/categories/{categoryId}
Response samples
200404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "12",
"leaf": true,
"name": "Other",
"options": {
"advertisement": true,
"offersWithProductPublicationEnabled": true,
"productCreationEnabled": true,
"sellerCanRequirePurchaseComments": true
},
"parent": {
"id": "709"
}
}
Get parameters supported by a category
Use this resource to get the list of parameters that are supported by the given category. Read more: PL / EN.

Authorizations:
bearer-token-for-applicationbearer-token-for-user
path Parameters
categoryId
required
string
Example: 709
The category ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 The list of parameters for the category returned successfully.
404 The category with the given ID does not exist.

get
/sale/categories/{categoryId}/parameters
Response samples
200404
Content type
application/vnd.allegro.public.v1+json
Example

Integer
Integer

Copy
Expand allCollapse all
{
"parameters": [
{}
]
}
Get planned changes in category parameters
Use this resource to get information about planned changes in category parameters. Please note that in some cases, the returned events may finally not happen in the future. At present we support the following changes: - REQUIREMENT_CHANGE - the parameter will be required in the category. Read more: PL / EN.

Authorizations:
bearer-token-for-applicationbearer-token-for-user
query Parameters
scheduledFor.gte	
string <date-time>
Example: scheduledFor.gte=2020-11-13T12:45:20.818Z
The minimum date and time from which the change will be effective from in ISO 8601 format. Should be greater than the current date time and less than 3 months from the current date.

scheduledFor.lte	
string <date-time>
Example: scheduledFor.lte=2020-11-13T12:45:20.818Z
The maximum date and time from which the change will be effective from in ISO 8601 format. Should be greater than the current date time and less than 3 months from the current date.

scheduledAt.gte	
string <date-time>
Example: scheduledAt.gte=2020-11-13T12:45:20.818Z
The minimum date and time at which the change was scheduled in ISO 8601 format.

scheduledAt.lte	
string <date-time>
Example: scheduledAt.lte=2020-11-13T12:45:20.818Z
The maximum date and time at which the change was scheduled in ISO 8601 format.

type	
Array of strings
Items Value: "REQUIREMENT_CHANGE"
The types of changes that will be returned in the response. All types of changes are returned by default.

offset	
integer <int32> >= 0
Default: 0
The offset of elements in the response.

limit	
integer <int32> [ 1 .. 1000 ]
Default: 100
The limit of elements in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "pl-PL"
Example: pl-PL
Expected language of messages.

Responses
200 Category parameters changes returned successfully.
400 Invalid parameters supplied in the request.
401 Unauthorized

get
/sale/category-parameters-scheduled-changes
Response samples
200400401
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"scheduledChanges": [
{}
]
}
Get changes in categories
Use this resource to get information about changes in categories. It returns changes that occurred in the last 3 months. At present we support the following changes:

CATEGORY_CREATED - new category was created.
CATEGORY_RENAMED - category name has been changed.
CATEGORY_MOVED - category has been moved to a different place in category tree, category parent id field is changed.
CATEGORY_DELETED - category is no longer available, category from redirectCategory field should be used instead.
Read more: PL / EN.

Authorizations:
bearer-token-for-applicationbearer-token-for-user
query Parameters
from	
string <= 256 characters
Example: from=MTEzMjQzODU3NA
The ID of the last seen event. Changes that occurred after the given event will be returned.

limit	
integer [ 1 .. 1000 ]
Default: 100
The number of events that will be returned in the response.

type	
Array of strings
Items Enum: "CATEGORY_CREATED" "CATEGORY_RENAMED" "CATEGORY_MOVED" "CATEGORY_DELETED"
Example: type=CATEGORY_CREATED
The types of events that will be returned in the response. All types of events are returned by default.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "pl-PL"
Example: pl-PL
Expected language of messages.

Responses
200 The list of category changes returned successfully
400 Invalid parameters supplied in the request.
401 Unauthorized

get
/sale/category-events
Response samples
200400401
Content type
application/vnd.allegro.public.v1+json
Example

Category created event
Category created event

Copy
Expand allCollapse all
{
"events": [
{}
]
}
Get categories suggestions
Use this resource to receive suggested categories for given phrase. This resource is rate limited to 5 requests per second. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
name
required
string
Example: name=bmw x3
Product name for which you want to get suggested categories.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Category suggestion returned successfully.
401 Unauthorized
403 Forbidden
406 Not Acceptable
422 Unprocessable Entity

get
/sale/matching-categories
Response samples
200401403406422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"matchingCategories": [
{}
]
}
Images and attachments
Upload an offer image
Upload image to our servers. You can choose from two upload options:

- provide a link and we will download an image for you
- send an image as binary data
Important! Remember to use dedicated domain for upload, i.e.

- https://upload.allegro.pl for Production
- https://upload.allegro.pl.allegrosandbox.pl for Sandbox
Read more about the rules for photos in an offer's gallery and description: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
isAiCoCreated	
boolean
Sets the uploaded image to be marked as "AI". For a JSON request body (application/vnd.allegro.public.v1+json), this flag can also be provided in the request body. If both the query parameter and the request body are provided, their values must not conflict, otherwise a 400 response is returned.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: 
application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json
url
required
string
URL of the image. It has to contain domain name, not an IP address. Currently we support http and https protocols. When using https the certificate chain needs to be valid.

isAiCoCreated	
boolean or null
Sets the uploaded image to be marked as "AI". Optional - can be omitted or set to true/false. If the isAiCoCreated query parameter is also provided, its value must not conflict with this field, otherwise a 400 response is returned.

Responses
201 Image uploaded correctly
400 Syntactically incorrect request
401 Invalid or missing bearer token
403 Authorization problem
413 Image is too big
415 Unsupported media type
422 Unprocessable entity (problem with image server)

post
/sale/images
Request samples
Payload
Content type

application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json

Copy
{
"url": "http://upload.allegro.pl/sale/offer-attachments/e9d1bf7c-804e-4faf-9e24-b2d3aa3eda05",
"isAiCoCreated": true
}
Response samples
201400
Content type
application/vnd.allegro.public.v1+json

Copy
{
"expiresAt": "2019-08-24T14:15:22Z",
"location": "string"
}
Create an offer attachment
You can attach pdf, jpeg or png files to your offers. We will present them under the offer description in the Additional information section. You can attach multiple files to one offer – one per each type from the list:

Guide (MANUAL). Allowed media types: PDF
Special offer terms (SPECIAL_OFFER_RULES). Allowed media types: PDF
Competition terms (COMPETITION_RULES). Allowed media types: PDF
Book excerpt (BOOK_EXCERPT). Allowed media types: PDF
Manual (USER_MANUAL). Allowed media types: PDF
Installation manual (INSTALLATION_INSTRUCTIONS). Allowed media types: PDF
Game manual (GAME_INSTRUCTIONS). Allowed media types: PDF
Energy label (ENERGY_LABEL). Allowed media types: JPEG, JPG, PNG
Product information sheet (PRODUCT_INFORMATION_SHEET). Allowed media types: PDF
Tire label (TIRE_LABEL). Allowed media types: JPEG, JPG, PNG
Data processing sheet - software (SOFTWARE_DATA_PROCESSING). Allowed media types: PDF
Data processing sheet - device (HARDWARE_DATA_PROCESSING). Allowed media types: PDF
Plant Protection Products (PPPs) license (PLANT_PROTECTION_PRODUCTS_AUTHORIZATION). Allowed media types: PDF
You can attach up to 20 files to one product for:

Safety information manual (SAFETY_INFORMATION_MANUAL). Allowed media types: PDF, JPEG, JPG, PNG
Uploading attachments flow:

Create an attachment object to receive an upload URL (POST /sale/offer-attachments),
Use the upload URL to submit the file (PUT /sale/offer-attachments/{attachmentId}),
Add attachments to the offer (PATCH /sale/product-offers/{offerId}).
Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
offer attachment

type	
string (AttachmentType)
Enum: "MANUAL" "SPECIAL_OFFER_RULES" "COMPETITION_RULES" "BOOK_EXCERPT" "USER_MANUAL" "INSTALLATION_INSTRUCTIONS" "GAME_INSTRUCTIONS" "ENERGY_LABEL" "PRODUCT_INFORMATION_SHEET" "TIRE_LABEL" "SAFETY_INFORMATION_MANUAL" "SOFTWARE_DATA_PROCESSING" "HARDWARE_DATA_PROCESSING" "PLANT_PROTECTION_PRODUCTS_AUTHORIZATION"
offer attachment type

file	
object (AttachmentFileRequest)
Responses
201 Attachment created successfully
400 Syntactically incorrect request
401 Invalid or missing bearer token
415 Unsupported media type
422 Unprocessable Entity

post
/sale/offer-attachments
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"type": "MANUAL",
"file": {
"name": "abcde.pdf"
}
}
Response samples
201
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "07ee5e36-afc7-41eb-af49-3df5354ef85",
"type": "MANUAL",
"file": {
"name": "abcde.pdf",
"url": "http://upload.allegro.pl/sale/offer-attachments/e9d1bf7c-804e-4faf-9e24-b2d3aa3eda05"
}
}
Upload an offer attachment
Upload an offer attachment. This operation should be used after creating an offer attachment with POST /sale/offer-attachments Important! You can find the URL address to upload the file to our server in the Location response header of POST /sale/offer-attachments. The URL is unique and one-time. As its format may change in time, you should always use the address from the header. Do not compose the address on your own. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
attachmentId
required
string
The ID of the attachment.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: 
application/pdf
application/pdf
string <binary>
File in a binary format

Responses
200 File uploaded correctly
400 Syntactically incorrect request
401 Invalid or missing bearer token
415 Unsupported media type

put
/sale/offer-attachments/{attachmentId}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "07ee5e36-afc7-41eb-af49-3df5354ef85",
"type": "MANUAL",
"file": {
"name": "abcde.pdf",
"url": "http://upload.allegro.pl/sale/offer-attachments/e9d1bf7c-804e-4faf-9e24-b2d3aa3eda05"
}
}
Get offer attachment details
Get details of an offer attachments, including download link, by attachment identifier ("attachmentId"). The attachment id can be retrieved by querying a particular offer, for example by using GET /sale/product-offers/{offerId}. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
attachmentId
required
string
The ID of the attachment.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Offer attachment details
403 User has no access to an attachment
404 Non existing attachment

get
/sale/offer-attachments/{attachmentId}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "07ee5e36-afc7-41eb-af49-3df5354ef85",
"type": "MANUAL",
"file": {
"name": "abcde.pdf",
"url": "http://upload.allegro.pl/sale/offer-attachments/e9d1bf7c-804e-4faf-9e24-b2d3aa3eda05"
}
}
Products
Get product parameters available in given category
Use this resource to get the list of product parameters available in given category. You can use these parameters to create a new product. Read more: PL / EN.

Authorizations:
bearer-token-for-applicationbearer-token-for-user
path Parameters
categoryId
required
string
Example: 709
The category ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 The list of product parameters for the category returned successfully.
404 The category with the given ID does not exist.

get
/sale/categories/{categoryId}/product-parameters
Response samples
200404
Content type
application/vnd.allegro.public.v1+json
Example

Integer
Integer

Copy
Expand allCollapse all
{
"parameters": [
{}
]
}
Get search products results
Use this resource to get a list of products according to provided parameters. At least ean or phrase parameter is required. Read more: PL / EN. This resource is limited with Leaky Bucket mechanism, read more PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
phrase	
string <= 1024 characters
Search phrase.

mode	
string
Enum: "GTIN" "MPN"
Search mode. If not specified, we are searching by GTIN, MPN, product's name, parameters, etc.

GTIN - restricts the search filtering to GTINs (Global Trade Item Number), e.g. EAN, ISBN, UPC.
MPN - restricts the search filtering to MPNs (Manufacturer Part Number).
language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: language=en-US
Language indicates the language for searching products. Allows to specify the language of the given phrase.

category.id	
string
The category identifier to filter results. This can only be used when searching by phrase.

Dynamic filters	
object
You can filter and customize your search results to find exactly what you need by applying filters ids and their dictionary values to query according to the flowing pattern: id=value. When the filter definition looks like:

{
  "id": "127448",
  "name": "Kolor",
  "type": "SINGLE",
  "values": [
    {
      "name": "biały",
      "value": "127448_2"
    },
    {
      "name": "czarny",
      "value": "127448_1"
    }
  ]
}
You can use 'Kolor' filter to query results, i.e.:

127448=127448_2 for "biały"
127448=127448_1 for "czarny".
page.id	
string
A "cursor" to the next set of results.

searchFeatures	
string
Value: "SIMILAR_CATEGORIES"
Enables additional search options: - SIMILAR_CATEGORIES - searching in the indicated category (category.id) and in 'similar categories' (works only if category.id is a leaf category).

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Successful operation.
400 Bad request
401 Unauthorized
422 One of parameters have invalid value.

get
/sale/products
Response samples
200400401422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"products": [
{}
],
"categories": {
"subcategories": [],
"path": []
},
"filters": [
{}
],
"nextPage": {
"id": "AoMhVAhDSexYPwUxOTA4YTMwZC02NDQ2LTRhNWUtYTU1Yy1iY2I4ZTdkNTNjYmI%3D"
}
}
Get all data of the particular product
Use this resource to retrieve all data of the particular product. Read more: PL / EN. This resource is limited with Leaky Bucket mechanism.

Authorizations:
bearer-token-for-user
path Parameters
productId
required
string
The product identifier.

query Parameters
category.id	
string
The similar category identifier. You can choose a category from 'similar categories' to filter the list of parameters available in the category context.

language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: language=en-US
The language version of product. You can indicate the language for the returned product data.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Product returned successfully
401 Unauthorized
404 A product's not found or language version of the product is currently unavailable.
422 One of parameters have invalid value.

get
/sale/products/{productId}
Response samples
200401404422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "c9e39cae-9cb6-11e9-a2a3-2a2ae2dbcce4",
"name": "iPhone 5s",
"category": {
"id": "257931",
"path": [],
"similar": []
},
"images": [
{}
],
"parameters": [
{}
],
"offerRequirements": {
"id": "2865624934",
"parameters": []
},
"compatibilityList": {
"id": "460b2511-b786-47b9-9d7e-1f868728cfd6-f103931434fbf4aa06764f3df74d371df23aa138a9cd46dbe570f51af79db1c4-2",
"type": "PRODUCT_BASED",
"items": []
},
"tecdocSpecification": {
"id": "470b8513-b786-b7b9-9e7e-2f848729cfd6",
"items": []
},
"description": {
"sections": []
},
"aiCoCreatedContent": {
"images": [],
"paths": []
},
"trustedContent": {
"paths": [],
"productPaths": []
},
"hasProtectedBrand": true,
"publication": {
"status": "PROPOSED"
},
"productSafety": {
"responsibleProducers": [],
"safetyInformation": {}
}
}
Propose a product
Use this resource to propose a product. You can add up to 20,000 new products to the Catalog each month. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
name
required
string <= 75 characters
Suggested product name.

category
required
object (ProductCategory)
Product category

images
required
Array of objects (ImageUrl)
List of product images. At least one image is required.

parameters
required
Array of objects (ProductParameter)
List of product parameters.

description	
object (StandardizedDescription)
The description section cannot have more than 40000 bytes in length.

language
required
string <BCP-47 language code>
Language of provided product data (name, description, parameters's values).

Responses
201 Product proposed successfully.
400 Bad request
401 Unauthorized
403 Forbidden - not allowed to access.
409 Product already exists. Url of the existing product is provided in the HTTP Location header field of the response.
422 Unprocessable Entity

post
/sale/product-proposals
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"name": "iPhone 5s",
"category": {
"id": "257931"
},
"images": [
{}
],
"parameters": [
{}
],
"description": {
"sections": []
},
"language": "pl-PL"
}
Response samples
201400401403409422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "c9e39cae-9cb6-11e9-a2a3-2a2ae2dbcce4",
"name": "iPhone 5s",
"category": {
"id": "257931",
"similar": []
},
"images": [
{}
],
"parameters": [
{}
],
"description": {
"sections": []
},
"aiCoCreatedContent": {
"images": [],
"paths": []
},
"language": "pl-PL",
"publication": {
"status": "LISTED"
}
}
Propose changes in product
Use this resource to propose changes in product. Read more: PL / EN. This resource is limited to 100 suggestions per day for a single user.

Authorizations:
bearer-token-for-user
path Parameters
productId
required
string
The product identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
name
required
string <= 150 characters
Proposed product name.

note	
string <= 500 characters
Note about product changes proposal.

category
required
object (ProductCategory)
Product category

images
required
Array of objects (ImageUrl)
List of product images. At least one image is required.

parameters
required
Array of objects (ProductParameter)
List of product parameters.

notifyViaEmailAfterVerification	
boolean
Receive an email notification after product changes proposal resolution.

language
required
string <BCP-47 language code>
Default: "pl-PL"
Language of provided proposal data.

Responses
201 Product changes proposed successfully.
400 Bad request.
401 Unauthorized.
404 Product with the given Id not found.
422 Unprocessable Entity.

post
/sale/products/{productId}/change-proposals
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"name": "iPhone 5s",
"note": "Some additional note to product changes proposal.",
"category": {
"id": "257931"
},
"images": [
{}
],
"parameters": [
{}
],
"notifyViaEmailAfterVerification": true,
"language": "en-US"
}
Response samples
201400401404422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "22f1ed1b-4108-4bbe-914c-456588b9dac9",
"name": {
"current": "Samsung S25",
"proposal": "Samsung S25 Ultra",
"reason": "It is Ultra version",
"resolutionType": "ACCEPTED"
},
"category": {
"current": "1234",
"proposal": "3214",
"reason": "It is different producer",
"resolutionType": "ACCEPTED"
},
"note": "Some additional note to product changes proposal.",
"images": [
{}
],
"parameters": [
{}
],
"notifyViaEmailAfterVerification": true,
"language": "pl-PL"
}
Get all data of the particular product changes proposal
Use this resource to retrieve all data of the particular product changes proposal. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
changeProposalId
required
string
The product changes proposal identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Product changes proposal returned successfully.
401 Unauthorized.
403 You do not have permission to access change proposal that not belong to you
404 Not Found.

get
/sale/products/change-proposals/{changeProposalId}
Response samples
200401403404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "22f1ed1b-4108-4bbe-914c-456588b9dac9",
"name": {
"current": "Samsung S25",
"proposal": "Samsung S25 Ultra",
"reason": "It is Ultra version",
"resolutionType": "ACCEPTED"
},
"category": {
"current": "1234",
"proposal": "3214",
"reason": "It is different producer",
"resolutionType": "ACCEPTED"
},
"note": "Some additional note to product changes proposal.",
"images": [
{}
],
"parameters": [
{}
],
"notifyViaEmailAfterVerification": true,
"language": "pl-PL"
}
Batch offer modification
Batch offer modification
Use this resource to modify multiple offers at once. Read more: PL / EN. This resource is rate limited to 250 000 offer changes per hour or 9000 offer changes per minute - limit applies to a single user of the application.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
offerChangeCommandDto

modification	
object (Modification)
Contains fields to change

offerCriteria	
Array of objects (OfferCriterium)
List of offer criteria

Responses
201 Command was registered
400 Semantically incorrect request or provided conditions not correct
401 Unauthorized
403 Forbidden
404 Not Found
409 Command id was already used
422 Unprocessable Entity

put
/sale/offer-modification-commands/{commandId}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"modification": {
"additionalServicesGroup": {},
"delivery": {},
"discounts": {},
"location": {},
"payments": {},
"sizeTable": {},
"publication": {},
"responsiblePerson": {},
"responsibleProducer": {},
"safetyInformation": {}
},
"offerCriteria": [
{}
]
}
Response samples
201
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "b9b8ef16-2709-411e-ac94-2be7e3ba25e7",
"createdAt": "2017-05-17T08:36:57.292Z",
"completedAt": "2017-05-17T08:36:57.292Z",
"taskCount": {
"failed": 0,
"success": 0,
"total": 0
}
}
Modification command summary
Use this resource to find out how many offers were edited within one {commandId}. You will receive a summary with a number of successfully edited offers. Read more: PL / EN. This resource is rate limited to retrieving information about 270 000 offer changes per minute.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 report was generated and successfully returned
401 Unauthorized
403 Forbidden
404 Command not found

get
/sale/offer-modification-commands/{commandId}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "b9b8ef16-2709-411e-ac94-2be7e3ba25e7",
"createdAt": "2017-05-17T08:36:57.292Z",
"completedAt": "2017-05-17T08:36:57.292Z",
"taskCount": {
"failed": 0,
"success": 0,
"total": 0
}
}
Modification command detailed report
Use this resource to retrieve a detailed summary of changes introduced within one {commandId} (defaults: limit = 100, offset = 0). Read more: PL / EN. This resource is rate limited to retrieving information about 270 000 offer changes per minute.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command identifier.

query Parameters
limit	
integer <int32> [ 1 .. 1000 ]
Default: 100
The limit of elements in the response.

offset	
integer <int32> [ 0 .. 999 ]
Default: 0
The offset of elements in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Task status successfully returned
400 Bad request
401 Unauthorized
403 Forbidden
404 Command not found
422 Unprocessable Entity

get
/sale/offer-modification-commands/{commandId}/tasks
Response samples
200400
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"tasks": [
{}
]
}
Batch offer price modification
Change price of offers. Read more: PL / EN. This resource is rate limited to 150 000 offer changes per hour or 9000 offer changes per minute - limit applies to a single user of the application.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
offerPriceChangeCommandDto

modification	
object (PriceModification)
The way the offer price should be changed. One of three ways is possible: new price, increase/decrease price, percentage change and only one can be chosen at once.

offerCriteria	
Array of objects (OfferCriterium)
List of offer criteria

Responses
201 Command was registered
400 Semantically incorrect request or provided conditions not correct
401 Unauthorized
409 Command id was already used
422 Unprocessable Entity

put
/sale/offer-price-change-commands/{commandId}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"modification": {
"type": "string",
"marketplaceId": "allegro-pl"
},
"offerCriteria": [
{}
]
}
Response samples
201
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "b9b8ef16-2709-411e-ac94-2be7e3ba25e7",
"createdAt": "2017-05-17T08:36:57.292Z",
"completedAt": "2017-05-17T08:36:57.292Z",
"taskCount": {
"failed": 0,
"success": 0,
"total": 0
}
}
Change price command summary
Returns status and summary of particular command execution. Read more: PL / EN. This resource is rate limited to retrieving information about 270 000 offer changes per minute.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 report was generated and successfully returned
401 Unauthorized
404 Command not found

get
/sale/offer-price-change-commands/{commandId}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "b9b8ef16-2709-411e-ac94-2be7e3ba25e7",
"createdAt": "2017-05-17T08:36:57.292Z",
"completedAt": "2017-05-17T08:36:57.292Z",
"taskCount": {
"failed": 0,
"success": 0,
"total": 0
}
}
Change price command detailed report
Defaults: limit = 100, offset = 0. Read more: PL / EN. This resource is rate limited to retrieving information about 270 000 offer changes per minute.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command identifier.

query Parameters
limit	
integer <int32> [ 1 .. 1000 ]
Default: 100
The limit of elements in the response.

offset	
integer <int32> [ 0 .. 999 ]
Default: 0
The offset of elements in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Task status successfully returned
400 Bad request
401 Unauthorized
404 Command not found
422 Unprocessable Entity

get
/sale/offer-price-change-commands/{commandId}/tasks
Response samples
200400
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"tasks": [
{}
]
}
Batch offer price and stock modification (beta)
Bulk price and stock modification. Contrary to standard batch price or stock modification, it lets you modify both price and stock modification across multiple offers, or within the same offer but in a separate modification unit.
Change price and stock of offers. Read more: PL / EN.
This resource is rate limited to 150 000 offer changes per hour or 9000 offer changes per minute - limit applies to a single user of the application.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.beta.v1+json
offerBulkChangeCommandDto

commandId
required
string <uuid>
The unique identifier for the command.

modifications
required
Array of objects (OfferBulkModification) [ 1 .. 25 ] items
A list of modifications price or stock to apply to offers. Multiple modifications of the same type for the same offerId are not allowed (eg. price and offerId).

Responses
201 Command was registered
400 Semantically incorrect request or provided conditions not correct
401 Unauthorized
409 Command id was already used
422 Unprocessable Entity

post
/sale/offer-bulk-modification-commands
Request samples
Payload
Content type
application/vnd.allegro.beta.v1+json

Copy
Expand allCollapse all
{
"commandId": "c1b3f63d-d293-4333-911d-a0c1053e2c81",
"modifications": [
{},
{}
]
}
Response samples
201
Content type
application/vnd.allegro.beta.v1+json

Copy
Expand allCollapse all
{
"id": "b9b8ef16-2709-411e-ac94-2be7e3ba25e7",
"createdAt": "2017-05-17T08:36:57.292Z",
"completedAt": "2017-05-17T08:36:57.292Z",
"taskCount": {
"failed": 0,
"success": 0,
"total": 0
}
}
Batch price and stock command summary (beta)
Returns status and summary of particular command execution. Read more: PL / EN. This resource is rate limited to retrieving information about 270 000 offer changes per minute.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 report was generated and successfully returned
401 Unauthorized
404 Command not found

get
/sale/offer-bulk-modification-commands/{commandId}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "b9b8ef16-2709-411e-ac94-2be7e3ba25e7",
"createdAt": "2017-05-17T08:36:57.292Z",
"completedAt": "2017-05-17T08:36:57.292Z",
"taskCount": {
"failed": 0,
"success": 0,
"total": 0
}
}
Batch price and stock command detailed report (beta)
Defaults: limit = 100, offset = 0. Read more: PL / EN. This resource is rate limited to retrieving information about 270 000 offer changes per minute.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command identifier.

query Parameters
limit	
integer <int32> [ 1 .. 1000 ]
Default: 100
The limit of elements in the response.

offset	
integer <int32> [ 0 .. 999 ]
Default: 0
The offset of elements in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Task status successfully returned
400 Bad request
401 Unauthorized
404 Command not found
422 Unprocessable Entity

get
/sale/offer-bulk-modification-commands/{commandId}/tasks
Response samples
200400
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"tasks": [
{}
]
}
Batch offer quantity modification
Change quantity of multiple offers. Read more: PL / EN. This resource is rate limited to 250 000 offer changes per hour or 9000 offer changes per minute - limit applies to a single user of the application.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
offerQuantityChangeCommandDto

modification	
object (QuantityModification)
The way the offer quantity should be changed. One of two ways is possible: new quantity, increase/decrease quantity and only one can be chosen at once.

offerCriteria	
Array of objects (OfferCriterium)
List of offer criteria

Responses
201 Command was registered
400 Semantically incorrect request or provided conditions not correct
401 Unauthorized
409 Command id was already used
422 Unprocessable Entity

put
/sale/offer-quantity-change-commands/{commandId}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"modification": {
"changeType": "FIXED",
"value": 1
},
"offerCriteria": [
{}
]
}
Response samples
201
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "b9b8ef16-2709-411e-ac94-2be7e3ba25e7",
"createdAt": "2017-05-17T08:36:57.292Z",
"completedAt": "2017-05-17T08:36:57.292Z",
"taskCount": {
"failed": 0,
"success": 0,
"total": 0
}
}
Change quantity command summary
Returns status and summary of the command. Read more: PL / EN. This resource is rate limited to retrieving information about 270 000 offer changes per minute.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Report was generated and successfully returned
401 Unauthorized
404 Command not found

get
/sale/offer-quantity-change-commands/{commandId}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "b9b8ef16-2709-411e-ac94-2be7e3ba25e7",
"createdAt": "2017-05-17T08:36:57.292Z",
"completedAt": "2017-05-17T08:36:57.292Z",
"taskCount": {
"failed": 0,
"success": 0,
"total": 0
}
}
Change quantity command detailed report
Defaults: limit = 100, offset = 0. Read more: PL / EN. This resource is rate limited to retrieving information about 270 000 offer changes per minute.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command identifier.

query Parameters
limit	
integer <int32> [ 1 .. 1000 ]
Default: 100
The limit of elements in the response.

offset	
integer <int32> [ 0 .. 999 ]
Default: 0
The offset of elements in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Task status successfully returned
400 Bad request
401 Unauthorized
404 Command not found
422 Unprocessable Entity

get
/sale/offer-quantity-change-commands/{commandId}/tasks
Response samples
200400
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"tasks": [
{}
]
}
Batch offer automatic pricing rules modification
Use this resource to modify the automatic pricing rules of multiple offers at the same time. Read more: PL / EN. This resource is rate limited to 150 000 offer changes per hour or 9000 offer changes per minute - limit applies to a single user of the application.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
OfferAutomaticPricingCommand

id	
string <uuid>
The Command identifier. This field is optional. If the client does not provide their own command id then the service will generate a command id and return it in the response.

modification
required
OfferAutomaticPricingModificationSet (object) or OfferAutomaticPricingModificationRemove (object)
offerCriteria
required
Array of objects (OfferCriterium)
List of offer criteria.

Responses
201 Command was registered
400 Semantically incorrect request or provided conditions not correct
401 Unauthorized
403 Forbidden
409 Command id was already used
422 Unprocessable Entity

post
/sale/offer-price-automation-commands
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "123a08d7-ab9b-460d-b9cb-d6ed64b3a018",
"modification": {
"set": []
},
"offerCriteria": [
{}
]
}
Response samples
201
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "b9b8ef16-2709-411e-ac94-2be7e3ba25e7",
"createdAt": "2017-05-17T08:36:57.292Z",
"completedAt": "2017-05-17T08:36:57.292Z",
"taskCount": {
"failed": 0,
"success": 0,
"total": 0
}
}
Automatic pricing command summary
Returns status and summary of the offer-price-automation-command. Read more: PL / EN. This resource is rate limited to retrieving information about 270 000 offer changes per minute.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 report was generated and successfully returned
401 Unauthorized
403 Forbidden
404 Command not found

get
/sale/offer-price-automation-commands/{commandId}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "b9b8ef16-2709-411e-ac94-2be7e3ba25e7",
"createdAt": "2017-05-17T08:36:57.292Z",
"completedAt": "2017-05-17T08:36:57.292Z",
"taskCount": {
"failed": 0,
"success": 0,
"total": 0
}
}
Automatic pricing command detailed report
Defaults: limit = 100, offset = 0. Returns status and report of the offer-price-automation-command. Read more: PL / EN. This resource is rate limited to retrieving information about 270 000 offer changes per minute.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command identifier.

query Parameters
limit	
integer <int32> [ 1 .. 1000 ]
Default: 100
The limit of elements in the response.

offset	
integer <int32> [ 0 .. 999 ]
Default: 0
The offset of elements in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Task status successfully returned
400 Bad request
401 Unauthorized
403 Forbidden
404 Command not found
422 Unprocessable Entity

get
/sale/offer-price-automation-commands/{commandId}/tasks
Response samples
200400
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"tasks": [
{}
]
}
Automatic pricing
Get automatic pricing rules
Use this resource to get automatic pricing rules. Rules with property default set to true are default rules created by Allegro for each merchant. This resource is rate limited to 5 requests per second. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 The list of automatic pricing rules returned successfully.
401 Unauthorized
403 Forbidden

get
/sale/price-automation/rules
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"rules": [
{},
{},
{},
{}
]
}
Post automatic pricing rule
Use this resource to create automatic pricing rule. This resource is rate limited to 5 requests per second. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
The automatic pricing rule.

name
required
string (AutomaticPricingRuleName) <= 33 characters
The rule name. Default rule names are automatically translated based on the value provided in the the "Accept-Language" header.

type
required
string (AutomaticPricingRuleType)
Enum: "EXCHANGE_RATE" "FOLLOW_BY_ALLEGRO_MIN_PRICE" "FOLLOW_BY_MARKET_MIN_PRICE" "FOLLOW_BY_TOP_OFFER_PRICE"
The rule type.

EXCHANGE_RATE - Calculates prices on additional marketplaces using the latest exchange rates and price from the offer base marketplace.
Is not available on base marketplace and business marketplaces.
More information about EXCHANGE_RATE type.
FOLLOW_BY_ALLEGRO_MIN_PRICE - Calculates prices by following the lowest product price on Allegro for a given marketplace.
Is not available on business marketplaces.
More information about FOLLOW_BY_ALLEGRO_MIN_PRICE type.
FOLLOW_BY_MARKET_MIN_PRICE - Calculates prices by following the lowest product price on market for a given marketplace.
Is not available on business marketplaces.
More information about FOLLOW_BY_MARKET_MIN_PRICE type.
FOLLOW_BY_TOP_OFFER_PRICE - Calculates prices by following the top offer price on market for a given marketplace.
Is not available on business marketplaces.
More information about FOLLOW_BY_TOP_OFFER_PRICE type.
configuration	
(AutomaticPricingRuleConfigurationChangeByAmount (object or null)) or (AutomaticPricingRuleConfigurationChangeByPercentage (object or null)) (AutomaticPricingRuleConfiguration)
Responses
201 The automatic pricing rules created.
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict - rule with that name already exists for this seller

post
/sale/price-automation/rules
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json
Example

Without configuration
Without configuration

Copy
{
"name": "My price on Allegro",
"type": "FOLLOW_BY_ALLEGRO_MIN_PRICE"
}
Response samples
201
Content type
application/vnd.allegro.public.v1+json
Example

Without configuration
Without configuration

Copy
{
"id": "641c73feaef0a8281a3d11f8",
"type": "FOLLOW_BY_ALLEGRO_MIN_PRICE",
"name": "My price on Allegro",
"default": false,
"updatedAt": "2023-03-23T15:45:02Z"
}
Get automatic pricing rule by id
Use this resource to get automatic pricing rule by id. Rules with property default set to true are default rules created by Allegro for each merchant and cannot be modified. This resource is rate limited to 5 requests per second. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
ruleId
required
string
Example: 66466e2b07ba0029b829f08d
The rule identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 The automatic pricing rule returned successfully.
401 Unauthorized
404 Not Found

get
/sale/price-automation/rules/{ruleId}
Response samples
200
Content type
application/vnd.allegro.public.v1+json
Example

Without configuration
Without configuration

Copy
{
"id": "641c73feaef0a8281a3d11f5",
"type": "FOLLOW_BY_ALLEGRO_MIN_PRICE",
"name": "My price on Allegro",
"default": false,
"updatedAt": "2023-03-23T15:45:02Z"
}
Edit automatic pricing rule
Use this resource to update automatic pricing rule. This resource is rate limited to 5 requests per second. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
ruleId
required
string
Example: 66466e2b07ba0029b829f08d
The rule identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
The automatic pricing rule.

name
required
string (AutomaticPricingRuleName) <= 33 characters
The rule name. Default rule names are automatically translated based on the value provided in the the "Accept-Language" header.

configuration	
(AutomaticPricingRuleConfigurationChangeByAmount (object or null)) or (AutomaticPricingRuleConfigurationChangeByPercentage (object or null)) (AutomaticPricingRuleConfiguration)
Responses
200 The automatic pricing rule updated.
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict - rule with that name already exists for this seller

put
/sale/price-automation/rules/{ruleId}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json
Example

Without configuration
Without configuration

Copy
{
"name": "My price on Allegro"
}
Response samples
200
Content type
application/vnd.allegro.public.v1+json
Example

Without configuration
Without configuration

Copy
{
"id": "641c73feaef0a8281a3d11c8",
"type": "FOLLOW_BY_ALLEGRO_MIN_PRICE",
"name": "My price on Allegro",
"default": false,
"updatedAt": "2023-03-23T15:45:02Z"
}
Delete automatic pricing rule
Use this resource to delete automatic pricing rule. This resource is rate limited to 5 requests per second. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
ruleId
required
string
Example: 66466e2b07ba0029b829f08d
The rule identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
204 The automatic pricing rules deleted.
401 Unauthorized
403 Forbidden
404 Not Found

delete
/sale/price-automation/rules/{ruleId}
Get automatic pricing rules assigned to the offer
Use this resource to get automatic pricing rules for offer. This resource is rate limited to 5 requests per second. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
offerId
required
string
Example: 15521818197
The offer identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 The list of automatic pricing rules assigned to offer returned successfully
401 Unauthorized
403 Forbidden
404 Not Found

get
/sale/price-automation/offers/{offerId}/rules
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"rules": [
{}
],
"updatedAt": "2023-03-23T15:45:02Z"
}
Offer tags
Tags are only available to sellers registered on allegro.pl and can only be assigned to offers with base marketplace allegro-pl.

Create a tag
Use this resource to create a new tag. You can create up to 100 tags. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
request

name
required
string [ 1 .. 25 ] characters
hidden	
boolean
Responses
200 Successfully created the requested tag
400 Bad request
401 Unauthorized action
403 User is not brandzone user and doesn't have tags subscription
422 Validation failed - your request was correct, but the tag could not be created.

post
/sale/offer-tags
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
{
"name": "Shoes",
"hidden": false
}
Response samples
200400401403422
Content type
application/vnd.allegro.public.v1+json

Copy
{
"id": "500fedd3-2140-4225-87d4-a22484222776"
}
Get the user's tags
Use this resource to get a list of tags defined by the specified user (Defaults: limit = 1000, offset = 0). Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
limit	
integer <int32> [ 1 .. 1000 ]
Default: 1000
The limit of elements in the response.

offset	
integer <int32> >= 0
Default: 0
The offset of elements in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Successfully returned the requested list of tags
401 Unauthorized action
403 User is not brandzone user and doesn't have tags subscription

get
/sale/offer-tags
Response samples
200401403
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"tags": [
{}
]
}
Delete a tag
Use this resource to delete the tag. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
tagId
required
string
Tag identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
204 Successfully deleted tag
401 Unauthorized action
403 User is not brandzone user and doesn't have tags subscription
404 Tag not found

delete
/sale/offer-tags/{tagId}
Response samples
401403
Content type
application/vnd.allegro.public.v1+json

Copy
{
"error": "unauthorized",
"error_description": "Full authentication is required to access this resource"
}
Modify a tag
Use this resource to update a tag. Read more: PL / EN. This resource is rate limited to 1 million changes per hour.

Authorizations:
bearer-token-for-user
path Parameters
tagId
required
string
Tag identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
request

name
required
string [ 1 .. 25 ] characters
hidden	
boolean
Responses
200 Successfully updated the requested tag
401 Unauthorized action
403 User is not brandzone user and doesn't have tags subscription
404 Tag not found
422 Validation failed - your request was correct, but the tag could not be updated.

put
/sale/offer-tags/{tagId}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
{
"name": "Shoes",
"hidden": false
}
Response samples
401403404422
Content type
application/vnd.allegro.public.v1+json

Copy
{
"error": "unauthorized",
"error_description": "Full authentication is required to access this resource"
}
Assign tags to an offer
Use this resource to assign a tag to offer. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
offerId
required
string
Offer identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
request

tags
required
Array of objects (TagId)
Responses
200 Successfully assigned tag to offer
400 Bad request
401 Unauthorized action
403 Forbidden - offer is created by someone else or user is not brandzone user or doesn't have tags subscription
404 Offer not found
422 Validation failed - your request was correct, but the tag could not be assigned.

post
/sale/offers/{offerId}/tags
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"tags": [
{}
]
}
Response samples
400401403404422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"errors": [
{}
]
}
Get tags assigned to an offer
Use this resource to get a list of tags assigned to offer. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
offerId
required
string
Offer identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Successfully returned list of assigned tags
401 Unauthorized action
403 User is not brandzone user and doesn't have tags subscription
404 Not found

get
/sale/offers/{offerId}/tags
Response samples
200401403404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"tags": [
{}
]
}
Tax settings
Get all tax settings for category
Use this resource to receive tax settings for a given leaf category. Based on received settings you may set VAT tax settings for your offers. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
category.id
required
string
Example: category.id=316194
An identifier of a leaf category for which all available tax settings will be returned.

countryCode	
Array of strings
Items Enum: "PL" "CZ" "SK" "HU" "LT"
Example: countryCode=PL
Country code for which tax settings will be returned. If not provided settings for all countries will be returned.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Tax settings for given category returned successfully
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
406 Not Acceptable

get
/sale/tax-settings
Response samples
200400401403404406
Content type

application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"subjects": [
{}
],
"rates": [
{}
],
"exemptions": [
{}
]
}
Compatibility List
Get list of categories where compatibility list is supported
Compatibility list is available in particular categories, this resource allows to get the list of these categories with additional details. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Configuration of supported categories.
401 Unauthorized

get
/sale/compatibility-list/supported-categories
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"supportedCategories": [
{},
{},
{},
{}
]
}
Get suggested compatibility list.
Resource allows to fetch compatibility list suggestion for given offer or product. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
offer.id	
string
Offer id on the basis of which we will return the suggested compatibility list.

product.id	
string
Product id on the basis of which we will return the suggested compatibility list.

language	
string
Example: language=pl-PL
Locale on the basis of which we will return the suggested compatibility list. For product-based suggestions if missing pl-PL will be used. For offer-based suggestions if missing offer language will be used.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Compatibility list suggestion returned successfully.
400 Bad request.
401 Unauthorized.
404 Suggestion was not found.

get
/sale/compatibility-list-suggestions
Response samples
200400401404
Content type
application/vnd.allegro.public.v1+json
Example

MANUAL
MANUAL

Copy
Expand allCollapse all
{
"type": "MANUAL",
"items": [
{}
]
}
Get list of compatible product groups
Compatible products are organized in groups, this resource allows to browse these groups. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
type
required
string
Example: type=CAR
Type of compatible products. You can find available types in the response for the GET supported-categories resource. You can use value provided in itemsType, for categories where inputType=ID.

limit	
integer [ 1 .. 200 ]
Default: 200
The limit of returned items.

offset	
integer >= 0
Default: 0
The offset of returned items.

header Parameters
If-Modified-Since	
string <<day-name>, <day> <month> <year> <hour>:<minute>:<second> GMT>
Example: Sat, 01 Dec 2018 10:00:00 GMT
Date of last data modification. If data has been modified after specified date, full set of data is returned. If header is not specified, full set of data is returned. Date has to be provided in HTTP-date format.

Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Groups of compatible products returned successfully.
304 Data has not been modified after the date provided in If-Modified-Since header.
400 Bad request
401 Unauthorized
422 Validation failed - for example type that was used is not supported

get
/sale/compatible-products/groups
Response samples
200400422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"groups": [
{},
{},
{}
],
"count": 3,
"totalCount": 256
}
Get list of compatible products
Resource allows to fetch compatible products of given type. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
type
required
string
Example: type=CAR
Type of compatible products. You can find available types in the response for the GET supported-categories resource. You can use value provided in itemsType, for categories where inputType=ID.

group.id	
string
Group identifier from /sale/compatible-products/groups resource. Parameter is required when parameter tecdoc.kTypNr or tecdoc.nTypNr or phrase is not specified.

tecdoc.kTypNr	
string
Identifier of passenger vehicle (kTypNr) from TecDoc database. When used, group.id parameter is ignored.

tecdoc.nTypNr	
string
Identifier of commercial vehicle (nTypNr) from TecDoc database. When used, group.id parameter is ignored.

phrase	
string
Query for compatible products. When used, parameters: group.id, limit, offset and header If-Modified-Since are ignored.

limit	
integer [ 1 .. 200 ]
Default: 200
The limit of returned items. If phrase parameter is present, parameter is ignored and maximum value is set to 200.

offset	
integer >= 0
Default: 0
The offset of returned items. If phrase parameter is present, parameter is ignored.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

If-Modified-Since	
string <<day-name>, <day> <month> <year> <hour>:<minute>:<second> GMT>
Example: Sat, 01 Dec 2018 10:00:00 GMT
Date of last data modification. If data has been modified after specified date, full set of data is returned. If header is not specified, full set of data is returned. Date has to be provided in HTTP-date format. Header is ignored if phrase parameter is used.

Responses
200 Compatible products returned successfully.
304 Data has not been modified after the date provided in If-Modified-Since header.
400 Bad request
401 Unauthorized
422 Validation failed - for example invalid format of If-Modified-Since header was passed

get
/sale/compatible-products
Response samples
200400422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"compatibleProducts": [
{}
],
"count": 1,
"totalCount": 1448
}
Rebates and promotions
Create a new promotion
This endpoint creates a new promotion. You can create promotions only if your base marketplace is allegro-pl. Created promotions are visible only on the allegro-pl marketplace. You can define the following types of promotions:

Large order discount
Only company users will see and be eligible for this type of promotion. In order to create a large order discount, you also have to be a company user. Furthermore, you are allowed to have only one active order discount at a time. Define a promotion with a single benefit of type LARGE_ORDER_DISCOUNT and a single criterion of type ALL_OFFERS. The benefit specification should contain a list of order value based discount thresholds. Threshold's order value defines the minimum total value of an order for which the threshold is applicable (lowerBound). Threshold's discount defines the discount percentage applied when the threshold is applied. The percentage's fractional part must be equal to 0. Only the highest applicable threshold (if any) will be applied to the total value of the order. A threshold with a higher order value than another threshold in the order discount must also have a higher discount. Large order discount is assigned automatically to all seller's offers. Moreover, it will be assigned to all newly added seller's offers once activated. Please note that it may take some time to propagate this type of promotion to all of your offers. Read more: PL / EN.
Wholesale price list
Only company users will see and be eligible for this type of promotion. In order to create a wholesale price list, you also have to be a company user. Define a promotion with a single benefit of type WHOLESALE_PRICE_LIST and a single criterion of type OFFERS_ASSIGNED_EXTERNALLY. The benefit specification should contain a name (it will be visible to you only) and a list of quantity based discount thresholds. Threshold's quantity defines the minimum number of units of an offer for which the threshold is applicable (lowerBound). Threshold's discount defines the discount percentage applied when the threshold is applied. The percentage's fractional part must be equal to 0. Only the highest applicable threshold (if any) will be applied to the total price of units of the offer bought. A threshold with a higher quantity than another threshold in the price list must also have a higher discount. In order to assign offers to a wholesale price list, use discounts field in batch offer modification. Read more: PL / EN.
Multipack
In order to create a new multipack, you have to define a promotion with a single benefit of type UNIT_PERCENTAGE_DISCOUNT and a single criterion of type CONTAINS_OFFERS. The benefit specification should contain a configuration section with a percentage which indicates the specific discount for the discounted offer. This percentage should be an integer value greater than 15 for quantity 2, greater than 30 for quantity 3, greater than 40 for quantity 4, greater than 50 for quantity 5 and lower than or equal to 100. The specification should also contain a trigger section with a field forEachQuantity that defines the amount of items in the multipack which is necessary to trigger the benefit. Additionally, the discountedNumber field must be set to 1 by default as you can only discount one unit in a multipack. Finally, the offer criterion specifies the offer for which the multipack promotion will take effect. Read more: PL / EN
Cross-offer multipack
A cross-offer multipack is created in the same fashion as a standard multipack. The only difference is that you need to pass more than 1 offer in the offer criterion section. This group of offers is then considered as a pool from which users can pick and choose forEachQuantity offers and the cheapest of them gets a discount.
Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
benefits
required
Array of objects (Benefit)
What kind of rebate will be given

offerCriteria
required
Array of objects (SellerRebateOfferCriterion)
What offers will be included

Responses
201 Successfully created the requested promotion
400 Bad request
401 Unauthorized action
403 Forbidden action
404 Offer/Offers not found
412 Validation failed – request had correct syntax, but promotion properties exceeds acceptable limits
422 Validation failed – request had correct syntax, but violated validation rules

post
/sale/loyalty/promotions
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json
Example

Large Order Discount
Large Order Discount

Copy
Expand allCollapse all
{
"benefits": [
{}
],
"offerCriteria": [
{}
]
}
Response samples
201400401403404412422
Content type
application/vnd.allegro.public.v1+json
Example

Large Order Discount
Large Order Discount

Copy
Expand allCollapse all
{
"status": "ACTIVE",
"createdAt": "2019-05-12T10:02:31.123Z",
"id": "72c40ffb-6127-4719-a473-867bf5775601",
"benefits": [
{}
],
"offerCriteria": [
{}
]
}
Get the user's list of promotions
Get a list of promotions defined by the authorized user and filtered by promotion type.

Restrictions:

Filtering by promotion type is required.

Sum of limit and offset must be equal to or lower than 50000. Limit must be equal to or lower than 5000.

Example:

offset = 49950 and limit = 50 will return promotions

offset = 49950 and limit = 51 will return 422 http error

offset = 0 and limit = 5000 will return promotions

offset = 0 and limit = 5001 will return 422 http error

Read more about: Large order discount PL / EN, Wholesale price list PL / EN, Multipack PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
limit	
integer <int32> [ 1 .. 5000 ]
Default: 50
Limit of promotions per page.

offset	
integer <int32> [ 0 .. 49999 ]
Default: 0
Distance between the beginning of the document and the point from which promotions are returned.

offer.id	
string
Example: offer.id=8226673525
Filter by offer id. No promotions with OFFERS_ASSIGNED_EXTERNALLY or ALL_OFFERS criteria will be returned if this parameter is present.

promotionType
required
string
Enum: "MULTIPACK" "CROSS_MULTIPACK" "LARGE_ORDER_DISCOUNT" "WHOLESALE_PRICE_LIST"
Filter by promotion type.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Successfully returned the requested list of promotions
400 Bad request
401 Unauthorized action
422 Restrictions were not satisfied

get
/sale/loyalty/promotions
Response samples
200401422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"promotions": [
{}
],
"totalCount": 0
}
Get a promotion data by id

Use this resource to return the requested promotion. You need to use its unique id.
Read more about: Large order discount PL / EN, Wholesale price list PL / EN, Multipack PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
promotionId
required
string
Promotion identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Successfully returned the requested promotion
401 Unauthorized action
404 Promotion not found

get
/sale/loyalty/promotions/{promotionId}
Response samples
200401404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"benefits": [
{}
],
"createdAt": "2019-05-01T10:12:32.321Z",
"id": "7c9a76d3-9fd0-4d13-a4ce-5d49bec12c79",
"offerCriteria": [
{}
],
"status": "ACTIVE"
}
Modify a promotion
Use this resource to update a promotion by its unique id.
It supports editing bundle's discount, wholesale price lists and large order discounts. Read more about: Large order discount PL / EN, Wholesale price list PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
promotionId
required
string
Promotion identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
benefits
required
Array of objects (Benefit)
What kind of rebate will be given

offerCriteria
required
Array of objects (SellerRebateOfferCriterion)
What offers will be included

Responses
200 Successfully updated the requested promotion
400 Bad request
401 Unauthorized action
403 Forbidden action
404 Promotion not found
422 Validation failed – request had correct syntax, but violated validation rules

put
/sale/loyalty/promotions/{promotionId}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json
Example

Large Order Discount
Large Order Discount

Copy
Expand allCollapse all
{
"benefits": [
{}
],
"offerCriteria": [
{}
]
}
Response samples
200400401403404422
Content type
application/vnd.allegro.public.v1+json
Example

Large Order Discount
Large Order Discount

Copy
Expand allCollapse all
{
"status": "ACTIVE",
"createdAt": "2019-05-12T10:02:31.123Z",
"id": "72c40ffb-6127-4719-a473-867bf5775601",
"benefits": [
{}
],
"offerCriteria": [
{}
]
}
Deactivate a promotion by id
Use this resource to deactivate the requested promotion. You need to use its unique id.
Read more about: Large order discount PL / EN, Wholesale price list PL / EN, Multipack PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
promotionId
required
string
Promotion identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
204 Successfully deactivated the requested promotion
401 Unauthorized action
404 Promotion not found

delete
/sale/loyalty/promotions/{promotionId}
Response samples
401
Content type
application/vnd.allegro.public.v1+json

Copy
{
"error": "unauthorized",
"error_description": "Full authentication is required to access this resource"
}
Create/modify turnover discount for marketplace Deprecated
You cannot create or modify a turnover-based discount. Turnover-based discounts are about to be withdrawn from the platform. Any existing discounts will be removed automatically. This resource is deprecated and will be removed on November 2, 2026.

Authorizations:
bearer-token-for-user
path Parameters
marketplaceId
required
string
Marketplace identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
request

thresholds	
Array of objects (TurnoverDiscountThresholdDto)
List of thresholds to apply to cumulated turnover.

Responses
200 Successfully created/modified turnover discount for marketplace
400 Bad request
401 Unauthorized action
403 Forbidden action
404 Marketplace not supported
422 Validation failed – request had correct syntax, but violated validation rules

put
/sale/turnover-discount/{marketplaceId}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"thresholds": [
{}
]
}
Response samples
200400401403404422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"marketplaceId": "allegro-business-cz",
"status": "ACTIVATING",
"definitions": [
{}
]
}
Get the list of turnover discounts Deprecated
Get a list of turnover discounts for all supported marketplaces. Read more: PL / EN. Currently, the only supported marketplace is allegro-business-cz. This resource is deprecated and will be removed on November 2, 2026.
Turnover discount for the marketplace can have one of the three statuses:

ACTIVATING - neither accumulation of the turnover, nor applying of the discount has started yet. Turnover will be being accumulated from the beginning of the next month.
ACTIVE - there is ongoing accumulation of the turnover and/or applying of the discount. The latest discount definition does not have fields cumulatingToDate and spendingToDate set to a specific date. There may be multiple (up to 3) definitions of the discount returned for each marketplace. Only one definition can be accumulated against, and only one definition can be applied at the same time - appropriate periods from different definitions will not overlap.
DEACTIVATING - there is ongoing accumulation of the turnover and/or applying of the discount. Accumulation of the turnover will be continued until cumulatingToDate of the last definition. Applying of the discount will be continued until spendingToDate of the last definition.
Authorizations:
bearer-token-for-user
query Parameters
marketplaceId	
Array of strings
List of marketplace identifiers. Only turnover discounts for specified marketplaces are returned.
Currently, only allegro-business-cz is supported.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 List of turnover discounts for marketplaces
401 Unauthorized action
403 Forbidden action

get
/sale/turnover-discount
Response samples
200401403
Content type
application/vnd.allegro.public.v1+json
Example

New discount
New discount

Copy
Expand allCollapse all
[
{
"marketplaceId": "allegro-business-cz",
"status": "ACTIVATING",
"definitions": []
}
]
Deactivate turnover discount for marketplace Deprecated
Deactivate turnover discount for a given marketplace. Read more: PL / EN. Currently, the only supported marketplace is allegro-business-cz. This resource is deprecated and will be removed on November 2, 2026.
Turnover discount will stop being cumulated with the end of the current month. Discount based on cumulated turnover will stop being applied with the end of the next month. After that, the discount will be completely deactivated.
When deactivating the discount that still has ACTIVATING status, turnover discount is deactivated immediately. In that case, no turnover discount will start being cumulated with the new month.

Authorizations:
bearer-token-for-user
path Parameters
marketplaceId
required
string
Marketplace identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Turnover discount for marketplace after deactivation
204 Discount with ACTIVATING status was deactivated
401 Unauthorized action
403 Forbidden action
404 Marketplace not supported

put
/sale/turnover-discount/{marketplaceId}/deactivate
Response samples
200401403404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"marketplaceId": "allegro-business-cz",
"status": "DEACTIVATING",
"definitions": [
{}
]
}
Offer bundles
List seller's bundles Deprecated
You can fetch page of seller's offer bundles using this endpoint.
Paging:
To move to next page, specify page.id parameter with value obtained in response from previous request. Number of offer bundles on single page can be specified using limit parameter.
Filtering:
Offer bundles can be filtered to bundles which contain offer specified in offer.id parameter. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
limit	
integer <int32> [ 1 .. 5000 ]
Default: 50
Example: limit=200
Limit of bundles per page.

offer.id	
string
Example: offer.id=123456789
Filter bundles which contains offer.

page.id	
string
Example: page.id=MjAyNC0wOS0xMFQwNjo0OTowMi40NTBa
ID of page which will be retrieved.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Page of seller's bundles.
400 Bad request
401 Unauthenticated action
403 Forbidden action
422 Validation failed – request had correct syntax, but violated validation rules

get
/sale/bundles
Response samples
200400401403422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"bundles": [
{}
],
"nextPage": {
"id": "MjAyNC0wOS0xMFQwNjo0OTowMi40NTBa"
}
}
Get bundle by ID Deprecated
Use this resource to retrieve offer bundle by its unique identifier. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
bundleId
required
string
Bundle ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Successfully returned the requested offer bundle
401 Unauthenticated action
404 Bundle not found

get
/sale/bundles/{bundleId}
Response samples
200401404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "a42d09c2-2669-4e7c-989b-7c341e84f787",
"offers": [
{},
{}
],
"publication": [
{}
],
"discounts": [
{}
],
"createdAt": "2023-09-21T10:22:02.999Z",
"createdBy": "USER"
}
Delete bundle by ID Deprecated
Use this resource to delete offer bundle by its unique identifier. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
bundleId
required
string
Bundle ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
204 Bundle successfully deleted.
401 Unauthenticated action
404 Bundle not found

delete
/sale/bundles/{bundleId}
Response samples
401404
Content type
application/vnd.allegro.public.v1+json

Copy
{
"error": "unauthorized",
"error_description": "Full authentication is required to access this resource"
}
Update discount associated with bundle Deprecated
Use this resource to update discount per marketplaces associated with bundle specified by its unique identifier. This will override currently set discounts for all marketplaces, so the unchanged discounts also must be specified in request. In case discount for marketplace is not specified in request it will be deleted. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
bundleId
required
string
Bundle ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
discounts	
Array of objects or null (BundleDiscountDTO)
Discounts on marketplaces. Can be null or empty if bundle shouldn't have discount on any marketplace.

Responses
200 Bundle discount successfully changed.
400 Bad request
401 Unauthenticated action
403 Forbidden action
422 Validation failed – request had correct syntax, but violated validation rules

put
/sale/bundles/{bundleId}/discount
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"discounts": [
{}
]
}
Response samples
200400401403422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "a42d09c2-2669-4e7c-989b-7c341e84f787",
"offers": [
{},
{}
],
"publication": [
{}
],
"discounts": [
{}
],
"createdAt": "2023-09-21T10:22:02.999Z",
"createdBy": "USER"
}
Flexible bundles
Create new flexible bundle
You can create flexible bundle using this resource.
Requirements:

there are max 6 slots in bundle;
order value for each slot must be unique (ranging from 0 to 5);
each slot can contain up to 30 offers;
all offers in slot must be from the same category leaf (based on assortment's tree);
at least one slot has to be marked as entrypoint;
offer can be used in bundle only once (cannot be used in multiple slots);
only offers active on at least one marketplace can be used;
B2B offers cannot be used;
age-restricted offers (eg. alcohol) cannot be used;
cannot use multiple offers which are representing same product;
all offers in bundle have to be 1F or not 1F.
Read more: PL / EN.
Authorizations:
bearer-token-for-user
Request Body schema: application/vnd.allegro.public.v1+json
slots
required
Array of objects (FlexibleBundleSlotDTO) [ 2 .. 6 ] items
discount	
object or null
Discount configuration for bundle

Responses
201 Successfully created the requested flexible bundle. While creating bundle, for each offer their availability to buy in a bundle is calculated on each marketplace. Offer can be unavailable to buy in bundle when it is not active on marketplace or it's stock is not sufficient. Reason why offer is not available is returned for each marketplace.
400 Bad request
401 Unauthenticated action
403 Forbidden action
422 Validation failed – request had correct syntax, but violated validation rules

post
/sale/flexible-bundles
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json
Example

Bundle without discount
Bundle without discount

Copy
Expand allCollapse all
{
"slots": [
{},
{}
],
"discount": null
}
Response samples
201400401403422
Content type
application/vnd.allegro.public.v1+json
Example

Bundle without discount
Bundle without discount

Copy
Expand allCollapse all
{
"id": "bac2128a-ec95-4d19-a241-d8be7001b8b8",
"createdAt": "2025-09-21T10:22:02.999Z",
"createdBy": "USER",
"slots": [
{},
{}
],
"discount": null
}
List seller's flexible bundles
You can fetch page of seller's flexible bundles using this endpoint.
Paging:
To move to next page, specify page.id parameter with value obtained in response from previous request. Number of offer bundles on single page can be specified using limit parameter.
Filtering:
Offer bundles can be filtered to bundles which contain offer specified in offer.id parameter. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
limit	
integer <int32> [ 1 .. 1000 ]
Default: 20
Example: limit=200
Limit of bundles per page.

offer.id	
string
Example: offer.id=123456789
Filter bundles which contains offer.

page.id	
string
Example: page.id=MjAyNC0wOS0xMFQwNjo0OTowMi40NTBa
ID of page which will be retrieved.

Responses
200 Page of seller's flexible bundles.
400 Bad request
401 Unauthenticated action
403 Forbidden action
422 Validation failed – request had correct syntax, but violated validation rules

get
/sale/flexible-bundles
Response samples
200400401403422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"bundles": [
{},
{},
{}
],
"nextPage": {
"id": "eyJsYXN0SWQiOiJidW5kbGUtNzg5In0="
}
}
Get flexible bundle by ID
Use this resource to retrieve flexible bundle by its unique identifier. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
bundleId
required
string <uuid>
Bundle ID.

Responses
200 Successfully returned the requested flexible bundle
401 Unauthenticated action
404 Bundle not found

get
/sale/flexible-bundles/{bundleId}
Response samples
200401404
Content type
application/vnd.allegro.public.v1+json
Example

Bundle without discount
Bundle without discount

Copy
Expand allCollapse all
{
"id": "bac2128a-ec95-4d19-a241-d8be7001b8b8",
"createdAt": "2025-09-21T10:22:02.999Z",
"createdBy": "ALLEGRO",
"slots": [
{},
{}
],
"discount": null
}
Updates flexible bundle
You can update flexible bundle using this resource.
Requirements:

there are max 6 slots in bundle;
order value for each slot must be unique (ranging from 0 to 5);
each slot can contain up to 30 offers;
all offers in slot must be from the same category leaf (based on assortment's tree);
at least one slot has to be marked as entrypoint;
offer can be used in bundle only once (cannot be used in multiple slots);
only offers active on at least one marketplace can be used;
B2B offers cannot be used;
age-restricted offers (eg. alcohol) cannot be used;
cannot use multiple offers which are representing same product;
all offers in bundle have to be 1F or not 1F.
Read more: PL / EN.
Authorizations:
bearer-token-for-user
path Parameters
bundleId
required
string <uuid>
Bundle ID.

Request Body schema: application/vnd.allegro.public.v1+json
slots
required
Array of objects (FlexibleBundleSlotDTO) [ 2 .. 6 ] items
discount	
object or null (FlexibleBundleDiscountDTO)
Discount configuration for bundle

Responses
200 Successfully updated the requested flexible bundle. While updating bundle, for each offer their availability to buy in a bundle is calculated on each marketplace. Offer can be unavailable to buy in bundle when it is not active on marketplace or it's stock is not sufficient. Reason why offer is not available is returned for each marketplace.
400 Bad request
401 Unauthenticated action
403 Forbidden action
422 Validation failed – request had correct syntax, but violated validation rules

put
/sale/flexible-bundles/{bundleId}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json
Example

Bundle without discount
Bundle without discount

Copy
Expand allCollapse all
{
"slots": [
{},
{}
],
"discount": null
}
Response samples
200400401403422
Content type
application/vnd.allegro.public.v1+json
Example

Bundle without discount
Bundle without discount

Copy
Expand allCollapse all
{
"id": "bac2128a-ec95-4d19-a241-d8be7001b8b8",
"createdAt": "2025-09-21T10:22:02.999Z",
"createdBy": "ALLEGRO",
"slots": [
{},
{}
],
"discount": null
}
Delete flexible bundle by ID
Use this resource to delete flexible bundle by its unique identifier. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
bundleId
required
string <uuid>
Bundle ID.

Responses
204 Bundle successfully deleted.
401 Unauthenticated action
404 Bundle not found

delete
/sale/flexible-bundles/{bundleId}
Response samples
401404
Content type
application/vnd.allegro.public.v1+json

Copy
{
"error": "unauthorized",
"error_description": "Full authentication is required to access this resource"
}
Badge campaigns
Get a list of available badge campaigns
Badge campaigns are another way to promote your offers. You can apply for a badge, which - depending on a type - will be displayed on your offer page of on the list of offers. First - use this resource to get a list of all available badge campaigns at the moment, then use POST /sale/badges to apply for badge. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
marketplace.id	
string
Example: marketplace.id=allegro-pl
The marketplace of campaigns.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 List of available badge campaigns.
400 Invalid values supplied in the query parameters.
401 Unauthorized.
403 The account is not a Business Account.

get
/sale/badge-campaigns
Response samples
200400401403
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"badgeCampaigns": [
{},
{}
]
}
Apply for badge in selected offer
This resource allows you to apply for a badge. Most badges involve additional fee charged. Your badge application will be verified and you will be notified about the verification status via e-mail. You can use Location provided in header of the response to track your application status. Application will be removed after 30 days when status of the application was changed form PROCESSED or DECLINED. Fees will be charged in accordance with Annex No. 1 to the Daily deals zone terms and conditions.

By using this resource you agree to the Daily deals zone terms and conditions or Commission discount terms and conditions. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
campaign
required
object (BadgeApplicationCampaign)
offer
required
object (BadgeOffer)
prices	
object or null (BadgeApplicationPrices)
Required by DISCOUNT and SOURCING campaign.

purchaseConstraints	
object (BadgeApplicationPurchaseConstraints)
Constraints of purchase of this offer while it participates in the campaign. Optional for all campaigns types.

declaredStock	
object or null (BadgeApplicationDeclaredStock)
Stock declared to be reserved for the campaign. Required only for campaigns with stockReservationIsRequired property equal true.

Responses
202 Successfully applied for a badge.
400 Syntactically incorrect request.
401 Unauthorized
403 The account is not a Business Account.
422 Validation error. Invalid parameters provided in the request.

post
/sale/badges
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json
Example

Discount
Discount

Copy
Expand allCollapse all
{
"campaign": {
"id": "BARGAIN"
},
"offer": {
"id": "12345678"
},
"prices": {
"bargain": {}
}
}
Response samples
202400401403422
Content type
application/vnd.allegro.public.v1+json
Example

Discount badge application
Discount badge application

Copy
Expand allCollapse all
{
"id": "01234567-89ab-0123-456789ab",
"createdAt": "2011-12-03T10:15:30Z",
"updatedAt": "2011-12-03T10:15:30Z",
"campaign": {
"id": "BARGAIN"
},
"offer": {
"id": "987654321"
},
"prices": {
"bargain": {}
},
"process": {
"status": "REQUESTED",
"rejectionReasons": [ ]
}
}
Get a list of badges
Use this resource to get a list of badges in authorized seller's offers. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
offer.id	
string
Offer ID.

marketplace.id
required
string
Example: marketplace.id=allegro-pl
The marketplace of badges.

offset	
integer >= 0
Offset.

limit	
integer [ 1 .. 1000 ]
Default: 50
The maximum number of badges returned in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Successfully returned list of badges.
400 Invalid values supplied in the query parameters.
401 Unauthorized.
403 The account is not a Business Account.

get
/sale/badges
Response samples
200400401403
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"badges": [
{},
{},
{},
{}
]
}
Get a badge application details
Use this resource to get a badge application details. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
applicationId
required
string
Badge application ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Successfully returned badge application.
401 Unauthorized.
403 The account is not a Business Account.
404 Badge application not found.

get
/sale/badge-applications/{applicationId}
Response samples
200401403404
Content type
application/vnd.allegro.public.v1+json
Example

Processed
Processed

Copy
Expand allCollapse all
{
"id": "81ff5e67-d00b-4141-a79a-68636755df95",
"createdAt": "2019-05-16T12:49:17.347Z",
"updatedAt": "2019-05-16T12:49:17.530Z",
"campaign": {
"id": "BARGAIN"
},
"offer": {
"id": "12345678"
},
"prices": {
"bargain": {}
},
"campaignStock": null,
"process": {
"status": "PROCESSED",
"rejectionReasons": [ ]
}
}
Get a list of badge applications
Use this resource to get a list of badge applications. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
campaign.id	
string
Campaign ID.

offer.id	
string
Offer ID.

offset	
integer >= 0
Offset.

limit	
integer [ 1 .. 1000 ]
Default: 50
The maximum number of applications returned in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Successfully returned badge applications list.
400 Invalid values supplied in the query parameters.
401 Unauthorized.
403 The account is not a Business Account.

get
/sale/badge-applications
Response samples
200400401403
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"badgeApplications": [
{},
{},
{},
{}
]
}
Get badge operation details
Use this resource to get badge operation details. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
operationId
required
string
Badge operation ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Successfully returned badge operation details.
401 Unauthorized.
403 You don't have permission to access this resource.
404 Badge operation not found.

get
/sale/badge-operations/{operationId}
Response samples
200401403404
Content type
application/vnd.allegro.public.v1+json
Example

Processed
Processed

Copy
Expand allCollapse all
{
"id": "81ff5e67-d00b-4141-a79a-68636755df95",
"type": "FINISH",
"createdAt": "2019-05-16T12:49:17.347Z",
"updatedAt": "2019-05-16T12:49:17.530Z",
"campaign": {
"id": "BARGAIN"
},
"offer": {
"id": "12345678"
},
"process": {
"status": "PROCESSED",
"rejectionReasons": [ ]
}
}
Update campaign badge for the given offer
This resource allows you to update a campaign badge for the given offer. You can use Location provided in header of the response to track your update status. Update offer price in a campaign or finish marking an offer in a campaign. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
offerId
required
string
Offer ID.

campaignId
required
string
Campaign ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Any of BadgePatchProcessBadgePatchPrices
process	
object
Responses
202 Successfully requested badge update.
400 Syntactically incorrect request.
401 Unauthorized.
403 You don't have permission to access this resource.
404 Resource not found.
409 Asynchronous badge operation for this offer already exists in status REQUESTED.
422 Validation error. Invalid parameters provided in the request.

patch
/sale/badges/offers/{offerId}/campaigns/{campaignId}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json
Example

Price update for the given offer in the given campaign
Price update for the given offer in the given campaign

Copy
Expand allCollapse all
{
"prices": {
"bargain": {}
}
}
Response samples
202400401403404409422
Content type
application/vnd.allegro.public.v1+json

Copy
{
"id": "154179f0-ed4c-4b84-9260-302d2dec3801"
}
Allegro Prices
Get account participation status
Use this resource to retrieve the account participation status for all supported marketplaces in the Allegro Prices program. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Successfully retrieved account participation status
401 Unauthorized

get
/sale/allegro-prices/accounts/participations
Response samples
200401
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"marketplaces": [
{}
]
}
Update account participation
Use this resource to update the account participation status for one or more marketplaces in the Allegro Prices program. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
marketplaces
required
Array of objects (AccountParticipationMarketplaceRequest) non-empty
List of marketplaces to update (must not be empty)

Responses
200 Successfully updated account participation
400 Bad request - invalid JSON format or missing required fields (e.g., null values for non-nullable fields)
401 Unauthorized - invalid or missing authentication token
422 Unprocessable Entity - validation error (e.g., empty marketplace list, invalid status, unsupported marketplace)

patch
/sale/allegro-prices/accounts/participations
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"marketplaces": [
{}
]
}
Response samples
200400401422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"marketplaces": [
{}
]
}
Submit offers command
Use this resource to submit a command to add offers to the Allegro Prices program. Returns a command ID that can be used to track the processing status. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
commandId	
string <uuid>
Optional custom command identifier. If not provided, a UUID will be generated automatically

offers
required
Array of objects (SubsidyOfferToSubmit) [ 1 .. 1000 ] items
List of offers to submit (1-1000 offers, must not contain duplicates)

Responses
201 Command successfully created and is being processed
400 Bad Request - invalid JSON format or missing required fields (e.g., invalid command ID format, null values for offers, offer id, marketplace id, or maxContributionPercentage)
401 Unauthorized - invalid or missing authentication token
409 Conflict - command with the same ID already exists
422 Unprocessable Entity - validation error (e.g., empty offers list, invalid discount declaration, duplicate offers, unsupported marketplace)

post
/sale/allegro-prices/offers/submit-offer-commands
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"commandId": "123e4567-e89b-12d3-a456-426614174000",
"offers": [
{}
]
}
Response samples
201400401409422
Content type
application/vnd.allegro.public.v1+json

Copy
{
"commandId": "123e4567-e89b-12d3-a456-426614174000",
"status": "IN_PROGRESS",
"createdAt": "2023-12-11T12:00:00.000Z"
}
Get submit offer command status
Use this resource to retrieve the status and details of a previously submitted offer command. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string <uuid>
The unique identifier of the command.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Command found and details retrieved successfully
400 Bad Request - invalid UUID format for command ID
401 Unauthorized - invalid or missing authentication token
404 Not Found - command does not exist or belongs to a different seller

get
/sale/allegro-prices/offers/submit-offer-commands/{commandId}
Response samples
200400401404
Content type
application/vnd.allegro.public.v1+json
Example

All offers successfully submitted
All offers successfully submitted

Copy
Expand allCollapse all
{
"commandId": "123e4567-e89b-12d3-a456-426614174000",
"createdAt": "2024-01-29T10:30:00.000Z",
"offers": [
{},
{}
]
}
Exclude offers command
Use this resource to submit a command to exclude offers from the Allegro Prices program. Returns a command ID that can be used to track the processing status. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
commandId	
string <uuid>
Optional custom command identifier. If not provided, a UUID will be generated automatically

offers
required
Array of objects (SubsidyOfferToExclude) [ 1 .. 1000 ] items
List of offers to exclude (1-1000 offers, must not contain duplicates)

Responses
201 Command successfully created and is being processed
400 Bad Request - invalid JSON format or missing required fields (e.g., invalid command ID format, null values for offers, offer id, or marketplace id)
401 Unauthorized - invalid or missing authentication token
409 Conflict - command with the same ID already exists
422 Unprocessable Entity - validation error (e.g., empty offers list, duplicate offers, unsupported marketplace)

post
/sale/allegro-prices/offers/exclusion-commands
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"commandId": "123e4567-e89b-12d3-a456-426614174000",
"offers": [
{}
]
}
Response samples
201400401409422
Content type
application/vnd.allegro.public.v1+json

Copy
{
"commandId": "123e4567-e89b-12d3-a456-426614174000",
"status": "IN_PROGRESS",
"createdAt": "2023-12-11T12:00:00.000Z"
}
Get exclude offer command status
Use this resource to retrieve the status and details of a previously submitted exclusion command. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string <uuid>
The unique identifier of the command.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Command found and details retrieved successfully
400 Bad Request - invalid UUID format for command ID
401 Unauthorized - invalid or missing authentication token
404 Not Found - command does not exist or belongs to a different seller

get
/sale/allegro-prices/offers/exclusion-commands/{commandId}
Response samples
200400401404
Content type
application/vnd.allegro.public.v1+json
Example

All offers successfully excluded
All offers successfully excluded

Copy
Expand allCollapse all
{
"commandId": "567e8901-e89b-12d3-a456-426614174004",
"createdAt": "2024-01-29T11:00:00.000Z",
"offers": [
{},
{},
{}
]
}
Query Allegro Prices offers status
Use this resource to retrieve a list of offers and their status in the Allegro Prices program with optional filtering and pagination. Allows filtering by offer IDs, marketplace, and scope (WITH_DECLARATION, DISCOUNTED, or EXCLUDED). Only offers in ACTIVATING, ACTIVE, or ENDED statuses are considered. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
offer	
object
Filter options for offers

marketplace
required
object
Marketplace identifier filter

limit	
integer <int32> [ 1 .. 1000 ]
Default: 20
Maximum number of offers to return in a single response. Must be between 1 and 1000.

offset	
integer <int32> >= 0
Default: 0
Number of offers to skip before starting to return results. Used for pagination. Must be at least 0.

Responses
200 Successfully retrieved offers
400 Bad request - Invalid request body or missing required fields
401 Unauthorized - Missing or invalid authentication credentials
422 Unprocessable entity - Validation error (e.g., invalid marketplace ID, limit out of range, invalid scope)

post
/sale/allegro-prices/offers-queries
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json
Example

Filter offers by scope (WITH_DECLARATION)
Filter offers by scope (WITH_DECLARATION)

Copy
Expand allCollapse all
{
"marketplace": {
"id": "allegro-pl"
},
"offer": {
"scope": "WITH_DECLARATION"
},
"limit": 50,
"offset": 0
}
Response samples
200400401422
Content type
application/vnd.allegro.public.v1+json
Example

Response with discounted offers
Response with discounted offers

Copy
Expand allCollapse all
{
"offers": [
{},
{}
],
"totalCount": 150,
"count": 2
}
AlleDiscount
Create submit offer command
Use this resource to create a command for submitting an offer. Offer will be submitted to the AlleDiscount campaign only if command is processed successfully. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "en-US"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
commandId	
string or null
The command UUID. If empty, system generates new one.

input	
object
Command input.

Responses
201 Command has been created.
400 Bad request. Example error codes:
CommandIdNotValidUuid
ProposedPriceAmountInvalidNumberFormat
ProposedPriceAmountNotPositive
ProposedPriceAmountInvalidDecimalPlaces
ProposedPriceAmountCannotBeNull
401 Unauthorized.
409 Provided UUID is already being used.

post
/sale/alle-discount/submit-offer-commands
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"commandId": "c1b3f63d-d293-4333-911d-a0c1053e2c81",
"input": {
"offer": {},
"campaign": {},
"proposedPrice": {}
}
}
Response samples
201400
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "c1b3f63d-d293-4333-911d-a0c1053e2c81",
"input": {
"offer": {},
"campaign": {},
"proposedPrice": {}
},
"output": {
"status": "NEW",
"createdAt": "2023-02-09T10:15:30.000Z",
"updatedAt": "2023-02-09T10:15:30.000Z"
}
}
Get the offer submission command status
Use this resource to get information about the submit offer command execution status. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command id in UUID format, must be unique.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "en-US"
Example: en-US
Expected language of messages.

Responses
200 Returns command output with status and possible errors.
401 Unauthorized.
404 Not Found. Check provided command id.

get
/sale/alle-discount/submit-offer-commands/{commandId}
Response samples
200
Content type
application/vnd.allegro.public.v1+json
Example

Submit command executed with status: SUCCESSFUL
Submit command executed with status: SUCCESSFUL

Copy
Expand allCollapse all
{
"id": "c1b3f63d-d293-4333-911d-a0c1053e2c81",
"input": {
"offer": {},
"campaign": {},
"proposedPrice": {}
},
"output": {
"status": "SUCCESSFUL",
"createdAt": "2023-02-09T10:15:30.000Z",
"updatedAt": "2023-02-09T12:15:30.000Z",
"newOfferParticipation": {},
"errors": [ ]
}
}
Create withdraw offer command
Use this resource to create a command for withdrawing an offer from specific campaign. Offer will be withdrawn from the AlleDiscount campaign only if command is processed successfully. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "en-US"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
commandId	
string or null
The Command UUID. If empty, system generates new one.

input	
object
Command input.

Responses
201 Command has been created.
400 Bad request. Example error codes:
CommandIdNotValidUuid
ParticipationIdMustBeUuid
InputParticipationIdFieldMissing
InputParticipationIdDoesNotExist
401 Unauthorized.
409 Provided UUID is already being used.

post
/sale/alle-discount/withdraw-offer-commands
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"commandId": "c1b3f63d-d293-4333-911d-a0c1053e2c81",
"input": {
"participationId": "f9a4a70c-6db9-4473-976c-90f8df9f74e8"
}
}
Response samples
201400
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "c1b3f63d-d293-4333-911d-a0c1053e2c81",
"input": {
"participationId": "f9a4a70c-6db9-4473-976c-90f8df9f74e8"
},
"output": {
"status": "NEW",
"createdAt": "2023-02-09T10:15:30.000Z",
"updatedAt": "2023-02-09T12:15:30.000Z"
}
}
Get the offer withdrawal command status
Use this resource to get information about the withdrawal command execution status. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Command id in UUID format, must be unique.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "en-US"
Example: en-US
Expected language of messages.

Responses
200 Returns command output with status and possible errors.
401 Unauthorized.
404 Not Found. Check provided command id.

get
/sale/alle-discount/withdraw-offer-commands/{commandId}
Response samples
200
Content type
application/vnd.allegro.public.v1+json
Example

Withdraw command with status: SUCCESSFUL
Withdraw command with status: SUCCESSFUL

Copy
Expand allCollapse all
{
"id": "c1b3f63d-d293-4333-911d-a0c1053e2c81",
"input": {
"participationId": "f9a4a70c-6db9-4473-976c-90f8df9f74e8"
},
"output": {
"status": "SUCCESSFUL",
"createdAt": "2024-02-09T10:15:30.000Z",
"updatedAt": "2024-02-09T12:15:30.000Z",
"withdrawnOfferParticipation": {},
"errors": [ ]
}
}
List eligible offers
Endpoint returning info about offers that can be submitted to a given AlleDiscount campaign. Only offer linked to the product in published list of goods (products) can be submitted to a given AlleDiscount campaign. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
campaignId
required
string
Campaign id to list offers from.

query Parameters
limit	
integer
Maximum number of offers returned in the eligibleOffers list; max value is 200.

offset	
integer
The number of offers to skip while listing the results.

meetsConditions	
boolean
If true, filters offers that only meet conditions of the campaign.

offerId	
string
ID of an offer; if the offer with the given ID exists, returns at most one element in the eligibleOffers list.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "en-US"
Example: en-US
Expected language of messages.

Responses
200 Lists offers eligible for submission.
400 Bad Request. Example error codes:
OffsetNegative
LimitBelowMin
LimitAboveMax
OfferIdInvalidFormat
401 Unauthorized.
403 Forbidden. Access to the AlleDiscount campaign may have been restricted, check user message.
404 Not Found. Check provided AlleDiscount campaign id.

get
/sale/alle-discount/{campaignId}/eligible-offers
Response samples
200400
Content type
application/vnd.allegro.public.v1+json
Example

Offers that meet conditions.
Offers that meet conditions.

Copy
Expand allCollapse all
{
"eligibleOffers": [
{}
],
"count": 1,
"totalCount": 1
}
List offer participations
Endpoint returning info about offer participations for a given AlleDiscount campaign. With this endpoint you are able to validate if the offer participates in AlleDiscount and if it has lowered price on the platform. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
campaignId
required
string
Campaign id to list offers from.

query Parameters
limit	
integer
Maximum number of offers returned in the eligibleOffers list; max value is 200.

offset	
integer
The number of offers to skip while listing the results.

offerId	
string
ID of an offer; if the offer with the given ID exists, returns at most one element in the submittedOffers list.

participationId	
string
Id of the participation, returns at most one element in the submittedOffers list.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "en-US"
Example: en-US
Expected language of messages.

Responses
200 Lists offer participations.
400 Bad Request.
401 Unauthorized.
403 Forbidden. Access to the AlleDiscount campaign may have been restricted, check user message.
404 Not Found. Check provided AlleDiscount campaign id.

get
/sale/alle-discount/{campaignId}/submitted-offers
Response samples
200400
Content type
application/vnd.allegro.public.v1+json
Example

Offer participation with status "ACCEPTED".
Offer participation with status "ACCEPTED".

Copy
Expand allCollapse all
{
"submittedOffers": [
{}
],
"count": 1,
"totalCount": 1
}
List AlleDiscount campaigns
List current AlleDiscount campaigns. Each campaign has its own list of goods (products) that indicate which offers can be submitted to it. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
campaignId	
string
Id of the searched campaign. If present, returns at most one entry.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "en-US"
Example: en-US
Expected language of messages.

Responses
200 Lists current AlleDiscount campaigns.
400 Bad Request.
401 Unauthorized.
404 Not Found.

get
/sale/alle-discount/campaigns
Response samples
200400404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"alleDiscountCampaigns": [
{}
]
}
Offer rating
Get offer rating
Use this resource to get offer rating. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
offerId
required
string
Example: 9991337999
Offer identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 OK.
401 Unauthorized action.
403 Offer access denied.
404 Offer not found.

get
/sale/offers/{offerId}/rating
Response samples
200401
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"averageScore": "4.0",
"scoreDistribution": [
{},
{},
{},
{},
{}
],
"totalResponses": 5,
"sizeFeedback": [
{},
{},
{}
]
}
Classifieds
Get the seller's advertisements daily statistics
This endpoint returns daily statistics collected for a list of advertisements in a given date range for logged user. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
date.gte	
string <date-time>
Example: date.gte=2020-11-13T12:45:20.818Z
The maximum date and time from which the events will be fetched in ISO 8601 format. The value should be less than the current date time. The difference between date.gte and date.lte should be less than 3 months.

date.lte	
string <date-time>
Example: date.lte=2020-11-13T12:45:20.818Z
The minimum date and time from which the events will be fetched in ISO 8601 format. The value should be less than the current date time and greater than date.lte. The difference between date.gte and date.lte should be less than 3 months.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "pl-PL"
Example: pl-PL
Expected language of messages.

Responses
200 Returns offer's statistics list
400 Syntactically incorrect request
401 Unauthorized
403 Forbidden
404 Not Found
422 Unprocessable Entity

get
/sale/classified-seller-stats
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"eventStatsTotal": [
{}
],
"eventsPerDay": [
{}
]
}
Get the advertisements daily statistics
This endpoint returns daily statistics collected for a list of advertisements in a given date range. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
offer.id
required
Array of strings
Example: offer.id=12394529345
List of offer Ids, maximum 50 values.

date.gte	
string <date-time>
Example: date.gte=2020-11-13T12:45:20.818Z
The maximum date and time from which the events will be fetched in ISO 8601 format. The value should be less than the current date time. The difference between date.gte and date.lte should be less than 3 months.

date.lte	
string <date-time>
Example: date.lte=2020-11-13T12:45:20.818Z
The minimum date and time from which the events will be fetched in ISO 8601 format. The value should be less than the current date time and greater than date.lte. The difference between date.gte and date.lte should be less than 3 months.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "pl-PL"
Example: pl-PL
Expected language of messages.

Responses
200 Returns offer's statistics list
400 Syntactically incorrect request
401 Unauthorized
403 Forbidden
404 Not Found
422 Unprocessable Entity

get
/sale/classified-offers-stats
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"offerStats": [
{}
]
}
Get classified packages assigned to an offer
Use this resource to retrieve classified packages currently assigned to an offer. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
offerId
required
string
Offer ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "pl-PL"
Example: pl-PL
Expected language of messages.

Responses
200 Packages returned successfully
400 Bad request
401 Unauthorized
403 Forbidden
404 Classified not found

get
/sale/offer-classifieds-packages/{offerId}
Response samples
200400401403404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"basePackage": {
"id": "e76d443b-c088-4da5-95f7-cc9aaf73bf7b"
},
"extraPackages": [
{}
]
}
Assign packages to a classified
Use this resource to assign classified packages to an offer. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
offerId
required
string
The offer ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "pl-PL"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Packages that should be assigned to the classified.

basePackage
required
object (ClassifiedPackage)
extraPackages	
Array of objects (ClassifiedExtraPackage)
Responses
200 Packages have been successfully assigned to the classified.
400 Bad request
401 Unauthorized
403 Forbidden
404 Classified not found
422 Validation error

put
/sale/offer-classifieds-packages/{offerId}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"basePackage": {
"id": "e76d443b-c088-4da5-95f7-cc9aaf73bf7b"
},
"extraPackages": [
{}
]
}
Response samples
400401403404422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"errors": [
{}
]
}
Get configurations of packages
Use this resource to retrieve configurations of classifieds packages for a category. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
category.id
required
string
Example: category.id=23456
The category ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "pl-PL"
Example: pl-PL
Expected language of messages.

Responses
200 Package configurations for the category returned successfully.
400 Bad request
401 Unauthorized

get
/sale/classifieds-packages
Response samples
200400401
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"packages": [
{}
]
}
Get the configuration of a package
Use this resource to retrieve the configuration of a classifieds package. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
packageId
required
string
The classifieds package ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "pl-PL"
Example: pl-PL
Expected language of messages.

Responses
200 The package's configuration returned successfully.
400 Bad request
401 Unauthorized
404 The classifieds package not found.

get
/sale/classifieds-packages/{packageId}
Response samples
200400401404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"extensions": [
{}
],
"id": "6174be19-56f9-484b-b72c-43b0b00785e8",
"name": "Power",
"promotions": [
{}
],
"publication": {
"duration": "PT240H"
},
"type": "BASE"
}
Pricing
Calculate fee and commission for an offer
Provides information about fee and commission for an offer. This resource is limited to 25 requests per second for a single user. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
offer	
object (PricingOffer)
Single offer data.

classifiedsPackages	
object (ClassifiedsPackages)
marketplaceId	
string or null
The marketplace on which the offer should be previewed. If omitted, it will default to the base marketplace.

Responses
200 Fee calculated successfully.
400 Bad request
401 Unauthorized
422 Unprocessable Entity

post
/pricing/offer-fee-preview
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"offer": {
"fundraisingCampaign": {},
"id": "string",
"category": {},
"parameters": [],
"promotion": {},
"publication": {},
"sellingMode": {}
},
"classifiedsPackages": {
"basePackage": {},
"extraPackages": []
},
"marketplaceId": "allegro-pl"
}
Response samples
200400401422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"commissions": [
{}
],
"quotes": [
{}
]
}
Get the user's current offer quotes
This endpoint returns current offer quotes (listing and promo fees) cycles for authenticated user and list of offers. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
offer.id
required
Array of strings
List of offer Ids, maximum 20 values.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Returns current offer quotes
400 Invalid request.
401 Full authentication is required to access this resource
403 Forbidden
503 Service is currently unavailable. Please try again later.

get
/pricing/offer-quotes
Response samples
200400503
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"count": 10,
"quotes": [
{}
]
}
Deposits
Get deposit types
Use this resource to get deposit types available when creating an offer. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Returns deposit types available to use when creating an offer.
401 Unauthorized
403 Forbidden
404 Not Found

get
/deposit/types
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"deposits": [
{}
]
}
Ingredients
Parse product ingredients
Use this resource to parse raw, free-text ingredients declarations into structured ingredient lists for one or more products. Every submitted product text is parsed independently. The response contains parsed items together with errors and warnings detected for each product.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
products
required
Array of objects (ProductIngredientsRequest) non-empty
List of products for which raw ingredients text should be parsed. Must not be empty.

Responses
200 Returns parsing results (items, errors and warnings) for every requested product.
400 Bad Request
401 Unauthorized
403 Forbidden

post
/ingredients/parse
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"products": [
{}
]
}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"products": [
{}
]
}
Order management
Get order events
Use this resource to return events that allow you to monitor actions which clients perform, i.e. making a purchase, filling in the checkout form (FOD), finishing payment process, making a surcharge. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
from	
string
You can use the event ID to retrieve subsequent chunks of events.

type	
Array of strings
Specify array of event types for filtering. Allowed values are:

BOUGHT: purchase without checkout form filled in
FILLED_IN: checkout form filled in but payment is not completed yet so data could still change
READY_FOR_PROCESSING: payment completed. Purchase is ready for processing
BUYER_CANCELLED: purchase was cancelled by buyer
FULFILLMENT_STATUS_CHANGED: fulfillment status changed
AUTO_CANCELLED: purchase was cancelled automatically by Allegro.
limit	
integer <int32> [ 1 .. 1000 ]
Default: 100
The maximum number of events returned in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Unauthorized
403 Forbidden
422 Unprocessable Entity - Returned when query parameters are incorrect.

get
/order/events
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"events": [
{}
]
}
Get order events statistics
Use this resource to returns object that contains event id and occurrence date of the latest event. It gives you current starting point for reading events. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Unauthorized

get
/order/event-stats
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"latestEvent": {
"id": "1532603898317497",
"occurredAt": "2018-10-12T10:12:32.321Z"
}
}
Get the user's orders
Use this resource to get an order list. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
offset	
integer >= 0
Default: 0
Index of first returned checkout-form from all search results.

limit	
integer [ 1 .. 100 ]
Default: 100
Maximum number of checkout-forms in response.

status	
string
Specify status value that checkout-forms must have to be included in the output. Allowed values are:

BOUGHT: purchase without checkout form filled in.
FILLED_IN: checkout form filled in but payment is not completed yet so data could still change.
READY_FOR_PROCESSING: payment completed. Purchase is ready for processing.
CANCELLED: purchase cancelled by buyer.
fulfillment.status	
string
Specify seller status value that checkout-forms must have to be included in the output. Allowed values are:

NEW
PROCESSING
READY_FOR_SHIPMENT
READY_FOR_PICKUP
SENT
PICKED_UP
CANCELLED
SUSPENDED
RETURNED.
fulfillment.provider.id	
string
Specify filter for order management provider. Allowed values are:

SELLER: for orders managed directly by seller
ALLEGRO: for orders managed by Allegro warehouse (One Fulfillment).
fulfillment.shipmentSummary.lineItemsSent	
string
Specify filter for line items sending status. Allowed values are:

NONE: none of line items have tracking number specified
SOME: some of line items have tracking number specified
ALL: all of line items have tracking number specified.
lineItems.boughtAt.lte	
string <date-time>
Latest line item bought date. The upper bound of date time range from which checkout forms will be taken.

lineItems.boughtAt.gte	
string <date-time>
Latest line item bought date. The lower bound of date time range from which checkout forms will be taken.

payment.id	
string
Find checkout-forms having specified payment id.

surcharges.id	
string
Find checkout-forms having specified surcharge id.

delivery.method.id	
string
Find checkout-forms having specified delivery method id.

buyer.login	
string
Find checkout-forms having specified buyer login.

marketplace.id	
string
Find checkout-forms of orders purchased on specified marketplace.

updatedAt.lte	
string <date-time>
Checkout form last modification date. The upper bound of date time range from which checkout forms will be taken.

updatedAt.gte	
string <date-time>
Checkout form last modification date. The lower bound of date time range from which checkout forms will be taken.

sort	
string
Enum: "lineItems.boughtAt" "-lineItems.boughtAt" "updatedAt" "-updatedAt"
The results' sorting order. No prefix in the value means ascending order. - prefix means descending order. If you don't provide the sort parameter, the list is sorted by line item boughtAt date, descending.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
400 Bad Request - Returned when request parameters contains illegal values.
401 Unauthorized
406 Not Acceptable
422 Unprocessable Entity - Returned when limit or offset value is outside an acceptable range

get
/order/checkout-forms
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"checkoutForms": [
{}
],
"count": 1,
"totalCount": 1
}
Get an order's details
Use this resource to get an order details. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string <uuid>
Example: 29738e61-7f6a-11e8-ac45-09db60ede9d6
Checkout form identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
400 Bad Request
401 Unauthorized
404 Not Found
406 Not Acceptable
422 Unprocessable Entity - Returned when order id is malformed UUID.

get
/order/checkout-forms/{id}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "29738e61-7f6a-11e8-ac45-09db60ede9d6",
"messageToSeller": "Please send me an item in red color",
"buyer": {
"id": "23123123",
"email": "user-email@allegro.pl",
"login": "User_Login",
"firstName": "Jan",
"lastName": "Kowalski",
"companyName": "Kowalex",
"guest": false,
"personalIdentity": "67062589524",
"phoneNumber": "+48123123123",
"preferences": {},
"address": {}
},
"payment": {
"id": "0f8f1d13-7e9e-11e8-9b00-c5b0dfb78ea6",
"type": "ONLINE",
"provider": "PAYU",
"finishedAt": "2018-10-12T10:12:32.321Z",
"paidAmount": {},
"reconciliation": {},
"features": []
},
"status": "READY_FOR_PROCESSING",
"fulfillment": {
"status": "SENT",
"shipmentSummary": {},
"provider": {}
},
"delivery": {
"address": {},
"method": {},
"pickupPoint": {},
"cost": {},
"time": {},
"smart": true,
"cancellation": {},
"calculatedNumberOfPackages": 1
},
"invoice": {
"required": true,
"address": {},
"dueDate": "2021-12-01",
"features": []
},
"lineItems": [
{}
],
"surcharges": [
{}
],
"codBookedPayments": [
{}
],
"note": {
"text": "Sample note"
},
"marketplace": {
"id": "allegro-pl"
},
"summary": {
"totalToPay": {}
},
"updatedAt": "2011-12-03T10:15:30.133Z",
"revision": "819b5836"
}
Get a list of available shipping carriers
Shipping carriers are essential to provide accurate tracking experience for customers. Use this resource to get a list of all available shipping carriers. This resource is rate limited to 50 requests per second.

The response of this resource can be stored in accordance with returned caching headers. Read more: PL / EN.

Authorizations:
bearer-token-for-applicationbearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 List of available shipping carriers.
401 Unauthorized
404 Not Found

get
/order/carriers
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"carriers": [
{},
{},
{},
{}
]
}
Get a list of parcel tracking numbers
Get a list of parcel tracking numbers currently assigned to the order. Orders can be retrieved using REST API resource GET /order/checkout-forms. Please note that the shipment list may contain parcel tracking numbers added through other channels such as Moje Allegro or by the carrier that delivers the parcel. Read more: PL / EN. This resource is rate limited to 50 requests per second.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string
Order identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Returns a list of parcel tracking numbers (shipments)
401 Authentication failed, e.g. token is expired
404 Order not found or doesn’t belong to the seller

get
/order/checkout-forms/{id}/shipments
Response samples
200401404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"shipments": [
{}
]
}
Add a parcel tracking number
Add a parcel tracking number (shipment) to given order line items. Read more: PL / EN. This resource is rate limited to 50 requests per second.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string
Order identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
request

carrierId
required
string
Supported carriers are available via shipping carriers resource.

waybill
required
string <= 64 characters
Waybill number (parcel tracking number). Cannot be empty and must be no longer than 64 characters.

carrierName	
string <= 30 characters
Carrier name to be provided only if carrierId is OTHER, otherwise it’s ignored. Must be no longer than 30 characters.

lineItems	
Array of objects
List of order line items. They must be from the order specified in the path parameter. When list is not provided or it is empty it means that every item from an order is included in shipment.

Responses
201 The request is OK and the parcel tracking number will be assigned to the order
400 Missing required field or invalid value in the request (e.g. unknown carrier id, carrier name too long, invalid tracking number structure)
401 Authentication failed, e.g. token is expired
404 Order not found or doesn’t belong to the seller
409 Maximum waybill usage exceeded (e.g. used in too many orders)
422 Some of the provided data is invalid, e.g. line item doesn’t belong to the order

post
/order/checkout-forms/{id}/shipments
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"carrierId": "ALLEGRO",
"waybill": "AD-1239134",
"carrierName": "Sample carrier",
"lineItems": [
{}
]
}
Response samples
201400401404409422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "REhMOjEyMzQ1Njc4OTEwUEw=",
"waybill": "AD-1239134",
"carrierId": "ALLEGRO",
"carrierName": "Sample carrier",
"lineItems": [
{}
],
"createdAt": "2019-02-18T11:46:48.264Z"
}
Set seller order status
Use to set seller order status. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string
Order identifier.

query Parameters
checkoutForm.revision	
string
Example: checkoutForm.revision=819b5836
Checkout form revision.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "en-US"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
request

status	
any (CheckoutFormFulfillmentStatus)
Enum: "NEW" "PROCESSING" "READY_FOR_SHIPMENT" "READY_FOR_PICKUP" "SENT" "PICKED_UP" "CANCELLED" "SUSPENDED" "RETURNED"
Order seller status. The status is managed by the seller, however in some cases the seller can enable automatic change of the status in the Orders settings. Order changes to SENT status when a tracking number is added to the order and the seller has enabled corresponding setting (see: here). Order can be switched to RETURNED status when both the buyer returns all order's items and the seller makes a refund for all of the order's items (either automatically or manually, see: here). The RETURNED status cannot be set by the seller - it changes automatically when corresponding setting is enabled in sale settings (see: here).

shipmentSummary	
object (CheckoutFormFulfillmentShipmentSummary)
provider	
object (CheckoutFormFulfillmentProvider)
Responses
204 Fulfillment set successfully
401 Authentication failed, e.g. token is expired
404 Order not found or doesn’t belong to the seller
409 Conflict. Provided revision is outdated.
422 Some of the provided data is invalid, e.g. unrecognized status value or given status is not allowed to be set (e.g. RETURNED status).

put
/order/checkout-forms/{id}/fulfillment
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"status": "SENT",
"shipmentSummary": {
"lineItemsSent": "SOME"
},
"provider": {
"id": "SELLER"
}
}
Response samples
409422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"errors": [
{}
]
}
Set line items' serial numbers
Use to set serial numbers in the given line items of seller order. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string
Order identifier.

query Parameters
checkoutForm.revision	
string
Example: checkoutForm.revision=819b5836
Checkout form revision.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "en-US"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
lineItems
required
Array of objects (CheckoutFormLineItemSetSerialNumbersRequest)
Responses
204 Serial numbers set successfully
401 Authentication failed, e.g. token is expired
404 Order or line item not found or doesn’t belong to the seller
409 Conflict. Provided revision is outdated.
422 Some of the provided data is invalid, e.g. quantity of serial numbers exceeds the quantity of the line item, or the number of serial number modifications is exceeded, or line item ids in the request body are duplicated.

post
/order/checkout-forms/{id}/serial-numbers
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"lineItems": [
{}
]
}
Response samples
409422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"errors": [
{}
]
}
Get order invoices details
Use to get invoices details including antivirus scan results and EPT invoice verification status. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string
Order identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "en-US"
Example: en-US
Expected language of messages.

Responses
200 Invoices fetched successfully
403 You do not have permission to access this order
404 Order with given id does not exist

get
/order/checkout-forms/{id}/invoices
Response samples
200403404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"orderMode": "UKRAINE_EXPORT",
"invoices": [
{}
],
"links": [
{}
],
"hasExternalInvoices": false
}
Post new invoice
Use to add new invoice metadata. Before you send an invoice file, you need to initialize the invoice instance with the required parameters. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string
Order identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "en-US"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
request

file
required
object (CheckFormsNewOrderInvoiceFile)
invoiceNumber	
string
Responses
201 Invoice created successfully
403 You do not have permission to access this order
404 Order with given id does not exist
409 Order with given id already has seller invoice
422 Some of the provided data is invalid or order does not allow an invoice or order's payment is rejected or previously uploaded file is still in scanning.
429 You're trying to add another metadata too fast. Upload a file to previously added metadata or wait a few seconds before adding next metadata.

post
/order/checkout-forms/{id}/invoices
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"file": {
"name": "invoice.pdf"
},
"invoiceNumber": "string"
}
Response samples
201403404409422429
Content type
application/vnd.allegro.public.v1+json

Copy
{
"id": "56ae349d-8045-4bb3-adcc-7cf6fb420f61"
}
Upload invoice file
Use to upload invoice file to match created invoice metadata. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string
Order identifier.

invoiceId
required
string
Invoice identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "en-US"
Example: en-US
Expected language of messages.

Request Body schema: application/pdf
string <binary>
File in a binary format

Responses
200 Invoice file uploaded successfully
403 You do not have permission to access this order
404 Order or invoice with given id does not exist
409 Invoice with given id already has invoice file uploaded
413 The file is too large. Max file size is 3MB
422 Uploaded file is empty or order's payment is rejected

put
/order/checkout-forms/{id}/invoices/{invoiceId}/file
Response samples
403404409413422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"errors": [
{}
]
}
Upload URL to billing documents
Used to upload a URL to a billing document. You can add up to 10 links.

Authorizations:
bearer-token-for-user
path Parameters
orderId
required
string
Order identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "en-US"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
url
required
string
Responses
201 URL to billing document uploaded successfully
403 You do not have permission to access this order
404 Order with the given ID does not exist
409 The given URL to the billing document already exists
422 The given URL is invalid

post
/order/{orderId}/billing-documents/links
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
{
"url": "string"
}
Response samples
403404409422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"errors": [
{}
]
}
Get Allegro pickup drop off points
Get a list of Allegro pickup drop off points. Read more: PL / EN.

Authorizations:
bearer-token-for-applicationbearer-token-for-user
query Parameters
carriers	
Array of strings (AllegroCarrier)
Items Enum: "UPS" "ALLEGRO_ONE_KURIER" "DPD"
Example: carriers=ALLEGRO_ONE_KURIER
List of carrier ids to filter the drop off/pick up points to only the ones where any of the listed carriers operate. In case of an empty list, all points are returned.

header Parameters
If-Modified-Since	
string <<day-name>, <day> <month> <year> <hour>:<minute>:<second> GMT>
Example: Sat, 01 Dec 2018 10:00:00 GMT
Date of last data modification. If data has been modified after specified date, full set of data is returned. If header is not specified, full set of data is returned. Date has to be provided in HTTP-date format. Information about date (the same HTTP-date format) of last modified data is available in response - Last-Modified.

Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Returns a list of Allegro pickup drop off points
304 Data has not been modified after the date provided in If-Modified-Since header.
400 Bad request. Invalid query parameters.
401 Authentication failed, e.g. token is expired

get
/order/carriers/ALLEGRO/points
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"points": [
{}
]
}
Get carrier parcel tracking history
Get tracking history for parcels. Read more: PL / EN.

Authorizations:
bearer-token-for-applicationbearer-token-for-user
path Parameters
carrierId
required
string
Carrier identifier.

query Parameters
waybill
required
Array of strings <= 20 items
Waybill number (parcel tracking number). Example: waybill=AAA0000E5D201&waybill=BBB00000E5D202 - returns parcel tracking history for AAA0000E5D201 as well as for BBB00000E5D202.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Returns parcel tracking history for given waybills
400 Bad request, e.g. unknown carrier id, missing or too many waybills in query parameter
401 Unauthorized, e.g. token is expired

get
/order/carriers/{carrierId}/tracking
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"carrierId": "ALLEGRO",
"waybills": [
{}
]
}
Payments
Payment operations history
Use this endpoint to get the list of the seller payment operations. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
wallet.type	
string
Default: "AVAILABLE"
Enum: "AVAILABLE" "WAITING"
Type of the wallet: * AVAILABLE - operations available for payout. * WAITING - operations temporarily suspended for payout.

wallet.paymentOperator	
string
Enum: "PAYU" "P24" "AF" "AF_P24" "AF_PAYU"
Payment operator: * PAYU - operations processed by PAYU operator. * P24 - operations processed by PRZELEWY24 operator. * AF - operations processed by Allegro Finance operator. * AF_P24 - operations processed by Allegro Finance with PRZELEWY24. * AF_PAYU - operations processed by Allegro Finance with PAYU.

payment.id	
string <uuid>
The payment ID.

participant.login	
string
Login of the participant. In case of REFUND_INCREASE operation this is the login of the seller, in other cases, of the buyer.

occurredAt.gte	
string <date-time>
Example: occurredAt.gte=2019-05-08T09:45:20.818Z
The minimum date and time of operation occurrence in ISO 8601 format.

occurredAt.lte	
string <date-time>
Example: occurredAt.lte=2019-05-08T09:45:20.818Z
The maximum date and time of operation occurrence in ISO 8601 format.

group	
Array of strings
Items Enum: "INCOME" "OUTCOME" "REFUND" "BLOCKADES"
Group of operation types: * INCOME - CONTRIBUTION, SURCHARGE, CORRECTION, DEDUCTION_INCREASE, LOAN_DEDUCTION_INCREASE, COMPENSATION, COMPENSATION_COD_INCREASE, TOP_UP, PAYOUT_SWEEP_INCREASE, PAYOUT_SWEEP_CANCEL_INCREASE. * OUTCOME - PAYOUT, PAYOUT_CANCEL, DEDUCTION_CHARGE, LOAN_DEDUCTION_CHARGE, COMPENSATION_COD_CHARGE, PAYOUT_SWEEP_CHARGE, PAYOUT_SWEEP_CANCEL_CHARGE. * REFUND - REFUND_CHARGE, REFUND_CANCEL, REFUND_INCREASE, CORRECTION, PROVIDER_REFUND_TRANSFER_CHARGE, PROVIDER_REFUND_TRANSFER_INCREASE. * BLOCKADES - BLOCKADE, BLOCKADE_RELEASE.

marketplaceId	
string
Enum: "allegro-pl" "allegro-cz"
Example: marketplaceId=allegro-pl
The marketplace ID where operation was made. When the parameter is omitted, searches for operations with all marketplaces. Note, that there are operations not assigned to any marketplace.

currency	
string
Example: currency=PLN
Currency of the operations.

limit	
integer <int32> [ 1 .. 50 ]
Default: 50
Number of returned operations.

offset	
integer <int32> [ 0 .. 10000 ]
Default: 0
Index of the first returned payment operation from all search results.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 The payment operations history for given search criteria returned successfully.
401 Unauthorized
422 Returned when any of the given search parameters have an invalid value or when the search result reached the limit of found operations - 10000.

get
/payments/payment-operations
Response samples
200422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"paymentOperations": [
{}
],
"count": 50,
"totalCount": 123
}
Initiate a refund of a payment
Use this endpoint to initiate a refund of a payment. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
payment
required
object (RefundPayment)
Payment affected by refund operation.

order
required
object (RefundOrder)
Order affected by refund operation.

commandId
required
string
Command UUID. If empty, idempotency will not be supported.

reason
required
string
Enum: "REFUND" "COMPLAINT" "PRODUCT_NOT_AVAILABLE" "PAID_VALUE_TOO_LOW" "OVERPAID" "CANCELLED_BY_BUYER" "NOT_COLLECTED"
Reason for a payment refund.

lineItems	
Array of objects (RefundLineItem)
List of order's line items which can be refunded.

deposits	
Array of objects (RefundLineItemDeposit)
List of refundable deposits for the order's line items.

delivery	
object
Payment refund for delivery.

overpaid	
object
Payment refund for overpaid.

surcharges	
Array of objects (PaymentsSurcharge)
List of surcharges for payment which can be refunded.

additionalServices	
object
Payment refund for additional services.

sellerComment	
string <= 250 characters
Sellers optional justification for refund.

Responses
200 Refund request created successfully.
400 Syntactically incorrect request.
401 Unauthorized.
403 Forbidden
404 Payment not found.
422 Unprocessable Entity.

post
/payments/refunds
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"payment": {
"id": "a6bee8b2-8b4e-11e9-8918-07b31163120a"
},
"order": {
"id": "a114b176-4833-451c-84dc-c37463793417"
},
"commandId": "14e142cf-e8e0-48cc-bcf6-399b5fd90b32",
"reason": "REFUND",
"lineItems": [
{}
],
"deposits": [
{}
],
"delivery": {
"value": {}
},
"overpaid": {
"value": {}
},
"surcharges": [
{}
],
"additionalServices": {
"value": {}
},
"sellerComment": "Example seller comment."
}
Response samples
200400401403404422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "09f0b4cc-7880-11e9-8f9e-2a86e4085a59",
"payment": {
"id": "a6bee8b2-8b4e-11e9-8918-07b31163120a"
},
"order": {
"id": "a114b176-4833-451c-84dc-c37463793417"
},
"reason": "REFUND",
"status": "SUCCESS",
"createdAt": "2017-05-17T08:36:57.292+02:00",
"totalValue": {
"amount": "123.45",
"currency": "PLN"
},
"lineItems": [
{}
],
"deposits": [
{}
],
"delivery": {
"value": {}
},
"overpaid": {
"value": {}
},
"surcharges": [
{}
],
"additionalServices": {
"value": {}
},
"sellerComment": "Example seller comment."
}
Get a list of refunded payments
Get a list of refunded payments. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
limit	
integer <int32> [ 1 .. 100 ]
Default: 50
Number of returned operations.

offset	
integer <int32> >= 0
Default: 0
Index of the first returned payment operation from all search results.

id	
string <uuid>
ID of the refund.

payment.id	
string <uuid>
ID of the payment.

order.id	
string <uuid>
ID of the order.

occurredAt.gte	
string <date-time>
Example: occurredAt.gte=2019-05-08T09:45:43.818Z
Minimum date and time when the refund occurred provided in ISO 8601 format.

occurredAt.lte	
string <date-time>
Example: occurredAt.lte=2019-05-08T09:45:32.818Z
Maximum date and time when the refund occurred provided in ISO 8601 format.

status	
Array of strings
Items Enum: "WAITING" "IN_PROGRESS" "SUCCESS" "CANCELED" "PARTIAL"
Current status of payment refund.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 List of payments refunds returned successfully.
401 Unauthorized
403 Forbidden
422 Unprocessable Entity. Returned when any of the given search parameters have an invalid value.

get
/payments/refunds
Response samples
200401403422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"refunds": [
{}
],
"count": 50,
"totalCount": 123
}
Post Purchase Issues
Get the user's post purchase issues
Use this resource to get the list of your disputes and claims ordered by descending opened date. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
checkoutForm.id	
string <uuid>
Example: checkoutForm.id=29738e61-7f6a-11e8-ac45-09db60ede9d6
Checkout form identifier.

limit	
integer <int32> [ 1 .. 100 ]
Default: 10
The maximum number of issues in a response.

offset	
integer <int32> >= 0
Default: 0
Index of first returned issue.

status	
Array of strings (PostPurchaseIssueStatus)
Items Enum: "DISPUTE_CLOSED" "DISPUTE_ONGOING" "DISPUTE_UNRESOLVED" "CLAIM_SUBMITTED" "CLAIM_ACCEPTED" "CLAIM_REJECTED"
Example: status=DISPUTE_ONGOING
Filter issues with given set of statuses.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of subject field.

Responses
200 OK
401 Unauthorized
404 Not Found
422 Unprocessable Entity

get
/sale/issues
Response samples
200
Content type
application/vnd.allegro.beta.v1+json

Copy
Expand allCollapse all
{
"issues": [
{},
{}
]
}
Get a single dispute or claim
Use this resource to get a single dispute or claim. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
issueId
required
string <uuid>
Dispute or claim identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of subject field.

Responses
200 OK
401 Unauthorized
403 Forbidden
404 Not Found

get
/sale/issues/{issueId}
Response samples
200
Content type
application/vnd.allegro.beta.v1+json
Example

Issue representing a dispute
Issue representing a dispute

Copy
Expand allCollapse all
{
"id": "6f552f2e-9626-46b3-af09-bfdbf9690d65",
"type": "DISPUTE",
"referenceNumber": null,
"decisionDueDate": null,
"openedDate": "2025-06-10T12:12:12.019Z",
"subject": "nie otrzymałem towaru po wpłacie",
"buyer": {
"id": "e781964b-ed6b-4f2b-b915-6c3f7495d6ee",
"login": "example-user"
},
"checkoutForm": {
"id": "94092826-f0e2-47ca-b8d1-94fd7cb82c33",
"createdAt": "2025-05-10T15:10:10.019Z"
},
"currentState": {
"status": "DISPUTE_ONGOING",
"statusDueDate": null,
"returnRequired": null,
"chatActive": true
},
"chat": {
"lastMessage": {},
"messagesCount": 2,
"initialMessage": {}
},
"expectations": [ ],
"description": "Zwrot 27 zł",
"offer": null,
"product": null,
"reason": null,
"right": "WARRANTY",
"attachments": [
{}
]
}
Get the messages and state claim changes within a post purchase issue
Use this resource to get the list of messages and state changes within a dispute or claim. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
issueId
required
string <uuid>
Dispute or claim identifier.

query Parameters
limit	
integer <int32> [ 1 .. 100 ]
Default: 10
The maximum number of messages within issue returned in a response.

offset	
integer <int32> >= 0
Default: 0
Index of first returned message within issue.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 OK
401 Unauthorized
403 Forbidden
404 Not Found

get
/sale/issues/{issueId}/chat
Response samples
200
Content type
application/vnd.allegro.beta.v1+json

Copy
Expand allCollapse all
{
"chat": [
{}
]
}
Add a message to an issue
Use this resource to post a message in certain issue. At least one of fields: 'text', 'attachment' has to be present. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
issueId
required
string <uuid>
Dispute or claim identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.beta.v1+json
Message request

text
required
string <= 20000 characters
attachments	
Array of objects (PostPurchaseIssueAttachmentId)
type
required
string
Enum: "REGULAR" "END_REQUEST" "RETURN_REQUIRED_SELLER_LABEL" "RETURN_REQUIRED_CUSTOM" "RETURN_NOT_REQUIRED"
Type of message, END_REQUEST is only allowed for disputes while return-related types are only allowed for claims.

Responses
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Dispute is in a state that forbids adding new messages
422 Unprocessable Entity

post
/sale/issues/{issueId}/message
Request samples
Payload
Content type
application/vnd.allegro.beta.v1+json

Copy
Expand allCollapse all
{
"text": "Good morning. Please clarify the problem.",
"attachments": [
{}
],
"type": "REGULAR"
}
Response samples
201
Content type
application/vnd.allegro.beta.v1+json

Copy
Expand allCollapse all
{
"id": "a9927fcc-f11a-436a-9f8d-177fd37d393c",
"text": "Dzień dobry. Proszę o doprecyzowanie problemu.",
"attachments": [
{}
],
"author": {
"login": "example-seller",
"role": "SELLER"
},
"createdAt": "2025-06-10T12:12:12.019Z"
}
Change status of a claim
Change the formal status of a claim, for example accept or reject it. Not a valid operation for disputes. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
issueId
required
string <uuid>
Claim identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.beta.v1+json
Claim status change

status
required
string
Enum: "ACCEPTED_REPAIR" "ACCEPTED_REFUND" "ACCEPTED_EXCHANGE" "ACCEPTED_PARTIAL_REFUND" "REJECTED_ADDITIONAL_REQUIREMENTS_NOT_COMPLETED" "REJECTED_PRODUCT_NOT_RETURNED" "REJECTED_PRODUCT_DAMAGED_BY_USER" "REJECTED_PRODUCT_CONFORMS_TO_CONTRACT" "REJECTED_MINOR_DEFECT" "REJECTED_OTHER" "REJECTED_CLAIM_WITHDRAWN_BY_BUYER"
message
required
string
partialRefund	
object (Price)
The price data.

Responses
200 Status changed correctly
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found

post
/sale/issues/{issueId}/status
Request samples
Payload
Content type
application/vnd.allegro.beta.v1+json

Copy
Expand allCollapse all
{
"status": "ACCEPTED_PARTIAL_REFUND",
"message": "I accept a partial refund",
"partialRefund": {
"amount": "123.45",
"currency": "PLN"
}
}
Create an attachment declaration
Use this resource to post an attachment declaration. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.beta.v1+json
A detailed declaration of a file to be uploaded

fileName
required
string
size
required
integer >= 1
Responses
201 Created
401 Unauthorized
403 Forbidden
422 Unprocessable Entity

post
/sale/issues/attachments
Request samples
Payload
Content type
application/vnd.allegro.beta.v1+json

Copy
{
"fileName": "example-file.jpg",
"size": 216772
}
Response samples
201
Content type
application/vnd.allegro.beta.v1+json

Copy
{
"id": "0c3c607d-d1de-4c6e-8db7-48c5b88a795d"
}
Upload an attachment
Upload a post purchase issue message attachment. This operation should be used after creating an attachment declaration with POST /sale/issues/attachments Important! You can find the URL address to upload the file to our server in the Location response header of POST /sale/issues/attachments. The URL is unique and one-time. As its format may change in time, you should always use the address from the header. Do not compose the address on your own. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
attachmentId
required
string <uuid>
Attachment identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: 
image/png
image/png
string <binary>
File in a binary format

Responses
200 File uploaded correctly
400 Syntactically incorrect request
401 Invalid or missing bearer token
413 File is too big
415 Unsupported media type
422 Unprocessable Entity

put
/sale/issues/attachments/{attachmentId}
Response samples
200
Content type
application/vnd.allegro.beta.v1+json

Copy
{
"id": "0c3c607d-d1de-4c6e-8db7-48c5b88a795d"
}
Get an attachment
Use this resource to get an attachment. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
attachmentId
required
string <uuid>
Attachment identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 OK
401 Unauthorized
403 Forbidden
404 Not Found

get
/sale/issues/attachments/{attachmentId}
Shipment management
Get available delivery options
Use this resource to retrieve two order characteristics. The first is a pre-populated request body for creating a shipment in SwA. The second is a list of possible delivery types for processing the order, including their limits. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
orderId
required
string <UUID>
Example: 09f0b4cc-7880-11e9-8f9e-2a86e4085a59
Order ID.

Responses
200 OK
401 Unauthorized
403 Forbidden
504 Gateway Timeout

get
/shipment-management/delivery-proposals/{orderId}
Response samples
200401403504
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"orderId": "string",
"suggestedInput": {
"deliveryMethodId": "c3066682-97a3-42fe-9eb5-3beeccab840c",
"credentialsId": "c9e6f40a-3d25-48fc-838c-055ceb1c5bc0",
"sender": {},
"receiver": {},
"referenceNumber": "abcd1234",
"packages": [],
"insurance": {},
"cashOnDelivery": {},
"labelFormat": "ZPL",
"additionalServices": [],
"additionalProperties": {}
},
"deliveryOptions": [
{}
]
}
Get available delivery services Deprecated
Use this resource to get delivery services available for user. It returns services provided by Allegro and contracts with carriers owned by user and configured by GUI. Read more: PL / EN.
This resource is deprecated and will be removed in Q1 2027. Consider using the new resource '/shipment-management/delivery-proposals/{orderId}' resource instead.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 OK
401 Unauthorized
403 Forbidden
504 Gateway Timeout

get
/shipment-management/delivery-services
Response samples
200401403504
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"services": [
{}
]
}
Create new shipment
Use this resource to create shipment for delivery. Read more: PL / EN. Please check also new resource '/shipment-management/delivery-proposals/{orderId}' to get prefilled request body for this resource.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
commandId	
string
Command UUID. If empty, then system generate new one.

input
required
object (ShipmentCreateRequestDto)
Responses
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
504 Gateway Timeout

post
/shipment-management/shipments/create-commands
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"commandId": "14e142cf-e8e0-48cc-bcf6-399b5fd90b32",
"input": {
"deliveryMethodId": "c3066682-97a3-42fe-9eb5-3beeccab840c",
"credentialsId": "c9e6f40a-3d25-48fc-838c-055ceb1c5bc0",
"sender": {},
"receiver": {},
"referenceNumber": "abcd1234",
"packages": [],
"insurance": {},
"cashOnDelivery": {},
"labelFormat": "ZPL",
"additionalServices": [],
"additionalProperties": {}
}
}
Response samples
200400401403504
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"commandId": "14e142cf-e8e0-48cc-bcf6-399b5fd90b32",
"input": {
"deliveryMethodId": "c3066682-97a3-42fe-9eb5-3beeccab840c",
"credentialsId": "c9e6f40a-3d25-48fc-838c-055ceb1c5bc0",
"sender": {},
"receiver": {},
"referenceNumber": "abcd1234",
"packages": [],
"insurance": {},
"cashOnDelivery": {},
"labelFormat": "ZPL",
"additionalServices": [],
"additionalProperties": {}
}
}
Get shipment creation command status
Use this resource to get shipment creation status. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Example: 14e142cf-e8e0-48cc-bcf6-399b5fd90b32
Command UUID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
504 Gateway Timeout

get
/shipment-management/shipments/create-commands/{commandId}
Response samples
200400401403504
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"commandId": "14e142cf-e8e0-48cc-bcf6-399b5fd90b32",
"status": "SUCCESS",
"errors": [
{}
],
"shipmentId": "ba88f0fb-acf3-438a-877e-580da50c0874"
}
Cancel shipment
Use this resource to cancel parcel. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
commandId	
string
Command UUID. If empty, then system generate new one.

input
required
object (ShipmentCancelRequestDto)
Responses
200 OK
400 Bad request
401 Unauthorized
403 Forbidden

post
/shipment-management/shipments/cancel-commands
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"commandId": "14e142cf-e8e0-48cc-bcf6-399b5fd90b32",
"input": {
"shipmentId": "ba88f0fb-acf3-438a-877e-580da50c0874"
}
}
Response samples
200400401403
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"commandId": "14e142cf-e8e0-48cc-bcf6-399b5fd90b32",
"input": {
"shipmentId": "ba88f0fb-acf3-438a-877e-580da50c0874"
}
}
Get shipment cancellation status
Use this resource to get parcel cancellation status. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Example: 14e142cf-e8e0-48cc-bcf6-399b5fd90b32
Command UUID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
504 Gateway Timeout

get
/shipment-management/shipments/cancel-commands/{commandId}
Response samples
200400401403504
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"commandId": "14e142cf-e8e0-48cc-bcf6-399b5fd90b32",
"status": "SUCCESS",
"errors": [
{}
],
"shipmentId": "ba88f0fb-acf3-438a-877e-580da50c0874"
}
Get shipment details
Use this resource to get parcel details. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
shipmentId
required
string
Shipment id.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
504 Gateway Timeout

get
/shipment-management/shipments/{shipmentId}
Response samples
200400401403404504
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "ba88f0fb-acf3-438a-877e-580da50c0874",
"deliveryMethodId": "c3066682-97a3-42fe-9eb5-3beeccab840c",
"credentialsId": "c9e6f40a-3d25-48fc-838c-055ceb1c5bc0",
"sender": {
"name": "Jan Kowalski",
"company": "Allegro.pl sp. z o.o.",
"street": "Główna 30",
"postalCode": "10-200",
"city": "Warszawa",
"state": "AL",
"countryCode": "PL",
"email": "email@mail.com",
"phone": "+48500600700",
"point": "A1234567"
},
"receiver": {
"name": "Jan Kowalski",
"company": "Allegro.pl sp. z o.o.",
"street": "Główna 30",
"postalCode": "10-200",
"city": "Warszawa",
"state": "AL",
"countryCode": "PL",
"email": "email@mail.com",
"phone": "+48500600700",
"point": "A1234567"
},
"referenceNumber": "abcd1234",
"packages": [
{}
],
"insurance": {
"amount": "23.47",
"currency": "PLN"
},
"cashOnDelivery": {
"amount": "2.50",
"currency": "PLN",
"ownerName": "Jan Kowalski",
"iban": "PL48109024022441789739167589"
},
"createdDate": "2020-01-11T09:36:57.00Z",
"canceledDate": null,
"carrier": "ALLEGRO",
"labelFormat": "PDF",
"additionalServices": [
"ADDITIONAL_HANDLING"
],
"additionalProperties": {
"additionalPropertyId1": "FIRST_MILE_CARRIER",
"additionalPropertyId2": "FIRST_MILE_CARRIER"
},
"transport": [
"InPost"
],
"pickupAvailable": true
}
Get shipments labels
Use this resource to get label for created shipment.
Returned content type depends on created shipment. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
shipmentIds
required
Array of strings [ 1 .. 2147483647 ] items
pageSize	
string
Enum: "A4" "A6"
Label page format. Only for PDF file.

cutLine	
boolean
Put additional cut lines. Only for PDF file with A4 size.

summaryReport	
object
Set of parameters for creating extra labels with shipment summary report. If null then report will be omitted.

Responses
200 OK
204 No Label For Given Parcel
400 Bad Request
401 Unauthorized
403 Forbidden
404 Shipment Not Found
504 Gateway Timeout

post
/shipment-management/label
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"shipmentIds": [
"ba88f0fb-acf3-438a-877e-580da50c0874"
],
"pageSize": "A6",
"cutLine": true,
"summaryReport": {
"placement": "LAST",
"fields": []
}
}
Response samples
400401403404504
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"errors": [
{}
]
}
Get shipments protocol
Protocol availability depends on Carrier. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
shipmentIds
required
Array of strings [ 1 .. 2147483647 ] items
Responses
200 OK
204 No Protocol For Given Parcels
400 Bad Request
401 Unauthorized
403 Forbidden
404 Shipment Not Found
504 Gateway Timeout

post
/shipment-management/protocol
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"shipmentIds": [
"ba88f0fb-acf3-438a-877e-580da50c0874"
]
}
Response samples
400401403404504
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"errors": [
{}
]
}
Get shipments pickup proposals
Use this resource to get parcels pickup date proposals. Pickup takes place, when courier arrives to take parcels for shipment. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
shipmentIds
required
Array of strings [ 1 .. 100 ] items
An array of unique shipment identifiers to retrieve details for. Must contain between 1 and 100 IDs.

readyDate	
string
Date when shipments will be ready.

address
required
object (PickupAddressDto)
Address where the courier will pick up parcels to be sent.

Responses
200 OK
400 Bad request
401 Unauthorized
403 Forbidden
504 Gateway Timeout

post
/shipment-management/pickup-proposals
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"shipmentIds": [
"ba88f0fb-acf3-438a-877e-580da50c0874"
],
"readyDate": "2020-01-01",
"address": {
"name": "Jan Kowalski",
"company": "Allegro.pl sp. z o.o.",
"street": "Główna 30",
"postalCode": "10-200",
"city": "Warszawa",
"state": "AL",
"countryCode": "PL",
"email": "email@mail.com",
"phone": "+48500600700"
}
}
Response samples
200400401403504
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
[
{
"proposals": [],
"address": {}
}
]
Request shipments pickup
Use this resource to request a pickup of shipments. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
commandId	
string
Command UUID. If empty, then system generate new one.

input
required
object (PickupCreateRequestDto)
Responses
200 OK
400 Bad request
401 Unauthorized
403 Forbidden

post
/shipment-management/pickups/create-commands
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"commandId": "14e142cf-e8e0-48cc-bcf6-399b5fd90b32",
"input": {
"shipmentIds": [],
"pickupTime": {},
"address": {}
}
}
Response samples
200400401403
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"commandId": "14e142cf-e8e0-48cc-bcf6-399b5fd90b32",
"input": {
"shipmentIds": [],
"pickupTime": {},
"address": {}
}
}
Create pickup command status
Use this resource to get pickup request status. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
commandId
required
string
Example: 14e142cf-e8e0-48cc-bcf6-399b5fd90b32
Command UUID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
504 Gateway Timeout

get
/shipment-management/pickups/create-commands/{commandId}
Response samples
200400401403504
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"commandId": "14e142cf-e8e0-48cc-bcf6-399b5fd90b32",
"status": "SUCCESS",
"errors": [
{}
],
"pickupId": "14e142cf-e8e0-48cc-bcf6-399b5fd90b32",
"carrierPickupId": "A10234234523"
}
Get pickup details
Use this resource to get pickup details. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
pickupId
required
string
Pickup ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
504 Gateway Timeout

get
/shipment-management/pickups/{pickupId}
Response samples
200400401403404504
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "ba88f0fb-acf3-438a-877e-580davf34874",
"carrierPickupId": "AD2923111",
"carrier": "PACKETA",
"pickupCarrier": "POCZTA_POLSKA",
"address": {
"name": "Jan Kowalski",
"company": "Allegro.pl sp. z o.o.",
"street": "Główna 30",
"postalCode": "10-200",
"city": "Warszawa",
"state": "AL",
"countryCode": "PL",
"email": "email@mail.com",
"phone": "+48500600700",
"point": "A1234567"
},
"shipmentIds": [
"ba88f0fb-acf3-438a-877e-58123vf34874"
],
"waybills": [
"1019374227038U"
]
}
Customer returns
[BETA] Get customer returns by provided query parameters
Use this resource to get all customer returns filtered by query parameters. Read more: PL / EN. This resource is limited to 25 requests per second for a single user and 50 requests per second for clientId.

Authorizations:
bearer-token-for-user
query Parameters
customerReturnId	
string
One or more customer return id's.

orderId	
string
One or more order id's.

buyer.email	
string
One or more buyer emails.

buyer.login	
string
One or more buyer logins.

items.offerId	
string
One or more returned item offer id's.

items.name	
string
One or more item names.

parcels.waybill	
string
One or more waybill id's.

parcels.transportingWaybill	
string
Waybill ids as generated by carriers physically transporting the parcel. Will be null if there's only one carrier involved in a parcel shipment.

parcels.carrierId	
string
One or more carrier id's.

parcels.transportingCarrierId	
string
Carrier id of a carrier physically transporting the parcel. Will be null if there's only one carrier involved in a parcel shipment.

parcels.sender.phoneNumber	
string
One or more phone numbers.

referenceNumber	
string
One or more reference numbers.

from	
string
The ID of the last seen customer return. Customer returns created after the given customer return will be returned.

createdAt.gte	
string
Date of the return in ISO 8601 format to search by greater or equal.

createdAt.lte	
string
Date of the return in ISO 8601 format to search by lower or equal.

marketplaceId	
string
The marketplace ID where operation was made. When the parameter is omitted, searches for operations with all marketplaces.

status	
string
Current return timeline statuses. The allowed values are:

CREATED
DISPATCHED
IN_TRANSIT
DELIVERED
FINISHED
FINISHED_APT
REJECTED
COMMISSION_REFUND_CLAIMED
COMMISSION_REFUNDED
WAREHOUSE_DELIVERED
WAREHOUSE_VERIFICATION.
limit	
integer <int32> [ 1 .. 1000 ]
Default: 100
Limit of customer returns per page.

offset	
integer <int32> >= 0
Default: 0
The offset of elements in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Successfully retrieved customer returns.
400 Bad request.
401 Unauthorized
403 Forbidden
406 Not Acceptable

get
/order/customer-returns
Response samples
200400401403406
Content type
application/vnd.allegro.beta.v1+json

Copy
Expand allCollapse all
{
"count": 1,
"customerReturns": [
{}
]
}
[BETA] Get customer return by id
Use this resource to get customer returns by its identifier. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
customerReturnId
required
string
Id of the customer return.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Successfully retrieved customer return.
400 Bad request.
401 Unauthorized
403 Forbidden
404 Not found
406 Not Acceptable

get
/order/customer-returns/{customerReturnId}
Response samples
200400401403404406
Content type
application/vnd.allegro.beta.v1+json

Copy
Expand allCollapse all
{
"id": "a3405c27-b01c-4357-9bea-e13925708b46",
"isFulfillment": false,
"createdAt": "2020-01-11T09:36:57.00Z",
"referenceNumber": "1234/Z04A",
"orderId": "a3405c27-b01c-4357-9bea-e13925708b46",
"buyer": {
"email": "user-email@allegro.pl",
"login": "User_Login"
},
"items": [
{}
],
"refund": {
"bankAccount": {}
},
"parcels": [
{}
],
"rejection": {
"code": "REFUND_REJECTED",
"reason": "Returned item is damaged.",
"createdAt": "2020-01-11T09:36:57.663+01:00"
},
"marketplaceId": "allegro-pl",
"status": "DELIVERED"
}
[BETA] Reject customer return refund
Use this resource to reject customer return refund with provided reason. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
customerReturnId
required
string
Id of the customer return.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.beta.v1+json
rejection
required
object
Refund rejection

Responses
200 Successfully rejected customer return.
400 Bad request.
401 Unauthorized
403 Forbidden
406 Not Acceptable
422 Unprocessable Entity. Might occur when customer return has already been rejected

post
/order/customer-returns/{customerReturnId}/rejection
Request samples
Payload
Content type
application/vnd.allegro.beta.v1+json

Copy
Expand allCollapse all
{
"rejection": {
"code": "REFUND_REJECTED",
"reason": "Returned item is damaged."
}
}
Response samples
200400401403406422
Content type
application/vnd.allegro.beta.v1+json

Copy
Expand allCollapse all
{
"id": "a3405c27-b01c-4357-9bea-e13925708b46",
"isFulfillment": false,
"createdAt": "2020-01-11T09:36:57.00Z",
"referenceNumber": "1234/Z04A",
"orderId": "a3405c27-b01c-4357-9bea-e13925708b46",
"buyer": {
"email": "user-email@allegro.pl",
"login": "User_Login"
},
"items": [
{}
],
"refund": {
"bankAccount": {}
},
"parcels": [
{}
],
"rejection": {
"code": "REFUND_REJECTED",
"reason": "Returned item is damaged.",
"createdAt": "2020-01-11T09:36:57.663+01:00"
},
"marketplaceId": "allegro-pl",
"status": "DELIVERED"
}
Commission refunds
Get a refund application details
Use this resource to get refund application details. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
claimId
required
string
Refund application ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Successfully returned refund application.
400 Semantically incorrect request or provided conditions not correct.
401 Unauthorized.
403 Refund application does not belong to you.
404 Refund application not found.
406 Not Acceptable.
422 Unprocessable Entity.

get
/order/refund-claims/{claimId}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "09f0b4cc-7880-11e9-8f9e-2a86e4085a59",
"status": "IN_PROGRESS",
"quantity": 1,
"commission": {
"amount": 100,
"currency": "PLN"
},
"buyer": {
"id": "12345678"
},
"createdAt": "2019-08-24T14:15:22Z",
"lineItem": {
"id": "09f0b4cc-7880-11e9-8f9e-2a86e4085a59",
"quantity": 1,
"boughtAt": "2019-08-24T14:15:22Z",
"offer": {}
},
"type": "MANUAL"
}
Cancel a refund application
Use this resource to cancel a refund application. This cannot be undone. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
claimId
required
string
Refund application ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
204 Refund application was cancelled successfully.
400 Semantically incorrect request or provided conditions not correct.
401 Unauthorized.
403 Refund application does not belong to you.
404 Refund application not found.
406 Not Acceptable.
422 Refund application has already been processed.

delete
/order/refund-claims/{claimId}
Get a list of refund applications
Use this resource to get a list of refund applications based on the provided query parameters. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
lineItem.offer.id	
string
ID of the offer associated with the refund application.

buyer.id	
string
Id of the buyer that made the purchase associated with the refund application.

status	
string
Enum: "IN_PROGRESS" "WAITING_FOR_PAYMENT_REFUND" "GRANTED" "REJECTED" "REJECTED_AFTER_APPEAL" "CANCELLED" "APPEALED"
Status of the refund application.

limit	
integer <int32> [ 1 .. 100 ]
Default: 25
Maximum number of returned refund applications in response.

offset	
integer <int32> >= 0
Default: 0
Index of the first returned refund application from all search results.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Successfully returned list of refund applications.
400 Semantically incorrect request or provided conditions not correct.
401 Unauthorized.
403 Refund application does not belong to you.
406 Not Acceptable.
422 Unprocessable Entity.

get
/order/refund-claims
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"refundClaims": [
{}
],
"count": 0
}
Create a refund application
Use this resource to create a refund application. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
lineItem	
object
Purchase for which a refund application will be created.

quantity	
integer <int32> >= 1
Quantity of product for which the refund application will be created. Must be greater than zero.

Responses
201 The refund application was created successfully.
400 Semantically incorrect request or provided conditions not correct.
401 Unauthorized.
403 Forbidden.
406 Not Acceptable.
422 Unprocessable Entity.

post
/order/refund-claims
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"lineItem": {
"id": "string"
},
"quantity": 1
}
Response samples
201
Content type
application/vnd.allegro.public.v1+json

Copy
{
"id": "string"
}
After sale services
Get the user's return policies
Use this resource to get the seller's return policies. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
limit	
integer <int32> [ 1 .. 60 ]
Default: 60
The limit of elements in the response.

offset	
integer <int32> [ 0 .. 59 ]
Default: 0
The offset of elements in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Unauthorized
403 Forbidden
404 Not Found

get
/after-sales-service-conditions/return-policies
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"count": 0,
"returnPolicies": [
{}
]
}
Create new user's return policy
Use this resource to create a return policy definition. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Return Policy

name
required
string <= 200 characters
Return policy name.

isFulfillment
required
boolean
Indicates if the return policy is for One Fulfillment offers. Cannot be changed.

availability
required
object (ReturnPolicyAvailability)
withdrawalPeriod	
string
Period in ISO 8601 format. Only periods in full days are accepted.

returnCost	
object or null (ReturnPolicyReturnCost)
Can be null if availability range is 'DISABLED'.

address	
object or null (ReturnPolicyAddress)
The return address of the policy. Can be null if availability range is 'DISABLED'.

contact	
object or null (ReturnPolicyContactV1)
options	
object or null (ReturnPolicyOptions)
Can be null if availability range is 'DISABLED'.

Responses
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
422 Unprocessable Entity

post
/after-sales-service-conditions/return-policies
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"name": "string",
"isFulfillment": true,
"availability": {
"range": "RESTRICTED",
"restrictionCause": {}
},
"withdrawalPeriod": "P14D",
"returnCost": {
"coveredBy": "SELLER"
},
"address": {
"name": "Allegro.pl sp. z o.o.",
"street": "Grunwaldzka 182",
"postCode": "11-232",
"city": "Poznań",
"countryCode": "PL"
},
"contact": {
"phoneNumber": "123 123 123",
"email": "useridentifier@domain.com"
},
"options": {
"cashOnDeliveryNotAllowed": true,
"freeAccessoriesReturnRequired": true,
"refundLoweredByReceivedDiscount": true,
"businessReturnAllowed": false,
"collectBySellerOnly": false
}
}
Response samples
201
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "09f0b4cc-7880-11e9-8f9e-2a86e4085a59",
"isFulfillment": true,
"seller": {
"id": "string"
},
"name": "string",
"availability": {
"range": "RESTRICTED",
"restrictionCause": {}
},
"withdrawalPeriod": "P14D",
"returnCost": {
"coveredBy": "SELLER"
},
"address": {
"name": "Allegro.pl sp. z o.o.",
"street": "Grunwaldzka 182",
"postCode": "11-232",
"city": "Poznań",
"countryCode": "PL"
},
"contact": {
"phoneNumber": "123 123 123",
"email": "useridentifier@domain.com"
},
"options": {
"cashOnDeliveryNotAllowed": true,
"freeAccessoriesReturnRequired": true,
"refundLoweredByReceivedDiscount": true,
"businessReturnAllowed": false,
"collectBySellerOnly": false
}
}
Get the user's return policy
Use this resource to get a return policy details. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
returnPolicyId
required
string
The ID of the return policy.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Unauthorized
403 Forbidden
404 Not Found

get
/after-sales-service-conditions/return-policies/{returnPolicyId}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "09f0b4cc-7880-11e9-8f9e-2a86e4085a59",
"isFulfillment": true,
"seller": {
"id": "string"
},
"name": "string",
"availability": {
"range": "RESTRICTED",
"restrictionCause": {}
},
"withdrawalPeriod": "P14D",
"returnCost": {
"coveredBy": "SELLER"
},
"address": {
"name": "Allegro.pl sp. z o.o.",
"street": "Grunwaldzka 182",
"postCode": "11-232",
"city": "Poznań",
"countryCode": "PL"
},
"contact": {
"phoneNumber": "123 123 123",
"email": "useridentifier@domain.com"
},
"options": {
"cashOnDeliveryNotAllowed": true,
"freeAccessoriesReturnRequired": true,
"refundLoweredByReceivedDiscount": true,
"businessReturnAllowed": false,
"collectBySellerOnly": false
}
}
Change the user's return policy
Use this resource to modify the return policy details. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
returnPolicyId
required
string
The ID of the return policy.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Return Policy

name
required
string <= 200 characters
Return policy name.

availability
required
object (ReturnPolicyAvailability)
withdrawalPeriod	
string
Period in ISO 8601 format. Only periods in full days are accepted.

returnCost	
object or null (ReturnPolicyReturnCost)
Can be null if availability range is 'DISABLED'.

address	
object or null (ReturnPolicyAddress)
The return address of the policy. Can be null if availability range is 'DISABLED'.

contact	
object or null (ReturnPolicyContactV1)
options	
object or null (ReturnPolicyOptions)
Can be null if availability range is 'DISABLED'.

Responses
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
422 Unprocessable Entity

put
/after-sales-service-conditions/return-policies/{returnPolicyId}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"name": "Default",
"availability": {
"range": "RESTRICTED",
"restrictionCause": {}
},
"withdrawalPeriod": "P14D",
"returnCost": {
"coveredBy": "SELLER"
},
"address": {
"name": "Allegro.pl sp. z o.o.",
"street": "Grunwaldzka 182",
"postCode": "11-232",
"city": "Poznań",
"countryCode": "PL"
},
"contact": {
"phoneNumber": "123 123 123",
"email": "useridentifier@domain.com"
},
"options": {
"cashOnDeliveryNotAllowed": true,
"freeAccessoriesReturnRequired": true,
"refundLoweredByReceivedDiscount": true,
"businessReturnAllowed": false,
"collectBySellerOnly": false
}
}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "09f0b4cc-7880-11e9-8f9e-2a86e4085a59",
"isFulfillment": true,
"seller": {
"id": "string"
},
"name": "string",
"availability": {
"range": "RESTRICTED",
"restrictionCause": {}
},
"withdrawalPeriod": "P14D",
"returnCost": {
"coveredBy": "SELLER"
},
"address": {
"name": "Allegro.pl sp. z o.o.",
"street": "Grunwaldzka 182",
"postCode": "11-232",
"city": "Poznań",
"countryCode": "PL"
},
"contact": {
"phoneNumber": "123 123 123",
"email": "useridentifier@domain.com"
},
"options": {
"cashOnDeliveryNotAllowed": true,
"freeAccessoriesReturnRequired": true,
"refundLoweredByReceivedDiscount": true,
"businessReturnAllowed": false,
"collectBySellerOnly": false
}
}
Delete the user's return policy
Use this resource to delete a return policy definition.

Authorizations:
bearer-token-for-user
path Parameters
returnPolicyId
required
string
The ID of the return policy.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
204 No content
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found

delete
/after-sales-service-conditions/return-policies/{returnPolicyId}
Response samples
200
Content type
application/vnd.allegro.public.v1 +json

Copy
Expand allCollapse all
{
"id": "09f0b4cc-7880-11e9-8f9e-2a86e4085a59",
"isFulfillment": true,
"seller": {
"id": "string"
},
"name": "string",
"availability": {
"range": "RESTRICTED",
"restrictionCause": {}
},
"withdrawalPeriod": "P14D",
"returnCost": {
"coveredBy": "SELLER"
},
"address": {
"name": "Allegro.pl sp. z o.o.",
"street": "Grunwaldzka 182",
"postCode": "11-232",
"city": "Poznań",
"countryCode": "PL"
},
"contact": {
"phoneNumber": "123 123 123",
"email": "useridentifier@domain.com"
},
"options": {
"cashOnDeliveryNotAllowed": true,
"freeAccessoriesReturnRequired": true,
"refundLoweredByReceivedDiscount": true,
"businessReturnAllowed": false,
"collectBySellerOnly": false
}
}
Get the user's implied warranties
Use this resource to get the seller's implied warranties. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
limit	
integer <int32> [ 1 .. 60 ]
Default: 60
The limit of elements in the response.

offset	
integer <int32> [ 0 .. 59 ]
Default: 0
The offset of elements in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Unauthorized
403 Forbidden
404 Not Found

get
/after-sales-service-conditions/implied-warranties
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"count": 0,
"impliedWarranties": [
{}
]
}
Create new user's implied warranty
Use this resource to create an implied warranty definition. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Implied warranty

name	
string <= 200 characters
Warranty name.

individual	
object (ImpliedWarrantyPeriod)
corporate	
object (ImpliedWarrantyPeriod)
address	
object (AfterSalesServicesAddress)
description	
string <= 10240 characters
Implied warranty description.

Responses
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
422 Unprocessable Entity

post
/after-sales-service-conditions/implied-warranties
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"name": "Default",
"individual": {
"period": "P2Y"
},
"corporate": {
"period": "P2Y"
},
"address": {
"name": "Allegro.pl sp. z o.o.",
"street": "Grunwaldzka 182",
"postCode": "11-232",
"city": "Poznań",
"countryCode": "PL"
},
"description": "string"
}
Response samples
201
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "09f0b4cc-7880-11e9-8f9e-2a86e4085a59",
"seller": {
"id": "string"
},
"name": "string",
"individual": {
"period": "P2Y"
},
"corporate": {
"period": "P2Y"
},
"address": {
"name": "Allegro.pl sp. z o.o.",
"street": "Grunwaldzka 182",
"postCode": "11-232",
"city": "Poznań",
"countryCode": "PL"
},
"description": "string"
}
Get the user's implied warranty
Use this resource to get an implied warranty details. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
impliedWarrantyId
required
string
The ID of the implied warranty.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Unauthorized
403 Forbidden
404 Not Found

get
/after-sales-service-conditions/implied-warranties/{impliedWarrantyId}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "09f0b4cc-7880-11e9-8f9e-2a86e4085a59",
"seller": {
"id": "string"
},
"name": "string",
"individual": {
"period": "P2Y"
},
"corporate": {
"period": "P2Y"
},
"address": {
"name": "Allegro.pl sp. z o.o.",
"street": "Grunwaldzka 182",
"postCode": "11-232",
"city": "Poznań",
"countryCode": "PL"
},
"description": "string"
}
Change the user's implied warranty
Use this resource to modify the implied warranty details. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
impliedWarrantyId
required
string
The ID of the implied warranty.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Implied warranty

name	
string <= 200 characters
Warranty name.

individual	
object (ImpliedWarrantyPeriod)
corporate	
object (ImpliedWarrantyPeriod)
address	
object (AfterSalesServicesAddress)
description	
string <= 10240 characters
Implied warranty description.

Responses
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
422 Unprocessable Entity

put
/after-sales-service-conditions/implied-warranties/{impliedWarrantyId}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"name": "Default",
"individual": {
"period": "P2Y"
},
"corporate": {
"period": "P2Y"
},
"address": {
"name": "Allegro.pl sp. z o.o.",
"street": "Grunwaldzka 182",
"postCode": "11-232",
"city": "Poznań",
"countryCode": "PL"
},
"description": "string"
}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "09f0b4cc-7880-11e9-8f9e-2a86e4085a59",
"seller": {
"id": "string"
},
"name": "string",
"individual": {
"period": "P2Y"
},
"corporate": {
"period": "P2Y"
},
"address": {
"name": "Allegro.pl sp. z o.o.",
"street": "Grunwaldzka 182",
"postCode": "11-232",
"city": "Poznań",
"countryCode": "PL"
},
"description": "string"
}
Get the user's warranties
Use this resource to get the seller's warranties. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
limit	
integer <int32> [ 1 .. 60 ]
Default: 60
The limit of elements in the response.

offset	
integer <int32> [ 0 .. 59 ]
Default: 0
The offset of elements in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Unauthorized
403 Forbidden
404 Not Found

get
/after-sales-service-conditions/warranties
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"count": 0,
"warranties": [
{}
]
}
Create new user's warranty
Use this resource to create a warranty definition. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Warranty

name	
string <= 200 characters
Warranty name.

type	
string (WarrantyType)
Enum: "MANUFACTURER" "SELLER"
Defines who is warrantor.

individual	
object (WarrantyPeriod)
corporate	
object (WarrantyPeriod)
attachment	
object (WarrantyAttachment)
description	
string <= 10240 characters
Warranty description.

Responses
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
422 Unprocessable Entity

post
/after-sales-service-conditions/warranties
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"name": "Default",
"type": "MANUFACTURER",
"individual": {
"period": "P12M",
"lifetime": false
},
"corporate": {
"period": "P12M",
"lifetime": false
},
"attachment": {
"id": "54702c96-4ccd-4c0e-b4c7-382a71e810b5",
"name": "warranty.pdf"
},
"description": "string"
}
Response samples
201
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "09f0b4cc-7880-11e9-8f9e-2a86e4085a59",
"seller": {
"id": "string"
},
"name": "string",
"type": "MANUFACTURER",
"individual": {
"period": "P12M",
"lifetime": false
},
"corporate": {
"period": "P12M",
"lifetime": false
},
"attachment": {
"id": "54702c96-4ccd-4c0e-b4c7-382a71e810b5",
"name": "string",
"url": "string"
},
"description": "string"
}
Get the user's warranty
Use this resource to get a warranty details. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
warrantyId
required
string
The ID of the warranty.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Unauthorized
403 Forbidden
404 Not Found

get
/after-sales-service-conditions/warranties/{warrantyId}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "09f0b4cc-7880-11e9-8f9e-2a86e4085a59",
"seller": {
"id": "string"
},
"name": "string",
"type": "MANUFACTURER",
"individual": {
"period": "P12M",
"lifetime": false
},
"corporate": {
"period": "P12M",
"lifetime": false
},
"attachment": {
"id": "54702c96-4ccd-4c0e-b4c7-382a71e810b5",
"name": "string",
"url": "string"
},
"description": "string"
}
Change the user's warranty
Use this resource to modify the warranty details. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
warrantyId
required
string
The ID of the warranty.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Warranty

name	
string <= 200 characters
Warranty name.

type	
string (WarrantyType)
Enum: "MANUFACTURER" "SELLER"
Defines who is warrantor.

individual	
object (WarrantyPeriod)
corporate	
object (WarrantyPeriod)
attachment	
object (WarrantyAttachment)
description	
string <= 10240 characters
Warranty description.

Responses
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
422 Unprocessable Entity

put
/after-sales-service-conditions/warranties/{warrantyId}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"name": "Default",
"type": "MANUFACTURER",
"individual": {
"period": "P12M",
"lifetime": false
},
"corporate": {
"period": "P12M",
"lifetime": false
},
"attachment": {
"id": "54702c96-4ccd-4c0e-b4c7-382a71e810b5",
"name": "warranty.pdf"
},
"description": "string"
}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "09f0b4cc-7880-11e9-8f9e-2a86e4085a59",
"seller": {
"id": "string"
},
"name": "string",
"type": "MANUFACTURER",
"individual": {
"period": "P12M",
"lifetime": false
},
"corporate": {
"period": "P12M",
"lifetime": false
},
"attachment": {
"id": "54702c96-4ccd-4c0e-b4c7-382a71e810b5",
"name": "string",
"url": "string"
},
"description": "string"
}
Create a warranty attachment metadata
You can attach PDF files to warranties. Uploading attachments flow:

Create an attachment object to receive an upload URL (POST /after-sales-service-conditions/attachments),
Use the upload URL to submit the PDF file (PUT /after-sales-service-conditions/attachments/{attachmentId}),
Create (or update) warranty with attachment (POST /after-sales-service-conditions/warranties).
Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
After sale services attachment

name	
string
Responses
201 Attachment created successfully.
400 Syntactically incorrect request.
401 Invalid or missing bearer token.
403 Forbidden
415 Unsupported media type.
422 Unprocessable Entity.

post
/after-sales-service-conditions/attachments
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
{
"name": "uploaded_file.pdf"
}
Response samples
201
Content type
application/vnd.allegro.public.v1+json

Copy
{
"id": "54702c96-4ccd-4c0e-b4c7-382a71e810b5",
"name": "string",
"url": "string"
}
Upload an warranty attachment
Upload an after sale services attachment. This operation should be used after creating an offer attachment with POST /sale/offer-attachments Important! You can find the URL address to upload the file to our server in the Location response header of POST /after-sales-service-conditions/attachments. The URL is unique and one-time. As its format may change in time, you should always use the address from the header. Do not compose the address on your own. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
attachmentId
required
string
The ID of the attachment.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/pdf
string <binary>
File in a binary format

Responses
200 File uploaded correctly.
400 Syntactically incorrect request.
401 Invalid or missing bearer token.
403 Forbidden
404 Not found.
413 Payload too large.
422 Invalid file content.

put
/after-sales-service-conditions/attachments/{attachmentId}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
{
"id": "54702c96-4ccd-4c0e-b4c7-382a71e810b5",
"name": "string",
"url": "string"
}
Delivery
Get the user's shipping rates
Use this resource to get a list of seller's shipping rates. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
marketplace	
string
Example: marketplace=allegro-cz
Allows to filter shipping rates by marketplace that they are qualified for.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Authentication required
403 Unauthorized

get
/sale/shipping-rates
Response samples
200401403
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"shippingRates": [
{}
]
}
Create a new shipping rates set
Use this resource to create a new seller's shipping rates set. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Shipping rates set

id	
string
Shipping rates set ID (UUID) When creating a shipping rates set (Post) the field is ignored. It is required when updating (Put) a shipping rates.

name
required
string [ 1 .. 64 ] characters
User defined name of the shipping rates set. It may only contain: letters, numbers, hyphens, dots, commas and spaces.

type
required
string
Enum: "PHYSICAL" "ELECTRONIC"
Whether the shipping rates set is physical or electronic. Note that once a shipping rates set is created, it cannot be changed later.

dispatchCountry	
string or null <= 2 characters
The dispatch country code in ISO 3166-1 alfa-2 format. It must be passed if the PHYSICAL type is provided. Note that once a shipping rates set is created, it cannot be changed later.

rates
required
Array of objects (ShippingRate)
lastModified	
string
Date and time of the last modification of the set in UTC ISO 8601 format. When creating (Post) or updating (Put) a shipping rates set the field is ignored.

Responses
201 OK
400 Bad request
401 Authentication required
422 The user has reached the limit of shipping rates sets. Information on the limit will be returned in the error message.

post
/sale/shipping-rates
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "5c7bbf8b-b294-4737-bbda-894320c413b8",
"name": "Allegro Delivery shipping rate",
"type": "PHYSICAL",
"dispatchCountry": "PL",
"rates": [
{}
],
"lastModified": "2021-11-30T15:17:05.130Z"
}
Response samples
201400401422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "5c7bbf8b-b294-4737-bbda-894320c413b8",
"name": "Allegro Delivery shipping rate",
"type": "PHYSICAL",
"dispatchCountry": "PL",
"rates": [
{}
],
"lastModified": "2021-11-30T15:17:05.130Z"
}
Get the details of a shipping rates set
Use this resource to get details of the given shipping rates set. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string
Shipping rates set identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Authentication required
403 Unauthorized
404 Shipping rates set with given ID not found

get
/sale/shipping-rates/{id}
Response samples
200401403404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "758fcd59-fbfa-4453-ae07-4800d72c2ca6",
"name": "Mój cennik",
"type": "PHYSICAL",
"dispatchCountry": "PL",
"features": {
"managedByAllegro": false,
"isFulfillment": false
},
"rates": [
{}
],
"lastModified": "2026-04-05T12:20:23.974Z"
}
Edit a user's shipping rates set
Use this resource to edit a new seller's shipping rates set. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string
Shipping rates set identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Shipping rates set

id	
string
Shipping rates set ID (UUID) When creating a shipping rates set (Post) the field is ignored. It is required when updating (Put) a shipping rates.

name
required
string [ 1 .. 64 ] characters
User defined name of the shipping rates set. It may only contain: letters, numbers, hyphens, dots, commas and spaces.

type
required
string
Enum: "PHYSICAL" "ELECTRONIC"
Whether the shipping rates set is physical or electronic. Note that once a shipping rates set is created, it cannot be changed later.

dispatchCountry	
string or null <= 2 characters
The dispatch country code in ISO 3166-1 alfa-2 format. It must be passed if the PHYSICAL type is provided. Note that once a shipping rates set is created, it cannot be changed later.

rates
required
Array of objects (ShippingRate)
lastModified	
string
Date and time of the last modification of the set in UTC ISO 8601 format. When creating (Post) or updating (Put) a shipping rates set the field is ignored.

Responses
200 OK
400 Bad request
401 Authentication required
403 Unauthorized
404 Set with given id does not exist
422 Unprocessable Entity.

put
/sale/shipping-rates/{id}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "5c7bbf8b-b294-4737-bbda-894320c413b8",
"name": "Allegro Delivery shipping rate",
"type": "PHYSICAL",
"dispatchCountry": "PL",
"rates": [
{}
],
"lastModified": "2021-11-30T15:17:05.130Z"
}
Response samples
200400401403404422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "5c7bbf8b-b294-4737-bbda-894320c413b8",
"name": "Allegro Delivery shipping rate",
"type": "PHYSICAL",
"dispatchCountry": "PL",
"rates": [
{}
],
"lastModified": "2021-11-30T15:17:05.130Z"
}
Get the user's delivery settings
Use this resource to get the delivery settings declared by the seller. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
marketplace.id	
string
Example: marketplace.id=allegro-pl
Marketplace for which delivery settings will be returned. By default (if the marketplace parameter is not set) the marketplace on which the seller has registered is used. However, we recommend that the marketplace.id query parameter should always be explicitly set.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Authentication required.
403 Forbidden - not allowed to access user data.
422 Unprocessable Entity - not supported marketplace.

get
/sale/delivery-settings
Response samples
200401403422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"marketplace": {
"id": "allegro-pl"
},
"freeDelivery": {
"amount": "123.45",
"currency": "PLN"
},
"abroadFreeDelivery": {
"amount": "900.12",
"currency": "PLN"
},
"joinPolicy": {
"strategy": "MAX"
},
"updatedAt": "2025-08-24T14:15:22Z"
}
Modify the user's delivery settings
Use this resource to modify the delivery settings declared by the seller. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Delivery settings set

marketplace	
object
The marketplace for which delivery settings will be modified. By default (if the marketplace parameter is not set) the marketplace on which the seller has registered is used. However, we recommend that the marketplace parameter should always be explicitly set.

freeDelivery	
object
A minimum total order amount required to qualify for free domestic delivery (for example for allegro-cz marketplace, only Czechia is treated as domestic). If you do not want to set free domestic delivery threshold, do not set this value.

abroadFreeDelivery	
object
A minimum total order amount required to qualify for free foreign delivery (for example for allegro-cz marketplace, all delivery countries other than Czechia are treated as foreign). If you do not want to set free foreign delivery threshold, do not set this value.

joinPolicy
required
object
Policy of calculating delivery costs.

Responses
200 OK
401 Authentication required.
403 Forbidden - not allowed to access user data.
422 Unprocessable Entity - wrong amount, wrong currency, wrong join policy strategy, unsupported marketplace, attempt to modify marketplace allegro-business-* - modifying the settings for such a marketplace should be done by modifying the allegro-* marketplace.

put
/sale/delivery-settings
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"marketplace": {
"id": "allegro-pl"
},
"freeDelivery": {
"amount": "123.45",
"currency": "PLN"
},
"abroadFreeDelivery": {
"amount": "900.12",
"currency": "PLN"
},
"joinPolicy": {
"strategy": "SUM"
}
}
Response samples
200401403422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"marketplace": {
"id": "allegro-pl"
},
"freeDelivery": {
"amount": "123.45",
"currency": "PLN"
},
"abroadFreeDelivery": {
"amount": "900.12",
"currency": "PLN"
},
"joinPolicy": {
"strategy": "MAX"
},
"updatedAt": "2025-08-24T14:15:22Z"
}
Get the list of delivery methods
Use this resource to get a list of all delivery methods currently available on the platform, as well as those that have already been discontinued. Read more: PL / EN.

Authorizations:
bearer-token-for-applicationbearer-token-for-user
query Parameters
marketplace	
string
Example: marketplace=allegro-pl
Allows to filter delivery methods by marketplace id.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Authentication required.

get
/sale/delivery-methods
Response samples
200401
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"deliveryMethods": [
{}
]
}
Additional services
Create additional services group
Use this resource to create a group of additional services. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Additional service group body

name
required
string [ 1 .. 100 ] characters
Name of the group provided by merchant, invisible for buyers.

language
required
string = 5 characters
IETF language tag. Must be equal to main language for given marketplace: 'pl-PL' on allegro.pl and 'cs-CZ' on allegro.cz while creating new group.
Cannot change the language of already created group while modifying existing group.

additionalServices
required
Array of objects (AdditionalServiceRequest)
Responses
201 OK
401 Unauthorized
422 Unprocessable Entity

post
/sale/offer-additional-services/groups
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"name": "Gift wrap only",
"language": "pl-PL",
"additionalServices": [
{}
]
}
Response samples
201
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"additionalServices": [
{}
],
"createdAt": "2019-08-24T14:15:22Z",
"id": "string",
"updatedAt": "2019-08-24T14:15:22Z",
"name": "Gift wrap only",
"seller": {
"id": "53703086"
},
"language": "pl-PL",
"managedByAllegro": true
}
Get the user's additional services groups
Use this resource to retrieve a list of groups with additional services available to a given user which you may assign to offers. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
offset	
integer <int32> >= 0
Default: 0
Example: offset=200
The offset of elements in the response.

limit	
integer <int32> [ 1 .. 1000 ]
Default: 100
Example: limit=200
The limit of elements in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Unauthorized
403 Forbidden

get
/sale/offer-additional-services/groups
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"additionalServicesGroups": [
{}
]
}
Get the additional services definitions by categories
Use this resource to get additional services definitions, grouped by additional services categories, available on given marketplace. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Unauthorized
403 Forbidden

get
/sale/offer-additional-services/categories
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"categories": [
{}
]
}
Get the details of an additional services group
Use this resource to get additional services group for a given ID. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
groupId
required
string
Additional Service Group ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Unauthorized
404 Not Found

get
/sale/offer-additional-services/groups/{groupId}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"additionalServices": [
{}
],
"createdAt": "2019-08-24T14:15:22Z",
"id": "string",
"updatedAt": "2019-08-24T14:15:22Z",
"name": "Gift wrap only",
"seller": {
"id": "53703086"
},
"language": "pl-PL",
"managedByAllegro": true
}
Modify an additional services group
Use this resource to modify existing additional service group. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
groupId
required
string
Additional service group ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Additional service group body

name
required
string [ 1 .. 100 ] characters
Name of the group provided by merchant, invisible for buyers.

language
required
string = 5 characters
IETF language tag. Must be equal to main language for given marketplace: 'pl-PL' on allegro.pl and 'cs-CZ' on allegro.cz while creating new group.
Cannot change the language of already created group while modifying existing group.

additionalServices
required
Array of objects (AdditionalServiceRequest)
Responses
200 OK
401 Unauthorized
404 Not Found

put
/sale/offer-additional-services/groups/{groupId}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"name": "Gift wrap only",
"language": "pl-PL",
"additionalServices": [
{}
]
}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"additionalServices": [
{}
],
"createdAt": "2019-08-24T14:15:22Z",
"id": "string",
"updatedAt": "2019-08-24T14:15:22Z",
"name": "Gift wrap only",
"seller": {
"id": "53703086"
},
"language": "pl-PL",
"managedByAllegro": true
}
Additional services translations
Get translations for specified group
Use this resource to get translations for additional service group. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
groupId
required
string
Additional Service Group ID.

query Parameters
language	
string = 5 characters
Example: language=en-US
IETF language tag. When provided, the response will contain translations in only that language (if exists).

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Unauthorized
404 Not Found

get
/sale/offer-additional-services/groups/{groupId}/translations
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"translations": [
{}
]
}
Create/Update translations for specified group and language
Use this resource to create/update translation for additional service group and specified language. It is allowed to provide an incomplete list of services that belong to the group. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
groupId
required
string
Additional Service Group ID.

language
required
string = 5 characters
Example: pl-PL
IETF Language tag.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Additonal service group translation.

additionalServices	
object (AdditionalServicesGroupTranslationWrapper)
Responses
200 Translation created/updated for group and language.
401 Unauthorized
404 Not Found

patch
/sale/offer-additional-services/groups/{groupId}/translations/{language}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"additionalServices": {
"translation": []
}
}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"language": "pl-PL",
"additionalServices": {
"translation": [],
"type": "MANUAL"
}
}
Delete a translation for a specified group and language
Use this resource to delete the translation for specified additional service group and language. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
groupId
required
string
Additional service group ID.

language
required
string = 5 characters
Example: pl-PL
IETF Language tag.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
204 Translation deleted successfully
401 Unauthorized
403 Forbidden
404 Additional service group or translation not found

delete
/sale/offer-additional-services/groups/{groupId}/translations/{language}
Size tables
Get a size table
Use this resource to get selected size table. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
tableId
required
string
Table identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL"
Example: pl-PL
Expected language of messages.

Responses
200 Size table returned successfully
401 Unauthorized
403 Forbidden
404 Not Found

get
/sale/size-tables/{tableId}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"headers": [
{}
],
"id": "e02bc505-4311-11e8-b7fd-6c3be5b54a70",
"name": "Nike shoes size table",
"template": {
"id": "5637592a-0a24-4771-b527-d89b2767d821"
},
"values": [
{}
]
}
Update a size table
Use this resource to update selected size table. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
tableId
required
string
Table identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Size table details

name
required
string
size table name

headers
required
Array of objects (Header)
size table headers

values
required
Array of objects (Cells)
size table cells

Responses
200 Size table updated successfully
401 Unauthorized
403 Forbidden
404 Not Found

put
/sale/size-tables/{tableId}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"name": "Nike shoes size table",
"headers": [
{}
],
"values": [
{}
]
}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"headers": [
{}
],
"id": "e02bc505-4311-11e8-b7fd-6c3be5b54a70",
"name": "Nike shoes size table",
"template": {
"id": "5637592a-0a24-4771-b527-d89b2767d821"
},
"values": [
{}
]
}
Get the user's size tables
Use this resource to get all size tables assigned to a seller account. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL"
Example: pl-PL
Expected language of messages.

Responses
200 Size tables returned successfully
401 Unauthorized
403 Forbidden
404 Not Found

get
/sale/size-tables
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"tables": [
{}
]
}
Create a size table
Use this resource to create size table. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Size table details

name
required
string
size table name

template
required
object (JustId)
headers
required
Array of objects (Header)
size table headers

values
required
Array of objects (Cells)
size table cells

Responses
201 Size table created successfully
401 Unauthorized
403 Forbidden
404 Not Found

post
/sale/size-tables
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"name": "Nike shoes size table",
"template": {
"id": "5637592a-0a24-4771-b527-d89b2767d821"
},
"headers": [
{}
],
"values": [
{}
]
}
Response samples
201
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"headers": [
{}
],
"id": "e02bc505-4311-11e8-b7fd-6c3be5b54a70",
"name": "Nike shoes size table",
"template": {
"id": "5637592a-0a24-4771-b527-d89b2767d821"
},
"values": [
{}
]
}
Get the size tables templates
Use this resource to get all size tables templates. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL"
Example: pl-PL
Expected language of messages.

Responses
200 Size tables templates returned successfully
401 Unauthorized
403 Forbidden

get
/sale/size-tables-templates
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"templates": [
{}
]
}
Points of service
Create a point of service
Use this resource to create a point of service. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Point of service

id	
string
UUID. When creating a point of service (Post) the field is ignored. It is required when updating (Put) a point of service.

externalId	
string <= 80 characters
ID from external client system.

name
required
string <= 80 characters
seller	
object (Seller)
type
required
string
Indicates point type. The only valid value so far is PICKUP_POINT.

address
required
object (Address)
phoneNumber	
string <= 16 characters
email	
string <= 64 characters
locations	
Array of objects (PosLocation)
IDs for a location. When creating (Post) or updating (Put) a point of service the field is ignored.

openHours
required
Array of objects (OpenHour)
Possible empty list of opening hours.

serviceTime	
string
Delivery time / Time period for receipt. Date format ISO 8601 e.g. 'PT24H'

payments	
Array of objects (Payment)
An empty list of payment types is available.

confirmationType
required
string
Confirmation method: AWAIT_CONTACT - We will inform you about the time of receipt, CALL_US - Please make an appointment, CONTACT_NOT_REQUIRED - Contact is not required.

status
required
string
Point of service status: ACTIVE - active, TEMPORARILY_CLOSED - temporarily closed, CLOSED_DOWN - closed down, DELETED - deleted.

createdAt	
string
Creation date. Date format (ISO 8601) - yyyy-MM-dd'T'HH:mm:ss.SSSZ When creating (Post) or updating (Put) a point of service the field is ignored.

updatedAt	
string
Modification date. Date format (ISO 8601) - yyyy-MM-dd'T'HH:mm:ss.SSSZ When creating (Post) or updating (Put) a point of service the field is ignored.

Responses
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict - similar Point of Service already exists. Url of the existing POS is provided in the HTTP Location header field of the response.
422 Unprocessable Entity

post
/points-of-service
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "string",
"externalId": "string",
"name": "string",
"seller": {
"id": "string"
},
"type": "string",
"address": {
"street": "string",
"city": "string",
"zipCode": "string",
"state": "string",
"countryCode": "PL",
"coordinates": {}
},
"phoneNumber": "string",
"email": "string",
"locations": [
{}
],
"openHours": [
{}
],
"serviceTime": "string",
"payments": [
{}
],
"confirmationType": "string",
"status": "string",
"createdAt": "string",
"updatedAt": "string"
}
Response samples
201400404409422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "string",
"externalId": "string",
"name": "string",
"seller": {
"id": "string"
},
"type": "string",
"address": {
"street": "string",
"city": "string",
"zipCode": "string",
"state": "string",
"countryCode": "PL",
"coordinates": {}
},
"phoneNumber": "string",
"email": "string",
"locations": [
{}
],
"openHours": [
{}
],
"serviceTime": "string",
"payments": [
{}
],
"confirmationType": "string",
"status": "string",
"createdAt": "string",
"updatedAt": "string"
}
Get the user's points of service
Use this resource to get a list of points of service by seller ID. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
seller.id
required
string
Example: seller.id=29324
User identifier.

countryCode	
string
Example: countryCode=PL
Country code identifier in ISO format. In case of incorrect or unsupported country code, empty list is returned. If missing, list of all defined points is returned. If present, correct and supported, list of all points with given country code for the user is returned.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Unauthorized
404 Not Found

get
/points-of-service
Response samples
200404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"posList": [
{}
]
}
Get the details of a point of service
Use this resource to get a details of a point of service for a given ID. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string
Point of service ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Unauthorized
403 Forbidden
404 Not Found

get
/points-of-service/{id}
Response samples
200404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "string",
"externalId": "string",
"name": "string",
"seller": {
"id": "string"
},
"type": "string",
"address": {
"street": "string",
"city": "string",
"zipCode": "string",
"state": "string",
"countryCode": "PL",
"coordinates": {}
},
"phoneNumber": "string",
"email": "string",
"locations": [
{}
],
"openHours": [
{}
],
"serviceTime": "string",
"payments": [
{}
],
"confirmationType": "string",
"status": "string",
"createdAt": "string",
"updatedAt": "string"
}
Modify a point of service
Use this resource to modify a point of service. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string
Point of service ID. Must match values with 'id' property from the body.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Point of service

id	
string
UUID. When creating a point of service (Post) the field is ignored. It is required when updating (Put) a point of service.

externalId	
string <= 80 characters
ID from external client system.

name
required
string <= 80 characters
seller	
object (Seller)
type
required
string
Indicates point type. The only valid value so far is PICKUP_POINT.

address
required
object (Address)
phoneNumber	
string <= 16 characters
email	
string <= 64 characters
locations	
Array of objects (PosLocation)
IDs for a location. When creating (Post) or updating (Put) a point of service the field is ignored.

openHours
required
Array of objects (OpenHour)
Possible empty list of opening hours.

serviceTime	
string
Delivery time / Time period for receipt. Date format ISO 8601 e.g. 'PT24H'

payments	
Array of objects (Payment)
An empty list of payment types is available.

confirmationType
required
string
Confirmation method: AWAIT_CONTACT - We will inform you about the time of receipt, CALL_US - Please make an appointment, CONTACT_NOT_REQUIRED - Contact is not required.

status
required
string
Point of service status: ACTIVE - active, TEMPORARILY_CLOSED - temporarily closed, CLOSED_DOWN - closed down, DELETED - deleted.

createdAt	
string
Creation date. Date format (ISO 8601) - yyyy-MM-dd'T'HH:mm:ss.SSSZ When creating (Post) or updating (Put) a point of service the field is ignored.

updatedAt	
string
Modification date. Date format (ISO 8601) - yyyy-MM-dd'T'HH:mm:ss.SSSZ When creating (Post) or updating (Put) a point of service the field is ignored.

Responses
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict - similar Point of Service already exists. Url of the existing POS is provided in the HTTP Location header field of the response.
422 Unprocessable Entity

put
/points-of-service/{id}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "string",
"externalId": "string",
"name": "string",
"seller": {
"id": "string"
},
"type": "string",
"address": {
"street": "string",
"city": "string",
"zipCode": "string",
"state": "string",
"countryCode": "PL",
"coordinates": {}
},
"phoneNumber": "string",
"email": "string",
"locations": [
{}
],
"openHours": [
{}
],
"serviceTime": "string",
"payments": [
{}
],
"confirmationType": "string",
"status": "string",
"createdAt": "string",
"updatedAt": "string"
}
Response samples
200400404409422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "string",
"externalId": "string",
"name": "string",
"seller": {
"id": "string"
},
"type": "string",
"address": {
"street": "string",
"city": "string",
"zipCode": "string",
"state": "string",
"countryCode": "PL",
"coordinates": {}
},
"phoneNumber": "string",
"email": "string",
"locations": [
{}
],
"openHours": [
{}
],
"serviceTime": "string",
"payments": [
{}
],
"confirmationType": "string",
"status": "string",
"createdAt": "string",
"updatedAt": "string"
}
Delete a point of service
Use this resource to delete a point of service. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string
Point of service ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
204 No content
401 Unauthorized
403 Forbidden
404 Not Found

delete
/points-of-service/{id}
Response samples
404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"errors": [
{}
]
}
Contacts
Create a new contact
Use this resource to create a new contact. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
New contact

name	
string <= 250 characters
emails	
Array of objects (EmailRequest) <= 1 items
phones	
Array of objects (PhonesRequest) <= 2 items
Responses
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
422 Unprocessable Entity

post
/sale/offer-contacts
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"name": "Main contact",
"emails": [
{}
],
"phones": [
{}
]
}
Response samples
201
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "3b5ba33b-8536-420e-beea-88a3f00d8789",
"name": "Main contact",
"emails": [
{}
],
"phones": [
{}
]
}
Get the user's contacts
Use this resource to get details of many contacts. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL"
Example: pl-PL
Expected language of messages.

Responses
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden

get
/sale/offer-contacts
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"contacts": [
{}
]
}
Get contact details
Use this resource to get contact details. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string
Contact identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL"
Example: pl-PL
Expected language of messages.

Responses
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found

get
/sale/offer-contacts/{id}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "3b5ba33b-8536-420e-beea-88a3f00d8789",
"name": "Main contact",
"emails": [
{}
],
"phones": [
{}
]
}
Modify contact details
Use this resource to modify contact details. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string
Contact identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
Contact

name	
string <= 250 characters
emails	
Array of objects (EmailRequest) <= 1 items
phones	
Array of objects (PhonesRequest) <= 2 items
Responses
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
422 Unprocessable Entity

put
/sale/offer-contacts/{id}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"name": "Main contact",
"emails": [
{}
],
"phones": [
{}
]
}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "3b5ba33b-8536-420e-beea-88a3f00d8789",
"name": "Main contact",
"emails": [
{}
],
"phones": [
{}
]
}
Responsible persons
Get the list of responsible persons
Use this resource to get a list of responsible persons for the compliance of the product with EU regulations. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
offset	
integer [ 0 .. 16000 ]
Default: 0
Index of first returned responsible persons data from all search results.

limit	
integer [ 1 .. 1000 ]
Default: 1000
Number of returned responsible persons data.

header Parameters
Accept
required
string
Example: application/vnd.allegro.public.v1+json
Acceptable representation of the response.

Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
422 Unprocessable Entity

get
/sale/responsible-persons
Response samples
200400401403422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"responsiblePersons": [
{}
],
"count": 1,
"totalCount": 1
}
Create responsible person
Use this resource to create a new responsible person for the compliance of the product with EU regulations. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept
required
string
Example: application/vnd.allegro.public.v1+json
Acceptable representation of the response.

Content-Type
required
string
Example: application/vnd.allegro.public.v1+json
Content type of the request body.

Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
name	
string <= 50 characters
Internal name of responsible person in dictionary (visible only to you). Can't start or end with whitespace. Can't contain whitespaces other than space. Can't contain multiple spaces in a row.

personalData	
object
Responsible person personal data.

Responses
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
422 Unprocessable Entity

post
/sale/responsible-persons
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"name": "Person responsible for batteries",
"personalData": {
"name": "Responsible person company name",
"address": {},
"contact": {}
}
}
Response samples
200400401403422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "fee43309-8761-43f9-9cfd-a43e539a0fc5",
"name": "Person responsible for batteries",
"personalData": {
"name": "Responsible person company name",
"address": {},
"contact": {}
}
}
Update responsible person
Use this resource to update the responsible person for the compliance of the product with EU regulations. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string <uuid>
Responsible person ID.

header Parameters
Accept
required
string
Example: application/vnd.allegro.public.v1+json
Acceptable representation of the response.

Content-Type
required
string
Example: application/vnd.allegro.public.v1+json
Content type of the request body.

Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
id	
string <uuid>
Responsible person ID.

name	
string <= 50 characters
Internal name of responsible person in dictionary (visible only to you). Can't start or end with whitespace. Can't contain whitespaces other than space. Can't contain multiple spaces in a row.

personalData	
object
Responsible person personal data.

Responses
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
422 Unprocessable Entity

put
/sale/responsible-persons/{id}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "fee43309-8761-43f9-9cfd-a43e539a0fc5",
"name": "Person responsible for batteries",
"personalData": {
"name": "Responsible person company name",
"address": {},
"contact": {}
}
}
Response samples
200400401403422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "fee43309-8761-43f9-9cfd-a43e539a0fc5",
"name": "Person responsible for batteries",
"personalData": {
"name": "Responsible person company name",
"address": {},
"contact": {}
}
}
Responsible producers
Get the list of responsible producers
Use this resource to get a list of responsible producers for the compliance of the product with EU regulations. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
offset	
integer [ 0 .. 50000 ]
Default: 0
Index of first returned responsible producers data from all search results.

limit	
integer [ 1 .. 1000 ]
Default: 1000
Number of returned responsible producers data.

header Parameters
Accept
required
string
Example: application/vnd.allegro.public.v1+json
Acceptable representation of the response.

Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
422 Unprocessable Entity

get
/sale/responsible-producers
Response samples
200400401403422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"responsibleProducers": [
{}
],
"count": 1,
"totalCount": 1
}
Create responsible producer
Use this resource to create a new responsible producer for the compliance of the product with EU regulations. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept
required
string
Example: application/vnd.allegro.public.v1+json
Acceptable representation of the response.

Content-Type
required
string
Example: application/vnd.allegro.public.v1+json
Content type of the request body.

Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
name	
string <= 50 characters
Internal name of responsible producer in dictionary (visible only to you). Can't start or end with whitespace. Can't contain whitespaces other than space. Can't contain multiple spaces in a row.

producerData	
object
Responsible producer data.

Responses
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
422 Unprocessable Entity

post
/sale/responsible-producers
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"name": "Company responsible for producing product.",
"producerData": {
"tradeName": "Trade name of responsible producer",
"address": {},
"contact": {}
}
}
Response samples
201400401403422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "fee43309-8761-43f9-9cfd-a43e539a0fc5",
"name": "Company responsible for producing product.",
"producerData": {
"tradeName": "Trade name of responsible producer",
"address": {},
"contact": {}
}
}
Get responsible producer
Use this resource to get a responsible producer for the compliance of the product with EU regulations. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string <uuid>
Responsible producer ID.

header Parameters
Accept
required
string
Example: application/vnd.allegro.public.v1+json
Acceptable representation of the response.

Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Unauthorized
403 Forbidden
404 Not Found
422 Unprocessable Entity

get
/sale/responsible-producers/{id}
Response samples
200401403404422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "fee43309-8761-43f9-9cfd-a43e539a0fc5",
"name": "Company responsible for producing product.",
"producerData": {
"tradeName": "Trade name of responsible producer",
"address": {},
"contact": {}
}
}
Update responsible producer
Use this resource to update the responsible producer for the compliance of the product with EU regulations. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string <uuid>
Responsible producer ID.

header Parameters
Accept
required
string
Example: application/vnd.allegro.public.v1+json
Acceptable representation of the response.

Content-Type
required
string
Example: application/vnd.allegro.public.v1+json
Content type of the request body.

Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
id	
string <uuid>
Responsible producer ID.

name	
string <= 50 characters
Internal name of responsible producer in dictionary (visible only to you). Can't start or end with whitespace. Can't contain whitespaces other than space. Can't contain multiple spaces in a row.

producerData	
object
Responsible producer data.

Responses
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
422 Unprocessable Entity

put
/sale/responsible-producers/{id}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "fee43309-8761-43f9-9cfd-a43e539a0fc5",
"name": "Company responsible for producing product.",
"producerData": {
"tradeName": "Trade name of responsible producer",
"address": {},
"contact": {}
}
}
Response samples
200400401403422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "fee43309-8761-43f9-9cfd-a43e539a0fc5",
"name": "Company responsible for producing product.",
"producerData": {
"tradeName": "Trade name of responsible producer",
"address": {},
"contact": {}
}
}
Advance Ship Notices
Get list of Advance Ship Notices
Use this resource to get a list of Advance Ship Notices. The list is ordered by createdAt property. Default offset is 0, default limit is 50. A list can be filtered by statuses. Multiple status query parameters are allowed. In such cases, filters are joined with OR logical operator. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
offset	
integer >= 0
Default: 0
The offset of elements in the response.

limit	
integer [ 1 .. 200 ]
Default: 50
Maximum number of elements in response.

status	
Array of strings (AdvanceShipNoticeStatus)
Items Enum: "DRAFT" "IN_TRANSIT" "UNPACKING" "COMPLETED" "CANCELLED"
Example: status=DRAFT
A status of the Advance Ship Notices in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Returns list of Advance Ship Notices that belong to a seller.
401 Unauthorized
403 Forbidden
422 Invalid request parameters.

get
/fulfillment/advance-ship-notices
Response samples
200422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"advanceShipNotices": [
{}
],
"count": 1,
"totalCount": 1
}
Create an Advance Ship Notice
Use this resource to create an Advance Ship Notice. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
items
required
Array of objects (ProductItem)
A list of product items.

handlingUnit	
object (HandlingUnit)
Represents information about handling unit.

shipping	
object (Shipping)
Represents information about package shipment. Constraints:

for method OWN_TRANSPORT: truckLicencePlate, estimatedTimeOfArrival and countryCode are required.
for method COURIER_BY_SELLER: courier, estimatedTimeOfArrival and countryCode are required.
for method THIRD_PARTY_DELIVERY: thirdParty, estimatedTimeOfArrival and countryCode are required.
declaredVolumeInCc	
number (DeclaredAsnVolume)
Total volume of all items declared by the merchant for delivery to the warehouse as part of the advance shipment notice, in cubic centimeters.

Responses
201 Advance Ship Notice created.
400 Invalid request body.
401 Unauthorized
403 Forbidden
422 Advance Ship Notice cannot be created due to improper input data.

post
/fulfillment/advance-ship-notices
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"items": [
{}
],
"handlingUnit": {
"unitType": "BOX",
"amount": 1,
"labelsType": "ONE_FULFILMENT"
},
"shipping": {
"method": "COURIER_BY_SELLER"
},
"declaredVolumeInCc": 1500
}
Response samples
201400422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "71529ad2-2265-4e15-b76b-c17025d848f7",
"displayNumber": "A-210310-0000002",
"status": "DRAFT",
"createdAt": "2020-08-26T12:50:04Z",
"updatedAt": "2020-08-26T12:50:04Z",
"items": [
{}
],
"handlingUnit": {
"unitType": "BOX",
"amount": 1,
"labelsType": "ONE_FULFILMENT"
},
"labels": {
"fileUrl": "https://api.allegro.pl/fulfillment/678453232"
},
"shipping": {
"method": "COURIER_BY_SELLER"
},
"volumeInCc": 1500
}
Get single Advance Ship Notice
Use this resource to get an Advance Ship Notice. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string <uuid>
Example: 84529ad2-2265-4e15-b76b-c17025d848f6
The identifier of returned Advance Ship Notice.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Returns single Advance Ship Notice.
401 Unauthorized
403 Forbidden
404 Not Found

get
/fulfillment/advance-ship-notices/{id}
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "71529ad2-2265-4e15-b76b-c17025d848f7",
"displayNumber": "A-210310-0000002",
"status": "DRAFT",
"createdAt": "2020-08-26T12:50:04Z",
"updatedAt": "2020-08-26T12:52:04Z",
"items": [
{}
],
"handlingUnit": {
"unitType": "BOX",
"amount": 1,
"labelsType": "ONE_FULFILMENT"
},
"labels": {
"fileUrl": "https://api.allegro.pl/fulfillment/678453232"
},
"shipping": {
"method": "COURIER_BY_SELLER"
},
"submittedAt": "2020-08-26T12:52:04Z",
"volumeInCc": 1500
}
Update Advance Ship Notice
Use this resource to update an Advance Ship Notice. Any content property update will clear labels property. Use Create labels command to create new labels for provided content. If a client wants to update read-only property, an error is returned (only in cases when sent value will be different than actual on the server). Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string <uuid>
Example: 84529ad2-2265-4e15-b76b-c17025d848f6
An identifier of Advance Ship Notice.

header Parameters
if-match
required
string
Example: 123456
A current version of Advance Ship Notice (e.g. from etag header obtained via get).

Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
items
required
Array of objects (ProductItem)
A list of product items.

handlingUnit	
object (HandlingUnit)
Represents information about handling unit.

shipping	
object (Shipping)
Represents information about package shipment. Constraints:

for method OWN_TRANSPORT: truckLicencePlate, estimatedTimeOfArrival and countryCode are required.
for method COURIER_BY_SELLER: courier, estimatedTimeOfArrival and countryCode are required.
for method THIRD_PARTY_DELIVERY: thirdParty, estimatedTimeOfArrival and countryCode are required.
declaredVolumeInCc	
number (DeclaredAsnVolume)
Total volume of all items declared by the merchant for delivery to the warehouse as part of the advance shipment notice, in cubic centimeters.

Responses
200 Advance Ship Notice updated
400 If-match header missing
401 Unauthorized
403 Forbidden
412 Concurrent modification of ASN
422 ASN is invalid or attempting to update read-only property

put
/fulfillment/advance-ship-notices/{id}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"items": [
{}
],
"handlingUnit": {
"unitType": "BOX",
"amount": 1,
"labelsType": "ONE_FULFILMENT"
},
"shipping": {
"method": "COURIER_BY_SELLER"
},
"declaredVolumeInCc": 1500
}
Response samples
200422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "71529ad2-2265-4e15-b76b-c17025d848f7",
"displayNumber": "A-210310-0000002",
"status": "DRAFT",
"createdAt": "2020-08-26T12:50:04Z",
"updatedAt": "2020-08-26T12:52:04Z",
"items": [
{}
],
"handlingUnit": {
"unitType": "BOX",
"amount": 1,
"labelsType": "ONE_FULFILMENT"
},
"labels": {
"fileUrl": "https://api.allegro.pl/fulfillment/678453232"
},
"shipping": {
"method": "COURIER_BY_SELLER"
},
"submittedAt": "2020-08-26T12:52:04Z",
"volumeInCc": 1500
}
Delete Advance Ship Notice
Use this resource to delete an Advance Ship Notice. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string <uuid>
Default: "0b488a23-bc99-470d-8842-0c585adf2479"
An identifier of the Advance Ship Notice to delete.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
204 Advance Ship Notice was deleted.
401 Unauthorized
403 Forbidden
404 Not Found
422 ASN cannot be deleted - it is not in DRAFT status.

delete
/fulfillment/advance-ship-notices/{id}
Cancel Advance Ship Notice
Use this resource to cancel an Advance Ship Notice in IN_TRANSIT status. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string <uuid>
Default: "0b488a23-bc99-470d-8842-0c585adf2479"
An identifier of the Advance Ship Notice to cancel.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Advance Ship Notice was cancelled.
401 Unauthorized
403 Forbidden
404 Not Found
422 ASN cannot be cancelled - it is not in IN_TRANSIT status.

put
/fulfillment/advance-ship-notices/{id}/cancel
Get labels for Advance Ship Notice
Use this resource to get labels for Advance Ship Notice after being created with "create labels command". Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string <uuid>
Example: 84529ad2-2265-4e15-b76b-c17025d848f6
An identifier of the Advance Ship Notice.

header Parameters
accept
required
string
Enum: "application/pdf" "x-application/zpl"
Content-type of generated labels.

Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Returns PDF or ZPL file with labels.
401 Unauthorized
403 Forbidden
404 Not Found

get
/fulfillment/advance-ship-notices/{id}/labels
Submit the Advance Ship Notice
Use this resource to submit the Advance Ship Notice. After this operation, updates of the Advance Ship Notice are limited to selected properties only. See PUT /fulfillment/advance-ship-notices/{id}/submitted. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
command-id
required
string <uuid>
Default: "725432a9-ae9e-43de-b8c5-7430606a81a4"
The identifier of the command.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
id	
string <uuid>
The identifier of command.

input
required
object (SubmitCommandInput)
Represents input of the Advance Ship Notice submit command.

output	
object (SubmitCommandOutput)
Represents output of the Advance Ship Notice submit command.

Responses
201 Returns command output with status and possible errors. The command could fail with following error codes:
ASN_NOT_FOUND - Cannot find ASN with id given in command input.
COMMAND_FORBIDDEN - Requester has no access to run commands on given ASN.
INVALID_ASN_STATE - Such command cannot be run on current ASN state e.g. ASN has no shipping information.
COMMAND_FAILED - Any other error.
401 Unauthorized
422 Invalid request parameters.

put
/fulfillment/submit-commands/{command-id}
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "71529ad2-2265-4e15-b76b-c17025d848f7",
"input": {
"advanceShipNoticeId": "123a08d7-ab9b-460d-b9cb-d6ed64b3a018"
},
"output": {
"status": "RUNNING"
}
}
Response samples
201422
Content type
application/vnd.allegro.public.v1+json
Example

running command
running command

Copy
Expand allCollapse all
{
"id": "71529ad2-2265-4e15-b76b-c17025d848f7",
"input": {
"advanceShipNoticeId": "123a08d7-ab9b-460d-b9cb-d6ed64b3a018"
},
"output": {
"status": "RUNNING"
}
}
Get submit status
Use this resource to get submit status of the Advance Ship Notice. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
command-id
required
string <uuid>
Default: "882202c8-15ab-4a83-aeef-29ea505bf0d0"
An identifier of the command.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Returns command output with status and possible errors.
401 Unauthorized
403 Forbidden
422 Invalid request parameters.

get
/fulfillment/submit-commands/{command-id}
Response samples
200422
Content type
application/vnd.allegro.public.v1+json
Example

running command
running command

Copy
Expand allCollapse all
{
"id": "71529ad2-2265-4e15-b76b-c17025d848f7",
"input": {
"advanceShipNoticeId": "123a08d7-ab9b-460d-b9cb-d6ed64b3a018"
},
"output": {
"status": "RUNNING"
}
}
Update submitted Advance Ship Notice
Use this resource to update already submitted Advance Ship Notice. Update is allowed only when Advance Ship Notice is in "IN_TRANSIT" status. Handling unit's amount property update clears labels property. Use Create labels command to create new labels for provided content. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string <uuid>
Example: 84529ad2-2265-4e15-b76b-c17025d848f6
An identifier of Advance Ship Notice.

header Parameters
if-match
required
string
Example: 123456
A current version of Advance Ship Notice (e.g. from etag header obtained via get).

Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
items	
Array of objects (ProductItem)
A list of product items.

handlingUnit	
object (HandlingUnit)
Represents information about handling unit.

shipping	
object (Shipping)
Represents information about package shipment. Constraints:

for method OWN_TRANSPORT: truckLicencePlate, estimatedTimeOfArrival and countryCode are required.
for method COURIER_BY_SELLER: courier, estimatedTimeOfArrival and countryCode are required.
for method THIRD_PARTY_DELIVERY: thirdParty, estimatedTimeOfArrival and countryCode are required.
declaredVolumeInCc	
number (DeclaredAsnVolume)
Total volume of all items declared by the merchant for delivery to the warehouse as part of the advance shipment notice, in cubic centimeters.

Responses
200 Advance Ship Notice updated
400 If-match header missing
401 Unauthorized
403 Forbidden
412 Concurrent modification of ASN
422 Validation error

put
/fulfillment/advance-ship-notices/{id}/submitted
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"items": [
{}
],
"handlingUnit": {
"unitType": "BOX",
"amount": 1,
"labelsType": "ONE_FULFILMENT"
},
"shipping": {
"method": "COURIER_BY_SELLER"
},
"declaredVolumeInCc": 1500
}
Response samples
200422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "71529ad2-2265-4e15-b76b-c17025d848f7",
"displayNumber": "A-210310-0000002",
"status": "DRAFT",
"createdAt": "2020-08-26T12:50:04Z",
"updatedAt": "2020-08-26T12:52:04Z",
"items": [
{}
],
"handlingUnit": {
"unitType": "BOX",
"amount": 1,
"labelsType": "ONE_FULFILMENT"
},
"labels": {
"fileUrl": "https://api.allegro.pl/fulfillment/678453232"
},
"shipping": {
"method": "COURIER_BY_SELLER"
},
"submittedAt": "2020-08-26T12:52:04Z",
"volumeInCc": 1500
}
Check current state and details of Advance Ship Notice receiving
Use this resource to check the state of Advance Ship Notice receiving in Fulfillment Center in real time. The response contains a receiving progress and information about particular items - their quantities and conditions. While the Advance Ship Notice is in UNPACKING state, report is updated dynamically, which might result in different responses even at short time intervals. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
id
required
string <uuid>
Default: "712fa46c-7d4a-4ba0-b094-b5d1d4f6155d"
An identifier of advance ship notice.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Returns the state of Advance Ship Notice receiving in Fulfillment Center
401 Unauthorized
403 Forbidden
404 Not Found (ASN doesn't exist or is in state DRAFT or IN_TRANSIT)

get
/fulfillment/advance-ship-notices/{id}/receiving-state
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"updatedAt": "2020-08-26T12:50:04Z",
"stage": "COMPLETED",
"displayNumber": "A-210310-0000002",
"content": [
{}
]
}
Fulfillment Stock
Get available stock
Use this resource to get a list of the products belonging to the seller, which are in Allegro Warehouse. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
offset	
integer >= 0
Default: 0
The offset of elements in the response. Ignored for text/csv content type.

limit	
integer [ 1 .. 1000 ]
Default: 50
Maximum number of elements in response. Ignored for text/csv content type.

phrase	
string >= 3 characters
Filtering search results by product name.

sort	
string
Default: "name"
Enum: "available" "-available" "unfulfillable" "-unfulfillable" "name" "-name" "lastFourteenDaysSalesAverage" "-lastFourteenDaysSalesAverage" "reserve" "-reserve" "lastThirtyDaysSalesSum" "-lastThirtyDaysSalesSum" "storageFee" "-storageFee"
Defines how elements are sorted in response. Minus sign can be added to imply descending sort order. Ignored for text/csv content type. Possible values for the "sort" parameter:

-available - sorting by quantity of available products (descending)
available - sorting by quantity of available products (ascending)
-unfulfillable - sorting by quantity of unfulfillable products (descending)
unfulfillable - sorting by quantity of unfulfillable products (ascending)
-name - sorting by product’s name (descending)
name - sorting by product’s name (ascending)
lastFourteenDaysSalesAverage - sorting by product last fourteen days average sales (ascending)
-lastFourteenDaysSalesAverage - sorting by product last fourteen days average sales (descending)
reserve - sorting by reserve.outOfStockIn field (ascending)
-reserve - sorting by reserve.outOfStockIn field (descending)
lastThirtyDaysSalesSum - sorting by product last month sum sales (ascending)
-lastThirtyDaysSalesSum - sorting by product last month sum sales (descending)
storageFee - sorting by storage fee (ascending). The order by fee status is: NOT_APPLICABLE, then CHARGED ordered by amountGross ascending.
-storageFee - sorting by storage fee (descending). The order by fee status is: CHARGED ordered by amountGross descending, then NOT_APPLICABLE.
productId	
string <uuid>
Filtering search results by fulfillment product identifier. Ignored for text/csv content type.

productAvailability	
Array of strings
Items Enum: "SUFFICIENT" "UNAVAILABLE" "LOW"
Filtering search results by availability.

productStatus	
string
Value: "UNFULFILLABLE"
Filtering search results by status.

asnStatus	
string
Enum: "SUBMITTED" "NOT_FOUND"
Filtering search results by ASN status. Following values are allowed: SUBMITTED - Advanced Ship Notice document has been submitted and it contains a particular product. Only the products that have ASN with products on it are returned. NOT_FOUND - Advanced Ship Notice that contains a particular product was not found. It has not been submitted, may be expired, or products have already been delivered to the warehouse. Only the products that don't have related ASN with products on it are returned.

outOfStockInFrom	
integer
Filter by products with outOfStockIn greater than or equal.

outOfStockInTo	
integer
Filter by products with outOfStockIn less than or equal.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Returns available stock for the seller.
401 Unauthorized
403 Forbidden
422 Invalid request parameters.

get
/fulfillment/stock
Response samples
200422
Content type

application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"stock": [
{}
],
"count": 1,
"totalCount": 10
}
Fulfillment Parcels
Get list of shipped parcels
Use this resource to get list of parcels and included items for a given order. Items include detailed information such as expiration dates and serial numbers. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
orderId
required
string <uuid>
The Allegro's platform order identifier.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Returns list of parcels shipped by warehouse in a given order.
401 User not authenticated or token is expired
404 Not Found

get
/fulfillment/orders/{orderId}/parcels
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"orderId": "dd4bbba0-d692-11ec-9eac-2d3687b9fed8",
"parcels": [
{}
]
}
Fulfillment Products
Get list of available products
Use this resource to get a list of products that can be added to Advance Ship Notice. The list contains products for which the seller has created offers and is ordered by product's name. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
offset	
integer >= 0
Default: 0
The offset of elements in the response.

limit	
integer [ 1 .. 100 ]
Default: 50
Maximum number of elements in response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Returns list of products that can be added to Advance Ship Notice.
401 Unauthorized
403 Forbidden
422 Invalid request parameters.

get
/fulfillment/available-products
Response samples
200422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"products": [
{}
],
"count": 1,
"totalCount": 1
}
Fulfillment Returns
Get refund dispositions report
Use this resource to get refund dispositions for returns handled in One Fulfillment. The response contains data from the last 90 days only. The response contains both buyer returns and operational returns. When there is no matching disposition, the report array is empty. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
createdAt.gte	
string <date-time>
Example: createdAt.gte=2025-11-01T00:00:00.000Z
Date of the return in ISO 8601 format to search by greater or equal.

createdAt.lte	
string <date-time>
Example: createdAt.lte=2025-11-10T23:59:59.000Z
Date of the return in ISO 8601 format to search by lower or equal.

limit	
integer [ 1 .. 1000 ]
Default: 100
Maximum number of elements in response.

offset	
integer [ 0 .. 1000 ]
Default: 0
The offset of elements in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Returns the refund dispositions report.
401 Unauthorized
403 Forbidden
406 Not Acceptable
422 Invalid request parameters.

get
/fulfillment/returns/refund-dispositions
Response samples
200406422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"report": [
{}
]
}
Fulfillment Removal
Get current active removal preference
Use this resource to read your current removal preference. Removal preference is associated with system removal order at the moment of removal order is created. It means there can be not yet fulfilled removal orders associated with previously set removal preference. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Returns the current active Fulfillment Removal Preference
401 Unauthorized
403 Forbidden
404 Not Found (Fulfillment Removal Preferences was never set)

get
/fulfillment/removal/preferences
Response samples
200401
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"operation": "WITHDRAWAL",
"address": {
"company": "Company Warehouse Ltd",
"street": "Uliczna 7",
"postalCode": "60-166",
"city": "Poznań",
"countryCode": "PL",
"phone": {},
"additionalInfo": "Left doors in the warehouse."
}
}
Create new active Fulfillment Removal Preference
Use this resource to create new active removal preference. From the moment the preference is set, it becomes the active one, and all new system removal orders will be associated with this preference. Removal preference is associated with system removal order at the moment of removal order is created. It means there can be not yet fulfilled removal orders associated with previously set removal preference. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
operation
required
string
Enum: "WITHDRAWAL" "DISPOSAL"
Preference what kind of operation to execute on undesirable items WITHDRAWAL/DISPOSAL (required).

address	
object (FulfillmentWithdrawalAddress)
Represents information about address passed for withdrawal purpose.

Responses
201 Active Fulfillment Removal Preference created.
401 Unauthorized
403 Forbidden
422 Fulfillment Removal Preferences cannot be created due to invalid request body.

put
/fulfillment/removal/preferences
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"operation": "WITHDRAWAL",
"address": {
"company": "Company Warehouse Ltd",
"street": "Uliczna 7",
"postalCode": "60-166",
"city": "Poznań",
"countryCode": "PL",
"phone": {},
"additionalInfo": "Left doors in the warehouse."
}
}
Response samples
201401422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"operation": "WITHDRAWAL",
"address": {
"company": "Company Warehouse Ltd",
"street": "Uliczna 7",
"postalCode": "60-166",
"city": "Poznań",
"countryCode": "PL",
"phone": {},
"additionalInfo": "Left doors in the warehouse."
}
}
Fulfillment Warehouse
Get seller warehouse
Use this resource to get the warehouse assigned to the seller.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Returns the warehouse assigned to the seller.
401 Unauthorized
403 Forbidden
404 Warehouse assignment not found.

get
/fulfillment/warehouse
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "ADM-01",
"name": "Magazyn Allegro",
"location": {
"street": "Adamów 50",
"city": "Adamów",
"countryCode": "PL",
"postCode": "05-825",
"province": "MAZOWIECKIE"
}
}
Tax Identification Number
Add tax identification number
Use this resource to add tax identification number. For international sellers only. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
taxId	
string
User's tax identification number.

Responses
201 Tax identification number successfully added
401 Unauthorized
403 Forbidden
404 Not Found
422 Tax identification number is invalid

post
/fulfillment/tax-id
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
{
"taxId": "5252674798"
}
Response samples
422
Content type
application/json

Copy
Expand allCollapse all
{
"errors": [
{}
]
}
Update tax identification number
Use this resource to update tax identification number. For international sellers only. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
taxId	
string
User's tax identification number.

Responses
200 Tax identification number updated
401 Unauthorized
403 Forbidden
404 Not Found
422 Tax identification number is invalid

put
/fulfillment/tax-id
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
{
"taxId": "5252674798"
}
Response samples
422
Content type
application/json

Copy
Expand allCollapse all
{
"errors": [
{}
]
}
Get tax identification number
Use this resource to get tax identification number with verification status. After adding or updating the tax identification number the status will be NOT_VERIFIED and you will have to wait for acceptance status to start selling. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Returns tax identification number with verification status information
401 Unauthorized
403 Forbidden
404 Not Found

get
/fulfillment/tax-id
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
{
"taxId": "5252674798",
"verificationStatus": "ACCEPTED"
}
Conversions
[BETA] List CPS conversions
Use this resource to find your CPS (Cost Per Sale) conversions for specific filters. The response contains a list of CPS conversions that correspond with the specified parameters. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
orderCreatedAt.gte	
string
The minimum date and time of order creation in ISO 8601 format.

orderCreatedAt.lte	
string
The maximum date and time of order creation in ISO 8601 format.

lastModifiedAt.gte	
string
The minimum date and time of the latest conversion modification in ISO 8601 format.

lastModifiedAt.lte	
string
The maximum date and time of the latest conversion modification in ISO 8601 format.

status	
string
Conversion status. The allowed values are:

CREATED
REJECTED
CONFIRMED.
offset	
integer >= 0
Default: 0
The offset of elements in the response.

limit	
integer [ 1 .. 10000 ]
Default: 1000
Maximum number of elements in response.

includePublisherUrlParameters	
object
Comma-separated keys of the ‘publisherUrlParameters’ map which will be included in the response. By default the map is empty.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "en-US"
Example: en-US
Expected language of messages.

Responses
200 Returns the list of CPS conversions associated with a logged-in user and matched with query parameters.
400 Bad Request
401 Unauthorized
403 Forbidden
422 Invalid request parameters.

get
/affiliate/conversions/cps
Response samples
200422
Content type
application/vnd.allegro.beta.v1+json

Copy
Expand allCollapse all
{
"conversions": [
{}
]
}
Information about user
Get the user's ratings
Use this resource to receive your sales ratings sorted by last change date, starting from the latest. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
recommended	
string
Enum: "true" "false"
Example: recommended=true
Filter by recommended.

lastChangedAt.gte	
string <date-time>
Example: lastChangedAt.gte=2020-11-13T12:45:20.818Z
Last change (creation or latest edition) date time in ISO 8601 format. The lower bound of date time range from which ratings will be fetched.

lastChangedAt.lte	
string <date-time>
Example: lastChangedAt.lte=2020-11-13T12:45:20.818Z
Last change (creation or latest edition) date time in ISO 8601 format. The upper bound of date time range from which ratings will be fetched.

offset	
integer <int32> [ 0 .. 20000 ]
Default: 0
Example: offset=101
The offset of elements in the response.

limit	
integer <int32> [ 1 .. 100 ]
Default: 20
Example: limit=100
The limit of elements in the response.

header Parameters
Accept-Language	
string <BCP-47 language code>
Default: pl-PL
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages. The header is available only for content version 'application/vnd.allegro.beta.v1+json'.

Responses
200 OK
401 Unauthorized
403 Forbidden
404 Not Found

get
/sale/user-ratings
Response samples
200
Content type

application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"ratings": [
{}
]
}
Get the user's rating by given rating id
Use this resource to receive your sales rating by given rating id. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
ratingId
required
string
Example: 5df0a6d1ef437e00255572a1
The ID of the rating.

header Parameters
Accept-Language	
string <BCP-47 language code>
Default: pl-PL
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages. The header is available only for content version 'application/vnd.allegro.beta.v1+json'.

Responses
200 OK
401 Unauthorized
403 Forbidden
404 Not Found

get
/sale/user-ratings/{ratingId}
Response samples
200
Content type

application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"answer": {
"createdAt": "2017-05-17T08:36:57.292Z",
"message": "That is not our fault"
},
"buyer": {
"id": "string",
"login": "string"
},
"comment": "string",
"createdAt": "2017-05-17T08:36:57.292Z",
"editedAt": "2017-05-19T08:36:57.292Z",
"excludedFromAverageRates": false,
"excludedFromAverageRatesReason": "Rating not unique",
"id": "string",
"lastChangedAt": "2017-05-19T08:36:57.292Z",
"order": {
"id": "5354bed4-92b7-4fbb-9810-03a8f7834d15",
"offers": []
},
"rates": {
"delivery": 5,
"deliveryCost": 5,
"description": 5,
"service": 5
},
"recommended": false,
"removal": {
"possibleTo": "2017-05-17T08:36:57.292Z",
"request": {}
}
}
Answer for user's rating
Use this resource to answer for received rating. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
ratingId
required
string
Example: 5df0a6d1ef437e00255572a1
ID of the rating.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
User rating answer request.

message
required
string <= 500 characters
Answer message.

Responses
201 OK
400 Bad request
401 Unauthorized
403 Forbidden
404 Not Found

put
/sale/user-ratings/{ratingId}/answer
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
{
"message": "That is not our fault"
}
Response samples
201400
Content type
application/vnd.allegro.public.v1+json

Copy
{
"createdAt": "2017-05-17T08:36:57.292Z",
"message": "That is not our fault"
}
Request removal of user's rating
Use this resource to request removal of received rating. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
ratingId
required
string
Example: 5df0a6d1ef437e00255572a1
ID of the rating.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
User rating removal request.

request
required
object
Responses
201 OK
400 Bad request
401 Unauthorized
403 Forbidden
404 Not Found

put
/sale/user-ratings/{ratingId}/removal
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"request": {
"message": "string"
}
}
Response samples
201400
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"possibleTo": "2017-05-17T08:36:57.292Z",
"request": {
"createdAt": "2017-05-17T08:36:57.292Z",
"message": "string",
"source": "SELLER"
}
}
Get sales quality
Use this resource to get current sales quality with at most 30 days history. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Unauthorized
403 Forbidden

get
/sale/quality
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"quality": [
{}
]
}
Get basic information about user
Use this resource when you need basic information about authenticated user. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 OK
401 Unauthorized
403 Forbidden - when token is without user context

get
/me
Response samples
200401403
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "46968690",
"login": "Client:46968690",
"firstName": "Amadeusz",
"lastName": "Iksiński",
"email": "user-email@allegro.pl",
"baseMarketplace": {
"id": "allegro-pl"
},
"company": {
"name": "Allegro.pl sp. z o.o.",
"taxId": "5252674798"
},
"features": [
"SUPER_SELLER",
"ONE_FULFILLMENT"
]
}
Get user's additional emails
Use this resource to get a list of all additional email addresses assigned to account. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 List of user's additional emails returned successfully
401 Unauthorized

get
/account/additional-emails
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"additional-emails": [
{}
]
}
Add a new additional email address to user's account
Use this resource to add a new additional email address to account. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
request

email
required
string
A valid email address you want to add to your account. Maximum length of the part before the @ sign is 64 characters.

Responses
201 Additional email added successfully
400 Bad request
401 Unauthorized
422 Email address provided in the request is not valid

post
/account/additional-emails
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
{
"email": "test@allegro.pl"
}
Response samples
201
Content type
application/vnd.allegro.public.v1+json

Copy
{
"id": "8fe19442-d0c0-4a84-873f-42fc40a7bcf0",
"email": "example@allegro.pl",
"createdAt": "2011-12-03T10:15:30Z"
}
Get information about a particular additional email
Use this resource to retrieve a single additional email. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
emailId
required
string
Id of the additional email.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Additional email returned successfully
401 Unauthorized
404 Additional email not found

get
/account/additional-emails/{emailId}
Response samples
200401
Content type
application/vnd.allegro.public.v1+json

Copy
{
"id": "8fe19442-d0c0-4a84-873f-42fc40a7bcf0",
"email": "example@allegro.pl",
"createdAt": "2011-12-03T10:15:30Z"
}
Delete an additional email address
Use this resource to delete one of additional emails. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
emailId
required
string
Id of the additional email to be deleted.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
204 Successfully deleted additional email
401 Unauthorized
404 Additional email not found

delete
/account/additional-emails/{emailId}
Response samples
401
Content type
application/vnd.allegro.public.v1+json

Copy
{
"error": "unauthorized",
"error_description": "Full authentication is required to access this resource"
}
Get Smart! seller classification report
Use this resource to get a full Smart! seller classification report. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
marketplaceId	
string
Example: marketplaceId=allegro-pl
Marketplace for which seller classification report will be returned. If not specified, the classification result for the seller's registration marketplace will be returned.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Successfully returned seller Smart! classification report
401 Unauthorized action
404 Not Found
422 Unprocessable entity

get
/sale/smart
Response samples
200401404422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"classification": {
"fulfilled": true,
"lastChanged": "2017-05-17T08:36:57.292+02:00"
},
"conditions": [
{},
{},
{}
],
"excludedDeliveryMethods": [
{}
]
}
Information about marketplaces
Get details for all marketplaces in allegro
Use this resource to get information about all the marketplaces on the platform. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "en-US"
Example: en-US
Expected language of messages.

Responses
200 Successfully returned all available marketplaces in allegro

get
/marketplaces
Response samples
200
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"marketplaces": [
{}
]
}
Message Center
List user threads
Use this resource to get the list of user threads sorted by last message date, starting from newest. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
limit	
integer <int32> [ 1 .. 20 ]
Default: 20
The maximum number of threads returned in the response.

offset	
integer <int64> [ 0 .. 15000000 ]
Default: 0
Index of the first returned thread from all results. Available only for content version 'application/vnd.allegro.public.v1+json'.

page.id	
string
ID of the page of threads to retrieve. Available only for content version 'application/vnd.allegro.beta.v1+json'.

read	
boolean
Filters threads by read status. Available only for content version 'application/vnd.allegro.beta.v1+json'.

status	
string
Enum: "OPEN" "CLOSED"
Filters threads by status. Available only for content version 'application/vnd.allegro.beta.v1+json'.

type	
Array of strings
Items Enum: "COMMON" "POST_PURCHASE_ISSUE"
Filters threads by their type. Available only for content version 'application/vnd.allegro.beta.v1+json'. If omitted, threads of all types are returned. If you pass multiple values, the response includes threads whose type matches any of them.

orderId	
string
Filters POST_PURCHASE_ISSUE threads by order identifier. Available only for content version 'application/vnd.allegro.beta.v1+json'.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 OK
401 User not authorized
422 Incorrect limit or offset

get
/messaging/threads
Response samples
200
Content type

application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"threads": [
{}
],
"offset": 20,
"limit": 20
}
Get user thread
Use this resource to get thread with provided identifier. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
threadId
required
string
Identifier of thread to get.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Thread returned successfully
401 User not authorized
404 Thread not found

get
/messaging/threads/{threadId}
Response samples
200
Content type

application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "88ae369b-8f65-4fc4-9c77-bedf604a2e2",
"read": "false",
"lastMessageDateTime": "2020-08-26T12:52:04Z",
"interlocutor": {
"login": "AllegroLogin",
"avatarUrl": "https://a.allegroimg.com/original/0129e7/f15ce8924166850eec3fb82bcd5s/avatar"
}
}
Mark a particular thread as read
Use this resource to mark thread with provided identifier as read. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
threadId
required
string
Identifier of thread to be marked.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: 
application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json
Updated read flag

read
required
boolean
Responses
200 Thread marked as read successfully
401 User not authorized
403 User not allowed to update thread read flag
404 Thread not found
422 Validation errors - missing flag in the request body

put
/messaging/threads/{threadId}/read
Request samples
Payload
Content type

application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json

Copy
{
"read": "false"
}
Response samples
200
Content type

application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "88ae369b-8f65-4fc4-9c77-bedf604a2e2",
"read": "false",
"lastMessageDateTime": "2020-08-26T12:52:04Z",
"interlocutor": {
"login": "AllegroLogin",
"avatarUrl": "https://a.allegroimg.com/original/0129e7/f15ce8924166850eec3fb82bcd5s/avatar"
}
}
Write a new message
Use this resource to write new message to recipient. This resource is rate limited to 1 request per second for a user. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: 
application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json
Object representing new message.

recipient
required
object (Recipient)
text
required
string <= 2000 characters
attachments	
Array of objects or null (MessageAttachmentId)
order
required
object (MessageOrder)
Responses
201 Message successfully written
401 Authentication required
422 Validation errors

post
/messaging/messages
Request samples
Payload
Content type

application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"recipient": {
"login": "AllegroLogin"
},
"text": "Sample message",
"attachments": [
{}
],
"order": {
"id": "88ae369b-8f65-4fc4-9c77-bedf604a2e2"
}
}
Response samples
201
Content type

application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "97dc0b60-2da4-4247-92ba-b748630ba0f6",
"status": "DELIVERED",
"type": "MESSAGE_CENTER",
"createdAt": "2020-08-26T12:52:04Z",
"thread": {
"id": "88ae369b-8f65-4fc4-9c77-bedf604a2e2"
},
"author": {
"login": "AllegroLogin",
"isInterlocutor": true
},
"text": "Sample message",
"subject": "Sample subject",
"relatesTo": {
"offer": {},
"order": {}
},
"hasAdditionalAttachments": false,
"attachments": [
{}
],
"additionalInformation": {
"vin": "JT2SV12E6F0308977"
}
}
List messages in thread
Use this resource to list messages in thread with provided identifier. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
threadId
required
string
Identifier of thread to get messages from.

query Parameters
limit	
integer <int32> [ 1 .. 20 ]
Default: 20
The maximum number of messages returned in the response.

offset	
integer <int64> [ 0 .. 15000 ]
Default: 0
Index of the first returned message from all results. Available only for content version 'application/vnd.allegro.public.v1+json'.

before	
string <date-time>
Example: before=2020-11-13T12:45:20.818Z
Message creation date before filter parameter (exclusive) - cannot be used with offset. Available only for content version 'application/vnd.allegro.public.v1+json'.

after	
string <date-time>
Example: after=2020-11-13T12:45:20.818Z
Message creation date after filter parameter (exclusive). Available only for content version 'application/vnd.allegro.public.v1+json'.

page.id	
string
ID of the page of messages to retrieve. Available only for content version 'application/vnd.allegro.beta.v1+json'.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Thread message list returned successfully
401 User not authorized
403 User not allowed to list messages in selected thread
404 Thread not found
422 Incorrect limit, offset, after or before

get
/messaging/threads/{threadId}/messages
Response samples
200
Content type

application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"messages": [
{}
],
"offset": 20,
"limit": 20
}
Write a new message in thread
Use this resource to write new message in existing thread. This resource is rate limited to 1 request per second for a user. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
threadId
required
string
Identifier of thread to write message to.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: 
application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json
text
required
string <= 2000 characters
attachments	
Array of objects or null (MessageAttachmentId)
Responses
201 Message in thread successfully written
401 User not authorized
403 User not allowed to list messages in selected thread
404 Thread not found
422 Validation errors

post
/messaging/threads/{threadId}/messages
Request samples
Payload
Content type

application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"text": "Sample message",
"attachments": [
{}
]
}
Response samples
201422
Content type

application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "97dc0b60-2da4-4247-92ba-b748630ba0f6",
"status": "DELIVERED",
"type": "MESSAGE_CENTER",
"createdAt": "2020-08-26T12:52:04Z",
"thread": {
"id": "88ae369b-8f65-4fc4-9c77-bedf604a2e2"
},
"author": {
"login": "AllegroLogin",
"isInterlocutor": true
},
"text": "Sample message",
"subject": "Sample subject",
"relatesTo": {
"offer": {},
"order": {}
},
"hasAdditionalAttachments": false,
"attachments": [
{}
],
"additionalInformation": {
"vin": "JT2SV12E6F0308977"
}
}
Get single message
Use this resource to get message with provided identifier. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
messageId
required
string
Identifier of message to be returned.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Message returned successfully
401 User not authorized
404 Message not found

get
/messaging/messages/{messageId}
Response samples
200
Content type

application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"id": "97dc0b60-2da4-4247-92ba-b748630ba0f6",
"status": "DELIVERED",
"type": "MESSAGE_CENTER",
"createdAt": "2020-08-26T12:52:04Z",
"thread": {
"id": "88ae369b-8f65-4fc4-9c77-bedf604a2e2"
},
"author": {
"login": "AllegroLogin",
"isInterlocutor": true
},
"text": "Sample message",
"subject": "Sample subject",
"relatesTo": {
"offer": {},
"order": {}
},
"hasAdditionalAttachments": false,
"attachments": [
{}
],
"additionalInformation": {
"vin": "JT2SV12E6F0308977"
}
}
Delete single message Deprecated
Use this resource to delete message with provided identifier. This resource is deprecated and will be removed in the future. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
messageId
required
string
Identifier of the message to delete.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
204 Message successfully deleted
401 User not authorized
403 User not allowed to delete particular message
404 Message not found

delete
/messaging/messages/{messageId}
Add attachment declaration
Use this resource to add attachment declaration before uploading. Read more: PL / EN.

Authorizations:
bearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: 
application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json
filename
required
string
size
required
integer <int64> [ 0 .. 5242880 ]
Responses
201 Attachment declaration successfully added
401 User not authorized
415 Unsupported mime type
422 Validation errors

post
/messaging/message-attachments
Request samples
Payload
Content type

application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json

Copy
{
"filename": "attachment",
"size": "34923"
}
Response samples
201
Content type

application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json

Copy
{
"id": "97dc0b60-2da4-4247-92ba-b748630ba0f6"
}
Upload attachment binary data
Use this resource to upload attachment using identifier that was declared. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
attachmentId
required
string
The identifier of attachment that will be uploaded.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: 
image/png
image/png
string <binary>
File in a binary format

Responses
200 Attachment succesfully uploaded.
401 User not authorized
403 User does not have
404 Attachment declaration not found
413 Exceeded size limit
415 Unsupported mime type

put
/messaging/message-attachments/{attachmentId}
Response samples
200
Content type

application/vnd.allegro.public.v1+json
application/vnd.allegro.public.v1+json

Copy
{
"id": "97dc0b60-2da4-4247-92ba-b748630ba0f6"
}
Download attachment
Use this resource to download attachment with provided identifier. You can retrieve attachments uploaded within the last 6 months. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
attachmentId
required
string
Identifier of the attachment that will be downloaded.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Attachment file returned successfully
401 User not authorized
404 Attachment not found

get
/messaging/message-attachments/{attachmentId}
Billing
Get a list of billing entries
Use this resource to get a list of billing entries. The billing entries are sorted in descending order (newest first) by the date on which they occurred. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
marketplaceId	
string
Example: marketplaceId=allegro-pl
The marketplace ID where operation was made. By default the marketplace ID where the user is registered. Note: Business marketplace is not a separate user's billing and defaults back to the main marketplace for given country.

occurredAt.gte	
string <date-time>
Example: occurredAt.gte=2019-05-08T09:45:32.818Z
Date from which billing entries are filtered. If occurredAt.lte is also set, occurredAt.gte cannot be later.

occurredAt.lte	
string <date-time>
Example: occurredAt.lte=2019-05-08T09:45:32.818Z
Date to which billing entries are filtered. If occurredAt.gte is also set, occurredAt.lte cannot be earlier.

type.id	
Array of strings
Example: type.id=LIS&type.id=SUC
List of billing types by which billing entries are filtered.

offer.id	
string
Example: offer.id=12345
Offer ID by which billing entries are filtered.

order.id	
string <uuid>
Example: order.id=29738e61-7f6a-11e8-ac45-09db60ede9d6
Order UUID by which billing entries are filtered.

limit	
integer <int32> [ 1 .. 100 ]
Default: 100
Example: limit=10
Number of returned operations.

offset	
integer <int32> [ 0 .. 10000 ]
Default: 0
Example: offset=10
Index of the first returned payment operation from all search results.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 List of billing entries returned successfully.
401 Unauthorized
406 Not Acceptable
422 Unprocessable Entity

get
/billing/billing-entries
Response samples
200401406422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"billingEntries": [
{}
]
}
Get a list of billing types
Use this resource to get a list of all billing types. Type names are localized according to the "Accept-Language" header. Read more: PL / EN.

Authorizations:
bearer-token-for-applicationbearer-token-for-user
header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 List of billing types returned successfully.
401 Unauthorized

get
/billing/billing-types
Response samples
200401
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
[
{
"id": "SUC",
"description": "Prowizja od sprzedaży"
}
]
Auctions and Bidding
Place a bid in an auction
Use this resource to place a bid in an auction. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
offerId
required
string
The offer ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Request Body schema: application/vnd.allegro.public.v1+json
maxAmount
required
object (MaxPrice)
Maximum amount that user is willing to pay for the auction.

Responses
200 Bid succesfully placed
400 Bad request.
401 Unauthorized
404 Auction not found.
422 If bidding was not allowed (see message for explanation).

put
/bidding/offers/{offerId}/bid
Request samples
Payload
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"maxAmount": {
"amount": "123.45",
"currency": "PLN"
}
}
Response samples
200400401404422
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"maxAmount": {
"amount": "123.45",
"currency": "PLN"
},
"minimalPriceMet": false,
"highBidder": true,
"auction": {
"currentPrice": {}
}
}
Get current user's bid information
Use this resource to retrieve current user's bid information. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
offerId
required
string
The offer ID.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: en-US
Expected language of messages.

Responses
200 Bid information succesfully found.
404 Auction not found or user did not bid in the auction.

get
/bidding/offers/{offerId}/bid
Response samples
200404
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"maxAmount": {
"amount": "123.45",
"currency": "PLN"
},
"minimalPriceMet": false,
"highBidder": true,
"auction": {
"currentPrice": {}
}
}
Charity
Search fundraising campaigns
Use this resource to search fundraising campaigns. Read more: PL / EN.

Authorizations:
bearer-token-for-user
query Parameters
limit
required
integer <int32> [ 1 .. 100 ]
Maximum number of returned results.

phrase
required
string
Fundraising campaign name or it's Organization name prefix to search for.

header Parameters
Accept-Language	
string <BCP-47 language code>
Value: "pl-PL"
Example: pl-PL
Expected language of messages.

Responses
200 The request successfully returns the search result.
400 Invalid or missing query parameters.
401 Unauthorized
403 Forbidden

get
/charity/fundraising-campaigns
Response samples
200
Content type
application/vnd.allegro.beta.v1+json

Copy
Expand allCollapse all
{
"campaigns": [
{}
]
}
Public user information
Get any user's ratings summary
Use this resource to receive feedback statistics. Read more: PL / EN.

Authorizations:
bearer-token-for-user
path Parameters
userId
required
string
Example: 41846511
The ID of the user.

header Parameters
Accept-Language	
string <BCP-47 language code>
Enum: "en-US" "pl-PL" "uk-UA" "sk-SK" "cs-CZ" "hu-HU"
Example: pl-PL
Expected language of messages.

Responses
200 Feedback statistics returned successfully.
401 Unauthorized
403 Forbidden
404 User with the given ID not found or user is not a seller.

get
/users/{userId}/ratings-summary
Response samples
200401403
Content type
application/vnd.allegro.public.v1+json

Copy
Expand allCollapse all
{
"recommended": {
"unique": 80,
"total": 100
},
"notRecommended": {
"unique": 80,
"total": 100
},
"recommendedPercentage": "99,8",
"statistics": {
"received": {},
"excluded": {},
"removed": {}
},
"user": {
"createdAt": "2023-01-15"
}
}
Allegro
Serwisy Grupy Allegro

Allegro.cz
Allegro.sk
Allegro.hu
Onedelivery.cz