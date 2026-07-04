# School of Recycling — Curriculum Intelligence API

Machine-readable curriculum data for [School of Recycling](https://schoolofrecycling.com) (SoR), a K-12 online waste and plastic education platform operated by SoR LLC.

Built for two primary consumers:

1. **AI agents** — querying curriculum content (e.g. "find a plastic waste lesson for 11-year-olds aligned with SDG 12")
2. **School procurement systems** — evaluating whether SoR content fits their curriculum needs

---

## Quick start

```bash
cd sor-api
pip install -r requirements.txt
uvicorn main:app --reload
```

API: http://localhost:8000  
Docs: http://localhost:8000/docs

---

## Access model

| Endpoint type | Auth required | Header |
|---|---|---|
| Public | No | — |
| Gated | Yes | `X-API-Key: <your-key>` |

### Requesting an API key

```bash
curl -X POST http://localhost:8000/request-access \
  -H "Content-Type: application/json" \
  -d '{"email": "you@school.edu", "organisation": "Springfield Elementary"}'
```

SoR reviews all requests manually. Typical response time: 2–3 business days. Keys are stored as SHA-256 hashes in the SQLite database.

For local testing, set `SOR_MASTER_KEY` as an environment variable — this key bypasses the database check.

```bash
export SOR_MASTER_KEY=my-local-test-key
```

---

## Endpoints

### Public — no authentication required

#### `GET /about`
Machine-readable SoR organisation profile including memberships, SDGs, and API metadata.

```bash
curl http://localhost:8000/about
```

#### `GET /lessons`
List all lessons. Filterable by query parameters.

| Param | Values | Example |
|---|---|---|
| `age_group` | `6-9`, `10-12`, `13-16`, `17+` | `?age_group=10-12` |
| `waste_stream` | `plastic`, `organic`, `e-waste`, `textile` | `?waste_stream=plastic` |
| `sdg` | SDG number | `?sdg=12` |
| `availability` | `available`, `coming_soon` | `?availability=available` |
| `is_free` | `true`, `false` | `?is_free=true` |
| `audience` | `home_learner`, `classroom` | `?audience=classroom` |

```bash
# All available plastic lessons for ages 10-12
curl "http://localhost:8000/lessons?age_group=10-12&waste_stream=plastic&availability=available"

# Free lessons only
curl "http://localhost:8000/lessons?is_free=true"

# Lessons aligned with SDG 14 (Life Below Water)
curl "http://localhost:8000/lessons?sdg=14"
```

#### `GET /lessons/:id`
Public metadata for a single lesson (no learning outcomes or full description).

```bash
curl http://localhost:8000/lessons/plastic-m1-10-12
```

#### `GET /search?q=`
Keyword search across title, description, and topic tags.

```bash
curl "http://localhost:8000/search?q=ocean+plastic"
curl "http://localhost:8000/search?q=circular+economy"
curl "http://localhost:8000/search?q=SDG+12"
```

#### `GET /sdgs`
All SDGs covered and which lessons map to each.

```bash
curl http://localhost:8000/sdgs
```

#### `GET /age-groups`
All age groups with availability status and lesson counts.

```bash
curl http://localhost:8000/age-groups
```

#### `GET /waste-streams`
All waste streams covered with availability status.

```bash
curl http://localhost:8000/waste-streams
```

---

### Gated — `X-API-Key` header required

#### `GET /lessons/:id/full`
Full lesson detail: learning outcomes, full description, worksheet descriptions, discussion prompts.

```bash
curl http://localhost:8000/lessons/plastic-m1-10-12/full \
  -H "X-API-Key: my-local-test-key"
```

#### `GET /lessons?full=true`
Full detail for all results (same filter params as public `/lessons`).

```bash
curl "http://localhost:8000/lessons?age_group=13-16&full=true" \
  -H "X-API-Key: my-local-test-key"
```

---

## Data model

```
Lesson
├── id                         string        e.g. "plastic-m1-10-12"
├── title                      string
├── description                string        public short summary
├── full_description           string        gated — detailed module description
├── age_group                  string        "6-9" | "10-12" | "13-16" | "17+"
├── availability               string        "available" | "coming_soon"
├── edition                    string        "home" | "classroom" | "both"
├── price_home_usd             integer       37
├── price_classroom_usd        integer       147
├── waste_stream               string        "plastic" | "organic" | "e-waste" | "textile"
├── topic_tags                 string[]      e.g. ["ocean plastic", "circular economy"]
├── learning_outcomes          string[]      gated
├── pedagogical_approach       string        "systems thinking" | "critical inquiry" | "real-world trade-offs"
├── content_types              string[]      "video" | "worksheet" | "discussion_prompt" | "reflection" | "activity"
├── sdg_alignment              integer[]     e.g. [4, 12, 14]
├── language                   string        "en" (v1 only)
├── duration_per_module_minutes integer
├── duration_total_minutes     integer       (5 modules × per_module)
├── audience                   string        "home_learner" | "classroom" | "both"
├── url                        string        direct link to schoolofrecycling.com course page
├── is_free                    boolean       true for Module 1 globally
├── credential_context         string[]      ["UNEP GPML member", "UN Global Compact"]
├── worksheet_descriptions     string[]      gated
└── discussion_prompts         string[]      gated
```

---

## Seed data (v1)

Plastic course seeded for two age groups (10–12 and 13–16), five modules each:

| Module | Topic |
|---|---|
| 1 | The Plastic Story — origins, fossil fuels, polymer chemistry (`is_free: true`) |
| 2 | Plastic Types & Recyclability — resin codes, contamination, greenwashing |
| 3 | Waste Systems & Infrastructure — MRFs, waste trade, China National Sword |
| 4 | Ocean Plastic & Ecosystems — microplastics, food webs, cleanup tech |
| 5 | Circular Economy & Trade-offs — real-world limits of circular solutions |

Two coming-soon stubs: ages 6–9 and 17+.

---

## Deployment to Render

1. Fork / push this repo to GitHub.
2. In the [Render dashboard](https://render.com), click **New → Web Service**.
3. Connect your GitHub repo and point Render to `sor-api/` as the root directory.
4. Render will auto-detect `render.yaml`. The config:
   - Sets `DB_PATH` to `/data/sor.db` on a persistent 1 GB disk
   - Auto-generates `SOR_MASTER_KEY` as a secret env var
5. Copy the generated `SOR_MASTER_KEY` from Render's environment tab — that's your admin key.

The database is seeded automatically on first startup via the `startup` event handler.

---

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `DB_PATH` | `sor.db` | Path to SQLite database file |
| `SOR_MASTER_KEY` | `""` | Admin API key that bypasses DB check (set in production) |
| `ANTHROPIC_API_KEY` | `""` | Used to classify inbound Instantly replies (see below) |
| `SYSTEME_IO_API_KEY` | `""` | systeme.io public API key (Profile → Public API keys) |
| `INSTANTLY_WEBHOOK_SECRET` | `""` | Shared secret checked on `/webhooks/instantly-reply` — leave blank only while testing |

---

## Reply-to-course automation

Turns Instantly cold-email replies into free Module 1 access + nurture-sequence enrolment in systeme.io, with zero manual work.

**Flow:** Instantly reply → webhook → Claude classifies the reply → matching systeme.io contact tag → a systeme.io automation rule (built once, no-code) sends the age-appropriate Module 1 and enrols the contact in the 3-email nurture sequence.

The campaign (3 emails to 30 inboxes, ~13k sends) asks "which age group do you teach?" and offers free Module 1 in return. A reply of "September" gets tagged for a later follow-up instead.

### Multi-language replies

This campaign goes out to multiple countries, so replies come back in whatever language the recipient writes in — not necessarily the language the campaign itself was sent in. The classifier (Claude) reads and reasons about each reply in its original language rather than matching English keywords, and converts whatever schooling-system term is used (grade, class, year, form, etc.) to the closest age band using that country's own age/grade conventions, not US grade norms. "Ambiguous in this reply's country/language" still falls back to `unclear` rather than guessing.

Each classified reply also gets an ISO 639-1 language code logged (`GET /automation/log`, and a "Replies by language" breakdown on the dashboard) so you can see which languages/countries are actually replying and spot-check accuracy per language.

One thing this does **not** do: localize the Module 1 emails or nurture sequence themselves — that's whatever content the systeme.io workflow behind each tag sends. If you want different email copy per language, you'd need per-language tags (e.g. `module1-10-12-fr`) and workflows; the current setup sends the same (language of your systeme.io workflow) content regardless of the reply's language. Say the word if you want that split out.

### 1. Configure env vars

Set `ANTHROPIC_API_KEY`, `SYSTEME_IO_API_KEY`, and `INSTANTLY_WEBHOOK_SECRET` (pick any random string for the secret) in Render's environment tab.

### 2. Build the systeme.io automation rules (one-time, manual — systeme.io automations are no-code)

Use an **Automation Rule**, not a Workflow — this is a plain "tag added → do things" action with no delays or branching, which is exactly what Rules are for (Workflows are the visual multi-step builder for when the trigger logic itself needs conditions).

Only **4 tags** are needed — currency doesn't get its own tag, because the class licence (age-specific) and school licence (currency-specific only) checkout pages differ on two independent axes that a single tag/rule can't cleanly combine (12 tags would've been needed otherwise, and systeme.io's multi-trigger rules are OR, not AND, so they can't combine two tags into one condition either). Instead, currency is written straight onto the contact as custom fields that the (unchanged) age-specific nurture emails read via merge tags.

**4 age tags** — trigger = "Tag added" with that tag, actions = "Enroll in course" (that age's Module 1, Access type = Partial access) + "Subscribe to campaign" (that age's nurture sequence).

| Tag (must match exactly, case-sensitive) | Fires when |
|---|---|
| `Module-1 Free (6-9yr)` | Ages 6–9 |
| `Module-1 Free (10-12yr)` | Ages 10–12 |
| `Module-1 Free (13-16yr)` | Ages 13–16 |
| `Module-1 Free (17+yr)` | Ages 17+ |

Plus the September tag, unchanged:

| `Sept26-FollowUp` | Reply says "September" / asks to be followed up later |

**In each of the 4 nurture campaigns' emails**, insert the checkout link using systeme.io's merge tags instead of a hardcoded URL:
- `{checkout_link_class}` — the class-licence checkout page for that contact's age + currency
- `{checkout_link_school}` — the school-licence checkout page for that contact's currency (not age-specific)

Both custom fields (`checkout_link_class`, `checkout_link_school`) must exist under Contacts → Settings before this works — confirmed already created.

`sor-api/email_automation.py`'s `MODULE1_AGE_TAGS` holds the 4 tag names, and `CHECKOUT_LINKS_CLASS` / `CHECKOUT_LINKS_SCHOOL` hold the 12 + 3 checkout URLs — update those if any tag names or URLs change.

### Currency routing

Each lead's currency is derived from their country, not from anything in the reply text:

1. The webhook payload is searched for a country field — tries `Person Country`, `country`, `personCountry`, `lead country` (case/spacing-insensitive), both at the top level and inside common nested containers (`variables`, `custom_variables`, `lead_data`, `custom_fields`). **The exact field name Instantly uses for your "Person Country" CSV column wasn't verifiable against live docs while this was built** — same blind spot as the systeme.io API before. Check a real reply's `raw_payload` in `/automation/log` and adjust `COUNTRY_FIELD_CANDIDATES` in `email_automation.py` if it guessed wrong.
2. Country → currency: United Kingdom → GBP, EU member states → EUR, everything else (including non-EU Europe like Switzerland/Norway) → USD. Change `EU_COUNTRIES`/`UK_NAMES`/`currency_for_country()` if that's not the split you want.
3. If no country field can be found at all, the age tag is still applied (the lead gets free Module 1 access right away) but the two checkout-link custom fields are left unset — logged as `action = tagged_module1_currency_pending`, visible on the dashboard under "Needs currency review", so the checkout links can be filled in manually without blocking course access. Sending a wrong-currency (or blank) checkout link is worse than a short delay, so this never guesses.
4. **The exact systeme.io request shape for setting a contact's custom fields (`_set_custom_fields` in `email_automation.py`) is also unverified against live docs** — same pattern as everywhere else in this integration. If it errors, `/automation/log`'s error column will show systeme.io's real response body (per the diagnostic fix earlier), which will say exactly what shape it actually expects.

Tags don't need to exist beforehand — the automation creates them via the API on first use if missing. But the *rule* behind each tag must exist in systeme.io before that tag's first real reply comes in, or the tag gets applied with no action taken.

### 3. Point Instantly at the webhook

In Instantly: **Settings → Integrations → Webhooks** (or via API v2 `POST /api/v2/webhook`) → create a webhook for the `reply_received` event, URL `https://<your-render-url>/webhooks/instantly-reply`. If Instantly's webhook UI lets you set a custom header or secret token, set it to match `INSTANTLY_WEBHOOK_SECRET` — check [developer.instantly.ai/api/v2/webhook/createwebhook](https://developer.instantly.ai/api/v2/webhook/createwebhook) for the exact field, since this wasn't verified live while building. Replies to `auto_reply_received` (out-of-office etc.) are a separate event type and won't hit this webhook.

### 4. Watch it

`https://<your-render-url>/dashboard?key=<your SOR_MASTER_KEY>` — live counts of replies processed, Module 1 sends by age group, September follow-ups, and anything the classifier punted to "needs review" or that errored. Auto-refreshes every 30s. Bookmark it with the key in the URL.

### Endpoints

| Endpoint | Auth | Purpose |
|---|---|---|
| `POST /webhooks/instantly-reply` | webhook secret | Receives Instantly's `reply_received` events |
| `GET /automation/log?action=&limit=` | `X-API-Key` | Raw event log, filterable by `action` (`tagged_module1`, `tagged_september`, `logged_not_interested`, `logged_unclear`, `error`) |
| `GET /automation/stats` | `X-API-Key` | Aggregate counts for the dashboard |
| `GET /dashboard?key=` | query-param key | HTML dashboard |

### Go-live checklist

The systeme.io request/response shapes in `email_automation.py` (`_create_contact`, `_find_contact_id_by_email`, `_get_or_create_tag_id`) are based on their publicly documented API but weren't tested against a live key while building this — their docs site returned 403 to the automated fetch used during development. Before sending real campaign traffic:

1. Send one test webhook payload (`curl -X POST .../webhooks/instantly-reply -d '{"event_type":"reply_received","lead_email":"you@test.com","reply_text":"I teach 5th grade","campaign_id":"test"}'`) and confirm in systeme.io that a contact was created and tagged `module1-10-12`.
2. Reply again from the same test address to confirm the dedupe check stops it from double-tagging.
3. Check `GET /automation/log` for the resulting row and confirm `error` is empty.
4. If `_find_contact_id_by_email` 404s or the response shape doesn't match (systeme.io's "look up contact by email" support was, as of writing, still on their public roadmap rather than confirmed-shipped), replies from people who are already systeme.io contacts will log an `error` instead of tagging — check for that pattern in `/automation/log?action=error` early on and patch the lookup call if needed.

---

## Approving API keys

Access requests are logged to the `api_keys` table with `status = 'pending'`. To approve a key manually:

1. Generate a secure random key (e.g. `openssl rand -hex 32`)
2. Hash it: `python -c "import hashlib; print(hashlib.sha256(b'the-key').hexdigest())"`
3. Update the DB: `UPDATE api_keys SET key_hash = '<hash>', status = 'approved' WHERE id = <id>;`
4. Send the raw key to the requestor.

---

## Schema.org JSON-LD

See `schema_org_jsonld.json` for a JSON-LD snippet (`Organization` type) for embedding in the SoR website. It includes:
- UNEP GPML and UN Global Compact membership
- `subjectOf` pointing to this API
- Course listings with SDG `educationalAlignment`

Embed in the `<head>` of schoolofrecycling.com:

```html
<script type="application/ld+json">
  <!-- contents of schema_org_jsonld.json -->
</script>
```
