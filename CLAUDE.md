# Nowhere Maps — Reply-to-Course Automation

## Project overview

School of Recycling automated email-reply-to-course enrollment system. Instantly cold-email campaigns → Claude classifies reply → systeme.io tag applied → contact auto-enrolled in free Module 1 + nurture sequence.

**Status**: Production-ready. 28 teacher/age-group campaigns active, ready to send. US school-district curriculum-decision-maker campaigns (2 tracks) built and ready for late-August send; warm-reply routing code is done, systeme.io automation rules for the two district tags still need to be built no-code before go-live.

## Current setup

**Campaigns (active)**: 28 Module 1 campaigns across 2x US, 4x UK, 1x SE, 1x NO, 1x FI, 1x DK, 3x BE, 8x DE, 3x NL, 1x Saudi Arabia, 1x Oman, 1x Qatar, 1x UAE = ~40+ mailboxes, ~13k+ sends planned. Middle East campaigns added after initial send-out (`Saudi-09Aug`, `Oman-13Aug`, `Qatar-16Aug`, `UAE-17Aug`) — note these 4 countries aren't in `EU_COUNTRIES`/`UK_NAMES` so `currency_for_country()` falls back to USD for them (no SAR/OMR/QAR/AED checkout pages exist — only EUR/GBP/USD are supported currencies).

**Campaigns (built, not yet sent)**: 2 US school-district tracks — `US-24Aug-CurriculumDirectors` (Track A, generalist curriculum titles) and `US-25Aug-ScienceSTEMDirectors` (Track B, science/STEM/CTE titles), 4 emails each, targeting 246 districts / ~516 contacts purchased from MCH Strategic Data. Not asking for age group like module1 — asks for a reply to schedule a call; warm replies get tagged in systeme.io to trigger a calendar-booking follow-up sequence instead of a Module 1 enrollment. See "Reply-to-Course Automation" recap for full campaign copy/timing/list details.

**Configuration**:
- Render deployment: `sor-curriculum-api` (standard plan for persistent disk)
- Database: SQLite `/data/sor.db` on persistent 1GB disk
- API keys: `SOR_MASTER_KEY` auto-generated on first deploy
- Webhook secret: `INSTANTLY_WEBHOOK_SECRET` (set in Render environment, use query param `?secret=...` for testing)
- Environment vars: See `sor-api/render.yaml` (ANTHROPIC_API_KEY, SYSTEME_IO_API_KEY, INSTANTLY_WEBHOOK_SECRET, INSTANTLY_MODULE1_CAMPAIGN_IDS, INSTANTLY_SCHOOLS_CAMPAIGN_IDS, INSTANTLY_US_DISTRICTS_CURRICULUM_CAMPAIGN_IDS, INSTANTLY_US_DISTRICTS_SCIENCE_CAMPAIGN_IDS)

**Campaign routing**: 
- Type-based architecture (`campaign_id` → `campaign_type` → handler)
- 24 IDs registered under `module1` type in `INSTANTLY_MODULE1_CAMPAIGN_IDS`
- 1 ID each registered under `us_districts_curriculum` / `us_districts_science` types — sentiment-based classifier (`interested` / `referral` / `not_interested` / `unclear`), only `interested` gets tagged (`us-district-curriculum-reply` / `us-district-science-reply`)
- Unregistered campaigns safely ignored
- See README "Campaign types & routing" section for full architecture & extension guide

## Key files

| File | Purpose |
|---|---|
| `sor-api/email_automation.py` | Webhook endpoint, reply classification, systeme.io integration, dashboard |
| `sor-api/database.py` | SQLite schema, `reply_automation_log` table |
| `sor-api/main.py` | FastAPI app, routes, middleware |
| `sor-api/render.yaml` | Deployment config, env vars, persistent disk |
| `sor-api/requirements.txt` | Python deps (httpx, anthropic, fastapi, etc) |
| `README.md` | Full docs: endpoints, data model, reply automation, campaign types, troubleshooting |

## Recent work (July 2026)

1. **Campaign routing refactored** — split monolithic webhook into type-specific handlers
   - `handle_module1_campaign()` — full implementation (classify, tag, currency routing, checkout links)
   - `handle_schools_campaign()` — stub for August
   - Campaign registry loads from env vars, unregistered campaigns ignored

2. **Render plan upgraded** — free → standard for persistent disk (dashboard data now survives restarts)

3. **24 campaign IDs configured** — all registered in `INITIALLY_MODULE1_CAMPAIGN_IDS`

4. **Webhook tested & working** — tested with `mmmhuizing@hotmail.com`, correctly classified "5th grade" → age 10-12, applied tag, logged to database

5. **Dashboard verified** — live reply count, age/currency/language breakdown, activity log with local timezone rendering

6. **Documentation completed** — README "Campaign types & routing" section covers architecture, adding new types, testing, troubleshooting

7. **US school-district warm-reply routing built** — `us_districts_curriculum` / `us_districts_science` campaign types added: `classify_district_reply()` (new sentiment classifier — `interested`/`referral`/`not_interested`/`unclear`, separate from module1's age-group classifier), `handle_us_district_curriculum_campaign()` / `handle_us_district_science_campaign()` (thin wrappers around shared `_handle_us_district_reply()`), 2 campaign IDs registered in `render.yaml`, dashboard got a "US district campaigns" card row, README documents the new type per the existing extension-guide pattern

## Next steps

### Immediate (before module1 campaigns send)
- Verify Instantly webhook is pointing to `https://sor-curriculum-api.onrender.com/webhooks/instantly-reply?secret=YOUR_SECRET`
- Confirm all 4 systeme.io age-specific automation rules are built (tag added → enroll in Module 1 + subscribe nurture)
- Confirm `Sept26-FollowUp` automation rule exists (for September follow-up tag)
- Test one real reply before campaigns go live (check dashboard + `/automation/log`)

### Before US district campaigns send (late August)
- **Done**: real Instantly campaign IDs confirmed and match `render.yaml` (`US-24Aug-CurriculumDirectors` / `US-25Aug-ScienceSTEMDirectors`, both currently Draft status in Instantly)
- **Done**: systeme.io booking flow fully built, no-code side — "District Intro Call" event (20 min, Google Meet, Asia/Makassar availability Mon-Fri 8-11PM + Tue-Sat 5:30-8AM WITA to cover all 4 continental US timezones without the account's 00:00-05:00 blackout), booking page at `schoolofrecycling.com/us-districts-call-booking` with a 3-question form (district name, role, optional context), shared "US District Warm Reply Follow-up" campaign (2 emails: booking link + 3-day nudge), both tags (`us-district-curriculum-reply` / `us-district-science-reply`) created, and a single combined Automation Rule (2 "Tag added" triggers, OR logic, → Subscribe to campaign) live
- **Known gap**: systeme.io has no native "booked a meeting" trigger yet (on their roadmap, not shipped) — the nudge email can't auto-suppress once someone's booked. Workaround: periodically check the Bookings tab and manually remove anyone who's already booked from the campaign before the 3-day nudge fires. Worth re-checking systeme.io's roadmap before every future campaign that reuses this pattern.
- **Not yet done**: Debounce verification run on the purchased 516-contact list (list not purchased yet — user needs to buy it first before this or merge-field work can proceed)
- **Not yet done**: Campaign A's Email 1 subject line needs a fix — "Quick question re: {{district_name}}'s science/sustainability curriculum" reads Track-B-specific; broaden to something track-neutral like "...curriculum plans" since Track A's list includes many non-science titles (Chief Academic Officer, Deputy Superintendent, etc.)
- **Not yet done**: Campaign A emails 3-4 (social proof, low-pressure close) not yet drafted/reviewed this pass — only Emails 1-2 reviewed so far
- **Not yet done**: Campaign B (Science/STEM track) email copy — needs the same 4-email structure as Track A with sharper NGSS/standards framing in Email 2; hold until Track A copy + merge-field questions are resolved
- **Not yet done**: final merge-field population once list is verified (real district names/enrollment, not placeholders) — also confirm CAN-SPAM compliance (physical postal address + opt-out mechanism) somewhere in the cold sequence, since this is manual sending to ~500 public-sector contacts, not through a bulk ESP with an auto-footer
- **Not yet done**: Test one real/sample reply per track through the full live pipeline (webhook → tag → automation rule → follow-up email) now that all the no-code pieces exist (see README "US school-district curriculum decision-maker outreach" section)
- **Not yet done**: Enable Instantly's "stop sending on reply" + AI Smart Pause for OOO auto-replies; consider "stop emails to whole company on any reply"

### End of August (school decision-maker campaigns — separate `schools` stub, still unimplemented)
1. Create school campaigns in Instantly, get campaign IDs
2. Add IDs to `INSTANTLY_SCHOOLS_CAMPAIGN_IDS` in Render (or env var)
3. Implement `handle_schools_campaign()` in `email_automation.py` (classify for decision-maker intent, apply different tag scheme, different enrollment)
4. Create systeme.io automation rules for school campaign tags
5. Test with sample reply
6. Redeploy, go live

See README "Campaign types & routing" section → "How to add a new campaign type" for detailed steps.

### Optional future work
- Remove `/automation/debug/systeme-tags` diagnostic endpoint (added for debugging, no longer needed)
- Split nurture emails by language if needed (currently all send same language, regardless of reply language)
- Add more campaign types as needed

## Testing

**Test webhook (sample)**:
```bash
curl -X POST "https://sor-curriculum-api.onrender.com/webhooks/instantly-reply?secret=YOUR_WEBHOOK_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type":"reply_received",
    "campaign_id":"US-27Aug-NY",
    "lead_email":"test@example.com",
    "reply_subject":"Age question",
    "reply_text":"I teach 5th grade"
  }'
```

**Expected**: `"status":"processed"`, `"action":"tagged_module1"`, age group `"10-12"` extracted.

**Dashboard**: `https://sor-curriculum-api.onrender.com/dashboard?key=YOUR_SOR_MASTER_KEY`

**API log**: `GET /automation/log?limit=10` (requires `X-API-Key` header with any valid key)

## Architecture decisions

**Why campaign-type routing?**
- Different campaigns may have completely different intents (age groups vs decision criteria vs other)
- Avoids hardcoding all logic in one webhook
- New campaign types can be added without modifying webhook logic
- Unregistered campaigns are safely ignored (not errored)

**Why 4 age tags + 2 custom fields (not 12 combined age×currency tags)?**
- systeme.io Automation Rules support OR logic (tag A OR tag B), not AND
- Currency-specific checkout links are written as custom fields on contact, read by nurture email merge tags
- Age-specific nurture campaigns already exist, no need for 12 duplicates

**Why query param for webhook secret (not header)?**
- Simpler testing (one curl arg to modify)
- More reliable than header parsing in some contexts
- Code supports both, query param preferred

**Why persistent disk upgrade?**
- Free tier Render spins down after 15min, losing container filesystem
- Dashboard stats (reply counts, language breakdown) would disappear between uses
- Standard plan (~$7/month) enables persistent `/data/sor.db`

## Known limitations / blind spots

**systeme.io integration**:
- Contact create/PATCH/tag shapes not verified against live API (docs site was 403 during dev)
- Error responses do surface full body for debugging
- First test with live key should verify shapes work (see README "Go-live checklist")

**Instantly webhook**:
- Country field name not confirmed (tries multiple candidates, graceful fallback if missing)
- Secret must be passed as query param in testing (`?secret=...`), header format is flaky

**Claude classification**:
- Haiku model fast but sometimes needs more context
- Multi-language accuracy varies; logged with language code so you can spot-check by language

## Questions? Stuck?

- Check README "Campaign types & routing" for architecture & extension guide
- Check `/automation/log` for raw event details (includes full Instantly payload + error messages)
- Dashboard auto-refreshes every 30s — watch it live during testing

---

**Branch**: `claude/email-reply-course-automation-adoh5g`

**Render URL**: `https://sor-curriculum-api.onrender.com`

**API Docs**: `https://sor-curriculum-api.onrender.com/docs` (live after deploy)

**Dashboard**: `https://sor-curriculum-api.onrender.com/dashboard?key=YOUR_SOR_MASTER_KEY`
