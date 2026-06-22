# Step 4 — Apollo & LeadMash Lead Building

## Strategy

Apollo.io finds leads. LeadMash exports them cheaply without burning Apollo credits.

Apollo credits cost $49/month (startup plan) and deplete fast at scale. LeadMash scrapes the same Apollo search URL for $6 per 1,000 leads. Use LeadMash for all bulk exports.

## Apollo Search Setup

Go to apollo.io → Search → People

### Filters

| Filter | Value |
|--------|-------|
| Job Title | English Teacher, Teacher of English, Head of English, Curriculum Manager |
| Location | Target countries (see waves below) |
| Industry | Primary/Secondary Education, Education Management |
| Employee count | 11–200 (schools, not universities) |
| Email status | **Verified** |

**Important:** Always use Verified email filter. Unverified leads have high bounce rates that damage sender reputation. Do not run through additional verifiers (MillionVerifier etc.) — Apollo Verified is sufficient.

### Job Title Notes

- "English Teacher" alone is the cleanest filter — highest volume, most relevant
- "Head of English" and "Head of Department" increase volume but also include non-English departments
- "Curriculum Manager" adds smaller volume but decision-maker level
- Test combinations and check result count before exporting

### Lead Volume Guidelines

| Countries | Expected verified leads |
|-----------|------------------------|
| 1 country (large, e.g. DE) | 300–600 |
| Nordics + NL + BE | 800–1,400 |
| Full Wave 1 (+ DE + FR) | 2,000–3,500 |

Remove employee count filter to increase volume if needed (adds university contacts — filter manually after).

## Wave Structure

Run campaigns in waves to manage capacity and vacation windows.

| Wave | Countries | Timing |
|------|-----------|--------|
| Wave 1A | Nordics (NO, SE, DK, FI), NL, BE | July–August |
| Wave 1B | Germany, Austria, Switzerland | September–October |
| Wave 2 | France, Spain, Portugal | October–November |
| Wave 3 | Eastern Europe | November–December |

Avoid campaigns during school holidays. Teachers don't check work email.

## LeadMash Export

1. Build Apollo search and copy the search URL
2. Go to leadmash.io
3. Paste Apollo search URL
4. Select export size (minimum 1,000 — you pay for 1,000 even if you want fewer)
5. Pay $6 per 1,000 leads
6. Receive CSV by email (usually within a few hours)

LeadMash CSV columns: `firstName`, `lastName`, `email`, `companyName`, `title`, `location`

You only need: `firstName`, `lastName`, `email`, `companyName` for Instantly.

## CSV Cleanup (optional but recommended)

Before uploading to Instantly:
1. Remove duplicate emails
2. Remove rows with missing firstName or email
3. Check companyName format — fix obvious issues (all caps, abbreviations)
4. Save as UTF-8 CSV

## Upload to Instantly

See `03-instantly-setup.md` → Upload Leads section.

## Apollo Credits

Apollo credits = used when you reveal/export contact data directly in Apollo.

If you use LeadMash: you never reveal contacts in Apollo → zero credits used.

Keep Apollo credits for spot-checking individual contacts or small targeted searches (e.g. a specific school).

Startup discount: Apollo may offer 50% off if you email their sales team with a startup pitch. Not guaranteed — LeadMash is the reliable cost solution regardless.
