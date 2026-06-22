# Step 3 — Instantly Setup

## Account & Plan

Sign up at instantly.ai. Use **Hyper Growth** plan ($97/month) — required for:
- Unlimited warmup
- Unlimited active leads
- Advanced campaign analytics

## Connect Mailboxes via OAuth

Do NOT use CSV/IMAP method — Google blocks app passwords and returns 422 errors.

1. Instantly → Settings → Mailboxes → Add mailbox → Google
2. Log in with each account individually
3. Repeat for all 10 accounts

The OAuth setup in Google Admin (Step 2) authorizes access. You still add each account one at a time here.

## Warmup Settings (per mailbox)

Instantly → Settings → Mailboxes → select account → Warmup tab

| Setting | Value |
|---------|-------|
| Warmup enabled | On |
| Daily warmup limit | 30 |
| Reply rate | 30% |
| Mark important | On |
| Warmup tag | warmup |

Apply same settings to all 10 accounts.

**Important:** Health score (100% = correctly configured) is different from warmup score (builds over 4-6 weeks). Health score hitting 100% on day 1 is normal — it just means DNS is set up correctly. The warmup score is what matters for deliverability.

## Warmup Timeline

| Week | Expected warmup score |
|------|-----------------------|
| Week 1 | 10–20 |
| Week 2 | 30–50 |
| Week 3 | 50–70 |
| Week 4–5 | 70–85 |
| Week 5–6 | 85+ (launch ready) |

Do not launch campaign until all accounts hit 85+. Monitor daily.

If accounts get flagged (warmup disabled popup): request reactivation code in Instantly. Codes are sent to the mailbox itself — since these are Google accounts that actually receive email, codes will arrive. Enter code to reactivate.

## Create Campaign

Instantly → Campaigns → New Campaign

### Campaign Settings

| Setting | Value |
|---------|-------|
| Campaign name | Wave 1A — [Country/Region] |
| From accounts | All 10 mailboxes (rotate) |
| Daily sending limit | 15 per mailbox (150/day total) |
| Stop on reply | On |
| Stop on auto-reply | On |
| Track opens | Off (hurts deliverability) |
| Track clicks | Off (no links anyway) |

### Schedule Settings

| Setting | Value |
|---------|-------|
| Timezone | Recipient's timezone (or Central European Time) |
| Send days | Monday–Thursday |
| Send time | 08:00–11:00 |
| Send window | 3 hours |

Avoid Friday and weekends. Teachers read email in the morning.

### Sequence Structure

3 emails. Delays between:
- Email 1 → Email 2: 3 days
- Email 2 → Email 3: 4 days

Total sequence: ~8 days per lead.

## Upload Leads

Instantly → Campaigns → select campaign → Leads → Import CSV

CSV must have columns: `firstName`, `lastName`, `email`, `companyName`

Map columns on import. Instantly auto-deduplicates against previous campaigns if you enable global deduplication in settings.

## Variables

| Variable | Source |
|----------|--------|
| `{{firstName}}` | Lead's first name from CSV |
| `{{companyName}}` | School name from CSV |
| `{{senderFirstName}}` | Sending account's first name (auto) |

## Tokens

Tokens in Instantly = email verification credits. Not needed if using Apollo Verified filter — those leads are already verified. Do not spend tokens re-verifying Apollo Verified exports.

## Launch Checklist

- [ ] All 10 accounts warmup score 85+
- [ ] DNS health 100% on all accounts
- [ ] Leads uploaded and mapped
- [ ] Sequence copy added (all 3 emails)
- [ ] Schedule set to Mon–Thu 08:00–11:00
- [ ] Stop on reply = On
- [ ] Campaign start date set
- [ ] Test email sent from each sending domain (check inbox placement manually)
