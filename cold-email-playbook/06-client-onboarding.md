# Step 6 — Client Onboarding

## What You Need from the Client Before Starting

- [ ] Brand domain name (e.g. clientbrand.com)
- [ ] Access to their domain registrar (GoDaddy or other) — OR permission to add DNS records yourself
- [ ] Their main email address (for Reply-To and DMARC reports)
- [ ] Preferred sending name style (generic first names + brand abbreviation as last name)
- [ ] Credit card for tool subscriptions (or agree to bill separately)
- [ ] Brief on their offer: what are they selling, who is the target, what's the CTA

## DNS Access Options

**Option A — Client does it**
You send exact records (copy-paste from `01-domains-dns.md`). They add in GoDaddy.
- Slower (back and forth)
- GoDaddy sends SMS verification to their phone for each change
- Good if client prefers to keep control

**Option B — You get added as admin**
Client adds you as a GoDaddy delegate user.
- Faster
- You still trigger their SMS verification on changes
- Ask them to be available on phone/WhatsApp during DNS setup session (30 min)

**Option C — You handle everything**
Buy the sending domains on your own GoDaddy account.
- Fastest
- You control DNS fully, no SMS friction
- Add client credit card to the account for billing, or invoice them separately
- Risk: if relationship ends, you own the domains

Recommendation: Option B for most clients. Option C for high-volume recurring clients.

## Domain Purchasing

Buy sending domains yourself on GoDaddy to avoid back-and-forth.

Naming convention: same brand, different extension.
- Brand: clientbrand.com
- Sending 1: clientbrand.org
- Sending 2: clientbrand.co

Cost: ~$12–25/year per domain on GoDaddy. Invoice to client.

Avoid .com for sending domains — higher scrutiny, worse inbox rates.

## Tool Setup Checklist

| Tool | Who owns the account | Billing |
|------|---------------------|---------|
| GoDaddy (sending domains) | You or client | Client pays |
| Google Workspace (sending mailboxes) | New account, separate from client's existing Workspace | Client pays |
| Instantly | You (agency account) or new client account | Client pays |
| Apollo | You (agency) or client | Client pays |

**Important:** Always create a separate Google Workspace account for sending — never add sending domains to the client's existing Workspace. Plan mismatch causes pricing issues (Business Starter vs Standard).

## Payments

**Your GoDaddy account:** Add client credit card directly in GoDaddy under Payment Methods, or use your card and invoice the client.

**Google Workspace:** Create the Workspace with client's card. Use "Email for sign-in instructions" field during user creation — set to client's main email so all passwords arrive in one inbox.

**Instantly:** Client creates their own account, or you manage under an agency seat.

**Invoicing recommendation:** Charge a setup fee (one-off) + monthly retainer that covers all tools and management. Example pricing:

| | Cost |
|-|------|
| Setup fee (one-off) | €500–1,000 |
| Monthly management | €300–500/month |
| Tools pass-through | ~€200/month at cost |

## Passwords & Security

- Save all generated passwords before closing each account creation screen
- Use a password manager (Bitwarden, 1Password) per client
- Never reuse passwords across client accounts
- When handing over: export password file, transfer account ownership

## What to Hand Over at End of Engagement

- All domain login credentials
- Google Workspace admin access
- Instantly account access
- Apollo account access
- CSV of all leads used
- Warmup score screenshots
- DMARC report summary

## Communication Template (first contact)

> Hi [name],
>
> To get started I need a few things from you:
>
> 1. Your main email address (for reply routing)
> 2. Access to your domain registrar for 30 minutes (I'll tell you exactly which records to add)
> 3. A credit card to set up the tool subscriptions (~€200/month)
>
> Once those are in place I can have everything running within a week. Warmup takes 4–5 weeks, then we launch.
>
> Let me know when works for a quick call.
