logoSearch
Ctrl
K
Getting Started
Request Costs
Proxy Settings
Super (Residential & Mobile)
Geo Targeting
Regional Geo Targeting
Postal Code (ZIP Code) Targeting
API & Response
POST/PUT Request
Timeout
Retry Settings
Disable Redirection
Device
Sticky Sessions
Output & Response
How to Solve Blocking Issues
Status Codes
Usage Statistics
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


API & Response
POST/PUT Request
View as Markdown
Send POST and PUT requests to target websites

You can change the method type for all the requests to send with Scrape.do. We support GET, POST, PUT, PATCH, HEAD and DELETE methods.


Proxy Mode
curl
python
node
go
ruby
java
csharp
php

import requests
import json
import urllib.parse
token = "YOUR_TOKEN"
params = {
    "token": token,
    "url": "https://httpbin.org/anything",
}
data = json.dumps({
    "foo": "bar"
})
url = f"http://api.scrape.do/?{urllib.parse.urlencode(params)}"
method = "POST"
headers = {
    "Content-Type": "application/json",
}
response = requests.request(method, url, headers=headers, data=data)
print(f"Response status: {response.status_code}")
print(response.text)
API & Response

API configuration, request costs, and response customization

Timeout

Set request timeout

POST/PUT Request | Documentation | Scrape.do
logoSearch
Ctrl
K
Getting Started
Request Costs
Proxy Settings
Super (Residential & Mobile)
Geo Targeting
Regional Geo Targeting
Postal Code (ZIP Code) Targeting
API & Response
POST/PUT Request
Timeout
Retry Settings
Disable Redirection
Device
Sticky Sessions
Output & Response
How to Solve Blocking Issues
Status Codes
Usage Statistics
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


API & Response
Timeout
View as Markdown
Set request timeout

You can set the timeout value for the request you will send to the target website.

The value it can take must be between 5000 ms and 120000 ms. If the time is exceeded, system will return you that the request failed.


Proxy Mode
curl
python
node
go
ruby
java
csharp
php

import requests
import urllib.parse
token = "YOUR_TOKEN"
targetUrl = urllib.parse.quote("https://httpbin.co/sse?delay=1s")
timeout = "10000"
url = "http://api.scrape.do/?token={}&url={}&timeout={}".format(token, targetUrl,timeout)
response = requests.request("GET", url)
print(response.text)
POST/PUT Request

Send POST and PUT requests to target websites

Retry Settings

Configure retry behavior and timeout limits

Timeout | Documentation | Scrape.do
logoSearch
Ctrl
K
Getting Started
Request Costs
Proxy Settings
Super (Residential & Mobile)
Geo Targeting
Regional Geo Targeting
Postal Code (ZIP Code) Targeting
API & Response
POST/PUT Request
Timeout
Retry Settings
Disable Redirection
Device
Sticky Sessions
Output & Response
How to Solve Blocking Issues
Status Codes
Usage Statistics
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


API & Response
Retry Settings
View as Markdown
Configure retry behavior and timeout limits

Scrape.do automatically retries failed requests to maximize your success rate. These settings allow you to control how long the system waits before retrying and whether to disable retries entirely for specific use cases.

Retry Timeout
Our system determines the maximum waiting time with this parameter while waiting for results from the target website. When the time is exceeded, it sends a new request and checks it cyclically.

You can change this parameter, which is 15000 ms by default. The values it can take can be between 5000ms and 55000ms.

Important: Using this parameter can affect your success rates.


Proxy Mode
curl
python
node
go
ruby
java
csharp
php

import requests
import urllib.parse
token = "YOUR_TOKEN"
targetUrl = urllib.parse.quote("https://httpbin.co/anything")
timeout = "5000"
url = "http://api.scrape.do/?token={}&url={}&retryTimeout={}".format(token, targetUrl, timeout)
response = requests.request("GET", url)
print(response.text)
Disable Retry
When you use this parameter, our system will not retry the request if it fails.

Regardless of the initial response status, it will return you the result as successful or unsuccessful. This is useful when you want immediate results without waiting for retry attempts, or when you're implementing your own retry logic at the application level.


Proxy Mode
curl
python
node
go
ruby
java
csharp
php

import requests
import urllib.parse
token = "YOUR_TOKEN"
targetUrl = urllib.parse.quote("https://httpbin.co/anything")
disableRetry = "true"
url = "http://api.scrape.do/?token={}&url={}&disableRetry={}".format(token, targetUrl,disableRetry)
response = requests.request("GET", url)
print(response.text)
Timeout

Set request timeout

Disable Redirection

Control redirect behavior for your requests

On this page
Retry Timeout
Disable Retry
Retry Settings | Documentation | Scrape.do

logoSearch
Ctrl
K
Getting Started
Request Costs
Proxy Settings
Super (Residential & Mobile)
Geo Targeting
Regional Geo Targeting
Postal Code (ZIP Code) Targeting
API & Response
POST/PUT Request
Timeout
Retry Settings
Disable Redirection
Device
Sticky Sessions
Output & Response
How to Solve Blocking Issues
Status Codes
Usage Statistics
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


API & Response
Disable Redirection
View as Markdown
Control redirect behavior for your requests

Scrape.do by default follow redirected target web pages and returns results from where it redirected. It has a maximum of 10 redirections. If you reach the limit, the system will stop redirection and return a response with the last status.

In some cases, you may not want to use the redirection mechanism. By passing the disableRedirection=true parameter, you can prevent default redirection.

When you use this feature, you can find the url information that the target website wants to redirect you to in the Scrape.do-Target-Redirected-Location header.


Proxy Mode
curl
python
node
go
ruby
java
csharp
php

import requests
import json
import urllib.parse
token = "YOUR_TOKEN"
params = {
    "token": token,
    "url": "https://httpbin.co/redirect-to?status_code=307&url=http://example.com/",
    "disableRedirection": True,
}
data = None
url = f"http://api.scrape.do/?{urllib.parse.urlencode(params)}"
method = "GET"
headers = {}
response = requests.request(method, url, headers=headers, data=data)
print(f"Response status: {response.status_code}")
print(response.text)
Retry Settings

Configure retry behavior and timeout limits

Device

Emulate various devices

Disable Redirection | Documentation | Scrape.do

logoSearch
Ctrl
K
Getting Started
Request Costs
Proxy Settings
Super (Residential & Mobile)
Geo Targeting
Regional Geo Targeting
Postal Code (ZIP Code) Targeting
API & Response
POST/PUT Request
Timeout
Retry Settings
Disable Redirection
Device
Sticky Sessions
Output & Response
How to Solve Blocking Issues
Status Codes
Usage Statistics
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


API & Response
Device
View as Markdown
Emulate various devices

The device parameter is used to determine the type of device used for data scraping through our API service. We offer three options: "Desktop", "Mobile" and "Tablet". These options allow us to identify which devices users are accessing and optimize data scraping for the desired device. A website can be presented in different designs on desktop computers, mobile devices and tablet devices. Therefore, the correct identification of the device used in data scraping increases the accuracy and relevance of the obtained data.

Important: You can improve the user experience. For example, mobile-optimized data scraping provides faster response times and better performance.


Proxy Mode
curl
python
node
go
ruby
java
csharp
php

import requests
import json
import urllib.parse
token = "YOUR_TOKEN"
params = {
    "token": token,
    "url": "https://httpbin.co/headers",
    "device": "mobile",
}
data = None
url = f"http://api.scrape.do/?{urllib.parse.urlencode(params)}"
method = "GET"
headers = {}
response = requests.request(method, url, headers=headers, data=data)
print(f"Response status: {response.status_code}")
print(response.text)
Disable Redirection

Control redirect behavior for your requests

Sticky Sessions

Session based scraping

Device | Documentation | Scrape.do

logoSearch
Ctrl
K
Getting Started
Request Costs
Proxy Settings
Super (Residential & Mobile)
Geo Targeting
Regional Geo Targeting
Postal Code (ZIP Code) Targeting
API & Response
POST/PUT Request
Timeout
Retry Settings
Disable Redirection
Device
Sticky Sessions
Output & Response
How to Solve Blocking Issues
Status Codes
Usage Statistics
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


API & Response
Sticky Sessions
View as Markdown
Session based scraping

When you want to use the same proxy address for a certain period of time, you can pass the sessionId=1234 parameter. It can be any integer value. Each unique integer value will be the ID of a session.

SessionId value must be between 0 and 1000000.
If no request is sent within 5 minutes, the session you created will be closed automatically.
If the request sent with SessionId fails, a new proxy address will be provided and the session will be changed.
If you need to use new proxy constantly, you don't need to use session!
If used with Geo Targeting or Regional Geo Targeting, the session will be created only for the relevant country or region.
Sessions are created only for successful requests!
Example:


Proxy Mode
curl
python
node
go
ruby
java
csharp
php

import requests
import urllib.parse
token = "YOUR_TOKEN"
targetUrl = urllib.parse.quote( "https://httpbin.co/anything")
sessionId = "1234"
url = "http://api.scrape.do/?token={}&url={}&sessionId={}".format(token, targetUrl,sessionId)
response = requests.request("GET", url)
print(response.text)
Device

Emulate various devices

Output & Response

Customize response

Sticky Sessions | Documentation | Scrape.do

logoSearch
Ctrl
K
Getting Started
Request Costs
Proxy Settings
Super (Residential & Mobile)
Geo Targeting
Regional Geo Targeting
Postal Code (ZIP Code) Targeting
API & Response
POST/PUT Request
Timeout
Retry Settings
Disable Redirection
Device
Sticky Sessions
Output & Response
How to Solve Blocking Issues
Status Codes
Usage Statistics
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


API & Response
Output & Response
View as Markdown
Customize response

Here we present the parameters where the responses returned by our system can be customized.

Output Format
Scrape.do does support markdown output for LLM data training or other necessary purposes. You can use the output=markdown parameter to obtain the output in markdown format when the response content-type is text/html.


Proxy Mode
curl
python
node
go
ruby
java
csharp
php

import requests
import urllib.parse
token = "YOUR_TOKEN"
targetUrl = urllib.parse.quote("https://httpbin.co/")
url = "http://api.scrape.do/?token={}&url={}&output=markdown".format(token, targetUrl)
response = requests.request("GET", url)
print(response.text)
Downloading Pictures & Files
You don't need any extra configuration to download pictures or files. Just send a request with the target URL and get the result.

There is a 4MB response body limit per request in our system. With super proxies, this limit is 2MB.


Proxy Mode
curl
python
node
go
ruby
java
csharp
php

import requests
import urllib.parse
token = "YOUR_TOKEN"
targetUrl =  urllib.parse.quote("https://httpbin.co/image")
url = "http://api.scrape.do/?token={}&url={}".format(token, targetUrl)
response = requests.request("GET", url)
print(response.text)
Transparent Response
By default, Scrape.do returns status codes specified by our system. However, in some cases, you may want to use the exact status codes that the target web page returns.

In such cases, simply pass the transparentResponse=true parameter.


Proxy Mode
curl
python
node
go
ruby
java
csharp
php

import requests
import urllib.parse
token = "YOUR_TOKEN"
targetUrl = urllib.parse.quote("https://httpbin.co/anything")
transparentResponse = "true"
url = "http://api.scrape.do/?token={}&url={}&transparentResponse={}".format(token, targetUrl,transparentResponse)
response = requests.request("GET", url)
print(response.text)
Response Headers
By default, Scrape.do will return all the header information it receives from the target website. Our system also aims to make your work easier by adding the following header parameters to the response.

Header	Description
Scrape.do-Cookies	All cookie information returned from the target web page, joined with ';' and returned in one header
Scrape.do-Remaining-Credits	Total credits remaining in your subscription
Scrape.do-Request-Cost	Credits consumed by this specific request. This can differ from the base 1 / 5 / 10 / 25 table because some target domains have super and/or render applied by default server-side. See Request Costs for the per-domain pricing table.
Scrape.do-Resolved-Url	The final URL after following redirects. Useful for tracking where requests end up
Scrape.do-Target-Url	The original URL of the target web page you requested
Scrape.do-Initial-Status-Code	The first response status code received from the target website. In responses with redirects, this will show the initial 30X code
Scrape.do-Target-Redirected-Location	When disableRedirection=true, this shows the Location header from the target website's redirect response
Reading Scrape.do-Request-Cost. This header is the authoritative source for what a call actually cost. Always read it on each response if you're tracking spend programmatically, since the cost may differ from the baseline of the parameters you sent (Scrape.do applies default super / render profiles on certain target domains, see Request Costs for the full list).

Pure Cookies
When scraping websites, you may need to process cookies in their original format. By default, Scrape.do returns cookies in a special header called Scrape.do-Cookies. However, if you need to access the original Set-Cookie headers returned by the target website, you can enable the pureCookies parameter.

When set to pureCookies=true, this parameter returns the original Set-Cookie headers from the target website instead of the processed Scrape.do-Cookies format.


Proxy Mode
curl
python
node
go
ruby
java
csharp
php

import requests
import urllib.parse
token = "YOUR_TOKEN"
targetUrl = urllib.parse.quote("https://www.instagram.com/api/v1/users/web_profile_info/?username=google")
url = "http://api.scrape.do/?token={}&url={}&pureCookies=true".format(token, targetUrl)
response = requests.request("GET", url)
for key, value in response.headers.items():
    print(f"{key}: {value}")
Example Result
Pure Cookies Response

Sticky Sessions

Session based scraping

How to Solve Blocking Issues

Next Page

On this page
Output Format
Downloading Pictures & Files
Transparent Response
Response Headers
Pure Cookies
Example Result
Output & Response | Documentation | Scrape.do

logoSearch
Ctrl
K
Getting Started
Request Costs
Proxy Settings
Super (Residential & Mobile)
Geo Targeting
Regional Geo Targeting
Postal Code (ZIP Code) Targeting
API & Response
POST/PUT Request
Timeout
Retry Settings
Disable Redirection
Device
Sticky Sessions
Output & Response
How to Solve Blocking Issues
Status Codes
Usage Statistics
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


API & Response
How to Solve Blocking Issues
View as Markdown
You've sent a few requests to your target site, and we've explained below what you can do when you get blocked and no successful response. If you have not achieved a result even though you have done what is described here, please contact support and let us know. Rest assured that we will get back to you about the problem as soon as possible.

Use Super Proxy and Geo Targeting

You can use our high quality residential and mobile proxy pools with the super=true parameter, and you can make a request through the country served by the target web page by choosing the country via geoCode=us. For other countries, you can check the Geo Targeting section.
Use Headless Browser

By using our headless browser network with the render=true parameter, you can access the target website with a real browser and retrieve the results.
If you are blocked despite using Headless Browser, you can try again by adding the blockResources=false parameter.
If there is still no successful result, you can make the browser wait on the relevant page for 2 seconds with customWait=2000. By increasing this time, you can customize it according to the needs of the target website.
If there is no expected content in the successful return result, you can wait for a specific element with the Wait Selector feature.
Contact Support

If you have done all the steps above and still have no success, please contact support and let us know. We will check your requests and get back to you as soon as possible.
Output & Response

Customize response

Status Codes

Next Page

How to Solve Blocking Issues | Documentation | Scrape.do

logoSearch
Ctrl
K
Getting Started
Request Costs
Proxy Settings
Super (Residential & Mobile)
Geo Targeting
Regional Geo Targeting
Postal Code (ZIP Code) Targeting
API & Response
POST/PUT Request
Timeout
Retry Settings
Disable Redirection
Device
Sticky Sessions
Output & Response
How to Solve Blocking Issues
Status Codes
Usage Statistics
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


API & Response
Status Codes
View as Markdown
You can see the list of default response status codes and credit usage status used by Scrape.do in the return type below.

Status Code	Description	Consumes Credit
2xx	Successful API call	YES
404	Target not found	YES
429	You are sending requests too quickly (concurrency limit exceeded)	NO
401	You have no credits or your subscription has been suspended	NO
400	Bad request for Scrape.do	NO
400	Bad request for the target website	YES
502	Request has failed. Please try again	NO
510	The request was canceled by the HTTP client. You can see the status code in the dashboard logs	NO
Please note that when you use transparentResponse=true you will get status codes returned by the target website. If there is a problem caused by the proxy, our system may return 502 status code in addition to the target web page.

Authentication Throttling: Repeated requests with an invalid token may result in temporary IP-level throttling by the authentication server. If your IP is throttled, you will receive the message: "Your request has been temporarily throttled by the authentication server." Ensure your token is correct and wait before retrying.

How to Solve Blocking Issues

Previous Page

Usage Statistics

Next Page

Status Codes | Documentation | Scrape.do

logoSearch
Ctrl
K
Getting Started
Request Costs
Proxy Settings
Super (Residential & Mobile)
Geo Targeting
Regional Geo Targeting
Postal Code (ZIP Code) Targeting
API & Response
POST/PUT Request
Timeout
Retry Settings
Disable Redirection
Device
Sticky Sessions
Output & Response
How to Solve Blocking Issues
Status Codes
Usage Statistics
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


API & Response
Usage Statistics
View as Markdown
If you want to know usage statistics for your Scrape.do subscription, you can use the following API endpoint:


https://api.scrape.do/info?token=API_TOKEN
As part of security measures, you can send a maximum of 10 requests per minute to this end-point. When you exceed this limit, you will receive 429 status code.

Result:


{
  "IsActive": true, // Subscription status
  "ConcurrentRequest": 40, // Number of concurrent requests
  "MaxMonthlyRequest": 3500000, // Maximum number of requests per month
  "RemainingConcurrentRequest": 15, // Remaining number of concurrent requests
  "RemainingMonthlyRequest": 2565023, // Remaining number of requests per month
}
Status Codes

Previous Page

Headers & Cookies

Customize HTTP headers and manage cookies

Usage Statistics | Documentation | Scrape.do

logoSearch
Ctrl
K
Getting Started
Request Costs
Proxy Settings
Super (Residential & Mobile)
Geo Targeting
Regional Geo Targeting
Postal Code (ZIP Code) Targeting
API & Response
POST/PUT Request
Timeout
Retry Settings
Disable Redirection
Device
Sticky Sessions
Output & Response
How to Solve Blocking Issues
Status Codes
Usage Statistics
Headers & Cookies
Custom Headers
Extra Headers
Forward Headers
Set Cookies
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


Headers & Cookies
View as Markdown
Customize HTTP headers and manage cookies

Overview
HTTP headers and cookies are critical components for successful web scraping. Modern websites use headers to identify legitimate traffic and cookies to maintain session state. Scrape.do provides three distinct approaches to header management, each suited for different use cases.

Header Management Strategies
Custom Headers — Gives you complete control over all headers sent to the target website. Use this when you need to replicate specific browser behavior or handle complex authentication flows.

Extra Headers — Allows you to add specific headers on top of Scrape.do's automatically generated ones. This is ideal when you need to include one or two custom headers (like API keys or tracking IDs) without disrupting the optimized header set.

Forward Headers — Strips away all auto-generated headers and forwards only what you explicitly provide. Perfect for scenarios where you're working with APIs or need minimal header overhead.

Cookie Management
Set Cookies — Maintain session state across multiple requests. Use the setCookies parameter to pass authentication cookies, session tokens, or any other cookie-based data required by your target website.
Usage Statistics

Previous Page

Custom Headers

Take full control of request headers

On this page
Overview
Header Management Strategies
Cookie Management
Headers & Cookies | Documentation | Scrape.do