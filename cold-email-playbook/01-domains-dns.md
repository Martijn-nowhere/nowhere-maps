# Step 1 — Domains & DNS

## Domain Strategy

Never send cold emails from your brand domain. Use separate sending domains.

| Domain type | Purpose | Example |
|-------------|---------|---------|
| Brand domain | Website, main email | schoolofrecycling.com |
| Sending domain 1 | Cold outreach | schoolofrecycling.org |
| Sending domain 2 | Cold outreach | schoolofrecycling.co |

Buy sending domains on GoDaddy. Use .org, .co, .io, .net — avoid .com for sending.

## DNS Records to Add

Add these records in GoDaddy for each sending domain.

### MX Records (Google Workspace)
| Type | Name | Value | Priority |
|------|------|-------|----------|
| MX | @ | ASPMX.L.GOOGLE.COM | 1 |
| MX | @ | ALT1.ASPMX.L.GOOGLE.COM | 5 |
| MX | @ | ALT2.ASPMX.L.GOOGLE.COM | 5 |
| MX | @ | ALT3.ASPMX.L.GOOGLE.COM | 10 |
| MX | @ | ALT4.ASPMX.L.GOOGLE.COM | 10 |

### SPF Record
| Type | Name | Value |
|------|------|-------|
| TXT | @ | v=spf1 include:_spf.google.com ~all |

### DKIM Record
Generated in Google Workspace Admin → Apps → Gmail → Authenticate email.
| Type | Name | Value |
|------|------|-------|
| TXT | google._domainkey | (generated key from Google) |

### DMARC Record
| Type | Name | Value |
|------|------|-------|
| TXT | _dmarc | v=DMARC1; p=quarantine; rua=mailto:client@theirdomain.com |

## Domain Forwarding
Set up 301 redirect in GoDaddy to forward sending domains to brand website.
- schoolofrecycling.org → https://www.schoolofrecycling.com
- schoolofrecycling.co → https://www.schoolofrecycling.com

## Verification
Use dnschecker.org to confirm all records have propagated globally.
Check DMARC reports — Google sends them daily to the rua email address.
