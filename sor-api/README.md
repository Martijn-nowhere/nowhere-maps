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
