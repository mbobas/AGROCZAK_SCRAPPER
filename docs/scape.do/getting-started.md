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


llms.txt
Getting Started
View as Markdown
Scrape.do provides unblocked access to public web data at scale by:

Avoiding all anti-bot, WAF, and CAPTCHA through custom bypass solutions.
Rotating 150M+ datacenter, residential, and mobile proxies in 150 countries.
Seamlessly rendering and interacting web pages with its managed headless browser.
After signing up for Scrape.do and generating your API key, test your setup with a basic request:


Proxy Mode
curl
python
node
go
ruby
java
csharp
php

curl --location --request GET 'https://api.scrape.do/?token=YOUR_TOKEN&url=https://httpbin.co/anything'
Generate API Token
All your requests are authorized with your account token, which is automatically generated when you first sign up.

Your token is located in your dashboard here:

Token Location
If you haven't signed up yet, create a free-forever account here.

API Playground
The API Playground is your interactive testing environment where you can experiment with Scrape.do parameters without writing code. Use it to:

Test different parameter combinations in real-time
Generate code snippets in multiple programming languages (Python, Node.js, PHP, cURL, etc.)
Preview API responses before implementing in your application
Learn how parameters affect request behavior
API Playground Dashboard

Access the playground from your dashboard to build and refine your scraping requests with instant feedback.

Encode Your Target URL
Pass the target website URL you want to scrape using the url parameter.

When using API mode, you must URL-encode the parameter to prevent it from being misinterpreted as multiple query parameters (supported protocols: HTTP and HTTPS).

curl
python
node
go
ruby
java
csharp
php

sudo apt-get install gridsite-clients
urlencode "YOUR_URL"
No need to encode the URL if you use Proxy Mode.

API Parameters Overview
You can view all the parameters of Scrape.do from the table below and have an overview of all of them quickly.

Parameter	Type	Default	Description	Details
token*	string		The token to use for authentication.	more
url*	string		Target web page URL.	more
super	bool	false	Use Residential & Mobile Proxy Networks	more
geoCode	string		Choose the right country for your target web page	more
regionalGeoCode	string		Choose continent for your target web page	more
sessionId	int		Use the same IP address continuously with a session	more
customHeaders	bool	false	Handle all request headers for the target web page	more
extraHeaders	bool	false	Use it to change header values or add new headers over the ones we have added	more
forwardHeaders	bool	false	Forward your own headers to the target website	more
setCookies	string		Set cookies for the target web page	more
disableRedirection	bool	false	Disable request redirection for your use-case	more
callback	string		Deprecated. Use Async API webhooks instead	more
timeout	int	60000	Set maximum timeout for your requests	more
retryTimeout	int	15000	Set maximum timeout for retry mechanism	more
disableRetry	bool	false	Disable retry mechanism for your use-case	more
device	string	desktop	Specify the device type (desktop, mobile, tablet)	more
render	bool	false	Use a headless browser to render JavaScript and wait for content to load	more
waitUntil	string	domcontentloaded	Control when the browser considers the page loaded	more
customWait	int	0	Set the browser wait time on the target web page after content loaded	more
waitSelector	string		CSS selector to wait for in the target web page	more
width	int	1920	Browser viewport width in pixels	more
height	int	1080	Browser viewport height in pixels	more
blockResources	bool	true	Block CSS, images, and fonts on your target web page	more
screenShot	bool	false	Return a screenshot from your target web page	more
fullScreenShot	bool	false	Return a full page screenshot from your target web page	more
particularScreenShot	string		Return a screenshot of a particular area from your target web page	more
playWithBrowser	string		Simulate browser actions like click, scroll, execute js, etc.	more
output	string	raw	Get the output in raw or markdown format	more
transparentResponse	bool	false	Return pure response from target web page without Scrape.do processing	more
returnJSON	bool	false	Returns network requests with content as a property string	more
showFrames	bool	false	Returns all iframe content from the target webpage (requires render=true and returnJSON=true)	more
showWebsocketRequests	bool	false	Display websocket requests (requires render=true and returnJSON=true)	more
pureCookies	bool	false	Returns the original Set-Cookie headers from the target website	more
How Does Scrape.do Work?
Modern websites use sophisticated anti-bot systems (Cloudflare, PerimeterX, DataDome, Akamai) that fingerprint TLS handshakes, validate HTTP headers, and blacklist datacenter IPs to block automated traffic.

Scrape.do solves this by handling all anti-bot evasion on your behalf.

Technically, we act as an intelligent proxy layer between your application and target websites. Every request is intercepted, upgraded to mimic legitimate browser behavior at multiple layers (TLS, HTTP, JavaScript), routed through our residential/mobile proxy network, and delivered as if from a real user. Your request goes through our infrastructure which:

Routes through rotating proxies — Your request is forwarded through our pool of 150M+ datacenter, residential, and mobile IPs across 150 countries, automatically rotating to avoid rate limits and IP bans.

Mimics real browser behavior — We manipulate TLS fingerprints and HTTP headers to match legitimate browser traffic, making your requests indistinguishable from organic users to bypass WAFs and anti-bot systems.

Renders JavaScript if needed — Setting render=true spins up a headless browser (Chromium) to execute JavaScript and load dynamic content, essential for modern SPAs built with React, Vue, or Angular.

Handles CAPTCHAs automatically — When target sites present CAPTCHA challenges (reCAPTCHA, hCaptcha, etc.), our system detects and solves them transparently without your intervention.

Retries intelligently — If a request fails due to temporary issues (502/503, timeouts, rate limits), we automatically retry with a different IP until success or timeout.

Returns clean data — You receive the raw HTML, JSON, or any content type the target website returns. API credits are only consumed on successful requests (2xx status codes).

For asynchronous processing of long-running jobs, use the Async API to submit jobs and receive results via webhook instead of keeping connections open.

Credits
Credits are the unit of billing in Scrape.do. You are only charged for successful requests (status codes 2xx, 400, 404, 410). Failed requests are free.

Not all requests cost the same. Some websites require advanced bypass methods (residential proxies, headless browser rendering, or custom anti-detection solutions), which consume more credits per request. For example, a basic datacenter request costs 1 credit, while a residential proxy request with JS rendering costs 25.

See the full Request Costs table for credit pricing by request type and domain-specific pricing.

Concurrency
Concurrency is the number of requests your account can process simultaneously. Each plan has a concurrency limit that determines how many requests can be in-flight at the same time.

If you hit your concurrency limit, additional requests will be queued or rejected until a slot opens up. The Async API has a separate concurrency pool (30% of your plan limit) that runs independently from your main API concurrency, so you can use both without interference.

Request Costs

Next Page

On this page
Generate API Token
API Playground
Encode Your Target URL
API Parameters Overview
How Does Scrape.do Work?
Credits
Concurrency
Getting Started | Documentation | Scrape.do