logoSearch
Ctrl
K
Getting Started
Request Costs
Proxy Settings
API & Response
Headers & Cookies
Headless Browser
Integrations
Amazon Scraper API
Google Scraper API
Walmart Scraper API
Lowes Scraper API
Home Depot Scraper API
YouTube Scraper API
GET
ChatGPT Scraper API
GET
Asynchronous API
Proxy Mode
Libraries
Frequently Asked Questions
Contact Us
Changelog


Request Costs
View as Markdown
Scrape.do charges credits only for successful results. Failed requests cost nothing, your credits are only consumed when a successful response is returned.

Status codes counted as successful: 2XX, 400, 404, 410. If you see a target site returning one of these codes but the response is invalid for your use case, contact support@scrape.do and we can add a custom rule for your account.

How the cost of a request is determined
The credit cost of any request is decided by two things:

The proxy type and rendering mode you requested (set with the super and render query parameters). This is the baseline cost in the table below.
Whether the target domain has a default proxy / render profile applied server-side. For some domains, super=true and/or render=true are turned on automatically because that is the only configuration that reliably bypasses the target. In those cases the request costs the same as if you had passed those parameters yourself.
Always check the Scrape.do-Request-Cost response header to confirm what the request actually cost. That value is authoritative.

Base cost by request type
These are the standard costs for untargeted domains (domains not in the per-domain table below).

Request type	Credits
Normal request (datacenter proxy)	1
Datacenter + headless browser (render=true)	5
Residential / mobile (super=true)	10
Residential / mobile + headless browser (super + render)	25
Per-domain pricing
For the following domains, Scrape.do applies a default proxy or render profile server-side for reliability reasons. The "Defaults applied" column shows what is turned on for you automatically; the "Cost" column reflects what you will be charged whether or not you also passed those parameters in your request.

If your call already had stricter parameters (e.g., you sent super=true&render=true for a domain that only defaults to super=true), the higher cost applies.

Domain	Cost	Defaults applied	Notes
amazon.*	1	Routed via the Amazon Scraper API	Returns structured JSON. See the Amazon Scraper API docs.
google.*	10	super=true by default	Residential proxy automatically applied for reliable SERP access.
idealista.*	10	super=true by default	Residential proxy automatically applied.
akakce.com	10	super=true by default	Residential proxy automatically applied.
capterra.com	10	super=true by default	Residential proxy automatically applied.
hermes.com	10	super=true by default	Residential proxy automatically applied for consistent access.
leboncoin.fr	10	super=true by default	Residential proxy automatically applied.
mouser.com	10	super=true by default	Residential proxy automatically applied for consistent access.
cineworld.co.uk	20	super=true by default	Custom anti-detection profile.
chewy.com	50	Requires super=true	Custom solution. Contact support for access.
fastpeoplesearch.com	25	Requires super=true	Specialized extraction with enhanced success rates.
g2.com	25	Custom anti-detection	Specialized extraction profile.
leroymerlin.fr	25	Custom anti-detection	Specialized extraction profile.
mscdirect.com	25	Requires super=true	Custom solution with enhanced success rates.
naver.com	25	Custom infrastructure	Contact support for access.
realestate.com.au	25	super=true + render=true by default	Residential proxy with headless browser rendering automatically applied.
shein.*	25	Custom anti-detection	Specialized extraction profile.
therealreal.com	25	render=true by default	Browser rendering with enhanced proxy automatically applied.
linkedin.com	30	Custom infrastructure	Specialized handling required for platform restrictions.
aircanada.com	75	super=true + render=true by default	Residential + headless browser automatically applied.
jd.com	75	Custom infrastructure + super=true	Specialized solution.
shopee.*	100	Custom infrastructure	Full coverage across regions. Contact support for access.
carsales.com.au	25 to 200	Dynamic per request complexity	Contact support for access.
sainsburys.co.uk	200	Custom anti-detection	Specialized extraction profile.
nordstrom.*	25	Custom anti-detection	Specialized extraction profile.
lowes.com	10	Custom anti-detection	Specialized extraction profile.
Why does the per-domain cost differ from the base table? For these targets, Scrape.do has determined the minimum proxy / render profile that reliably bypasses the site, and applies it server-side. You do not need to pass super=true or render=true yourself, but the request is charged at the rate of that profile.

Always trust the response header. The Scrape.do-Request-Cost header on every response tells you exactly how many credits the call consumed. Use it for billing reconciliation rather than guessing from the table.

Confirming the cost of a request
Every successful response includes two headers you can read directly:

Header	What it tells you
Scrape.do-Request-Cost	Credits consumed by this specific request
Scrape.do-Remaining-Credits	Credits remaining on your subscription after this request
Both are documented on the Response Headers page.

Adding a new domain to the per-domain list
If a target site is consistently failing for you with default parameters and you want it added to the per-domain profile list, contact support@scrape.do with the URL pattern, your typical request volume, and any sample failing responses you have.

Getting Started

Previous Page

Proxy Settings

Configure proxy settings for your scraping requests

On this page
How the cost of a request is determined
Base cost by request type
Per-domain pricing
Confirming the cost of a request
Adding a new domain to the per-domain list
Request Costs | Documentation | Scrape.do