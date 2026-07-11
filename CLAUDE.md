# Nowhere Maps — Reply-to-Course Automation

## Project overview

School of Recycling automated email-reply-to-course enrollment system. Instantly cold-email campaigns → Claude classifies reply → systeme.io tag applied → contact auto-enrolled in free Module 1 + nurture sequence.

**Status**: Production-ready. 24 teacher/age-group campaigns active, ready to send. Schools/decision-maker campaigns planned end of August.

## Current setup

**Campaigns (active)**: 24 Module 1 campaigns across 2x US, 4x UK, 1x SE, 1x NO, 1x FI, 1x DK, 3x BE, 8x DE, 3x NL = ~40 mailboxes, ~13k sends planned.

**Configuration**:
- Render deployment: `sor-curriculum-api` (standard plan for persistent disk)
- Database: SQLite `/data/sor.db` on persistent 1GB disk
- API keys: `SOR_MASTER_KEY` auto-generated on first deploy
- Webhook secret: `INSTANTLY_WEBHOOK_SECRET` (set in Render environment, use query param `?secret=...` for testing)
- Environment vars: See `sor-api/render.yaml` (ANTHROPIC_API_KEY, SYSTEME_IO_API_KEY, INSTANTLY_WEBHOOK_SECRET, INSTANTLY_MODULE1_CAMPAIGN_IDS, INSTANTLY_SCHOOLS_CAMPAIGN_IDS)

**Campaign routing**: 
- Type-based architecture (`campaign_id` → `campaign_type` → handler)
- 24 IDs registered under `module1` type in `INSTANTLY_MODULE1_CAMPAIGN_IDS`
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

## Next steps

### Immediate (before campaigns send)
- Verify Instantly webhook is pointing to `https://sor-curriculum-api.onrender.com/webhooks/instantly-reply?secret=YOUR_SECRET`
- Confirm all 4 systeme.io age-specific automation rules are built (tag added → enroll in Module 1 + subscribe nurture)
- Confirm `Sept26-FollowUp` automation rule exists (for September follow-up tag)
- Test one real reply before campaigns go live (check dashboard + `/automation/log`)

### End of August (school decision-maker campaigns)
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
