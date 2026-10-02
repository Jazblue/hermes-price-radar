# Jina Reader / Structured-Data Test — Argos ASUS Laptop URLs

Date: 2026-10-03
Method: Jina Reader (https://r.jina.ai/) + direct HTTP baseline. No Playwright.
Status: FAILED — Argos blocks all automated access. Stopped per instruction; no bypass attempted.

## Test cases

| # | Product | Source URL | Fetch | Price extracted | Title found | JSON-LD | Verification |
|---|---------|-----------|-------|-----------------|-------------|----------|--------------|
| 1 | ASUS Vivobook AI 16in Ryzen 5 16GB 512GB Laptop - Blue | https://www.argos.co.uk/product/7741159 | NO (403) | NO | none | none | UNVERIFIED |
| 2 | ASUS Vivobook M160 16in R5 16GB 512GB Laptop - Silver | https://www.argos.co.uk/product/7761225 | NO (403) | NO | none | none | UNVERIFIED |

## Evidence

### Jina Reader — product 7741159 (3 attempts)
Command: `curl -s "https://r.jina.ai/https://www.argos.co.uk/product/7741159"`
Jina HTTP status: 200 (Jina itself responded), but returned an error document:

```
Title: Access Denied
URL Source: https://www.argos.co.uk/product/7741159
Warning: Target URL returned error 403: Forbidden
You don't have permission to access "http://www.argos.co.uk/product/7741159" on this server.
Reference #18.a8c83017.1790982640.7bab177d
```

### Jina Reader — product 7761225
Identical result: `Title: Access Denied` / `Target URL returned error 403: Forbidden`
Reference #18.abc84d17.1790982643.44da1b7

### Direct HTTP baseline (confirm the block is Argos-side, not a Jina artefact)
Command: `curl -H "User-Agent: <desktop Chrome UA>" https://www.argos.co.uk/product/<id>`
- 7741159 -> HTTP 403
- 7761225 -> HTTP 403

Note: on the 7761225 run curl also exited 23 (write error from `-o /dev/null` under the
MSYS shell); the HTTP code above is the value that matters and matches the other probes.

## Conclusion

The 403 originates at Argos's edge (Akamai — `errors.edgesuite.net` reference IDs), not at
Jina. Jina Reader is fetching on our behalf and Argos refuses the request. Because Jina
returns 200 with an error document, any scraper must parse the body for
`Access Denied` / `Target URL returned error` and treat it as a failure — a naive HTTP-status
check would record a false success.

Argos cannot be price-verified by any read-only HTTP reader (Jina Reader included) or by
headless Chrome. Do not pursue header rotation, proxy rotation, CAPTCHA solving, or similar
evasion — that is bot-protection bypass and out of scope for this skill.

## Consequence for price-radar

`data/products.json` currently holds `£549.00` for both products, retailer Argos, marked
"In stock", last checked 2026-10-02T14:58:36Z. That value could not be re-verified and
should not be presented as current on the website or in Google Sheets. Both entries
remain UNVERIFIED pending a data source that Argos does not block.