"""
Reply-to-course automation.

Flow: Instantly (cold email campaign) -> webhook on reply -> Claude classifies
the reply -> systeme.io contact gets tagged -> a systeme.io automation rule
(built in their no-code editor, not here) sends the matching free Module 1
and enrolls the lead in the nurture sequence.

Everything here is best-effort against publicly documented behaviour for
Instantly API v2 webhooks and the systeme.io public API. Neither vendor's
exact request/response shape could be verified against a live key while this
was written -- see README "Go-live checklist" before sending real traffic.
"""

import hashlib
import json
import os

import httpx
from anthropic import Anthropic
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from fastapi.responses import HTMLResponse

from auth import is_valid_key, require_api_key
from database import get_db

router = APIRouter()

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
SYSTEME_IO_API_KEY = os.environ.get("SYSTEME_IO_API_KEY", "")
INSTANTLY_WEBHOOK_SECRET = os.environ.get("INSTANTLY_WEBHOOK_SECRET", "")

SYSTEME_IO_BASE_URL = "https://api.systeme.io/api"
CLASSIFIER_MODEL = "claude-haiku-4-5-20251001"

AGE_GROUPS = ["6-9", "10-12", "13-16", "17+"]
CURRENCIES = ["EUR", "GBP", "USD"]

# EU member states (English names as they're likely to appear in a "Person
# Country" CSV column), used for the EUR bucket. UK is handled separately
# (GBP). Everything not in either set falls back to USD.
EU_COUNTRIES = {
    "austria", "belgium", "bulgaria", "croatia", "cyprus", "czech republic",
    "czechia", "denmark", "estonia", "finland", "france", "germany",
    "greece", "hungary", "ireland", "italy", "latvia", "lithuania",
    "luxembourg", "malta", "netherlands", "the netherlands", "poland",
    "portugal", "romania", "slovakia", "slovenia", "spain", "sweden",
}
UK_NAMES = {"united kingdom", "uk", "great britain", "england", "scotland", "wales", "northern ireland"}


def currency_for_country(country: str) -> str:
    normalized = country.strip().lower()
    if normalized in UK_NAMES:
        return "GBP"
    if normalized in EU_COUNTRIES:
        return "EUR"
    return "USD"


# Candidate keys to look for the lead's country under in the Instantly
# webhook payload -- the exact field name Instantly uses for a CSV custom
# column ("Person Country") wasn't verifiable against live docs while this
# was written. Checked in order, case/spacing-insensitive, both at the top
# level of the payload and inside common nested containers for custom lead
# variables. See README "Go-live checklist" -- confirm/adjust this list
# against a real payload's raw_payload in /automation/log.
COUNTRY_FIELD_CANDIDATES = ["person country", "personcountry", "country", "lead country"]
PAYLOAD_NESTED_CONTAINERS = ["variables", "custom_variables", "lead_data", "custom_fields", "lead_custom_fields"]


def _extract_country(payload: dict) -> str | None:
    def _search(d: dict) -> str | None:
        normalized_keys = {k.strip().lower().replace("_", " "): k for k in d.keys()}
        for candidate in COUNTRY_FIELD_CANDIDATES:
            if candidate in normalized_keys:
                value = d[normalized_keys[candidate]]
                if isinstance(value, str) and value.strip():
                    return value.strip()
        return None

    found = _search(payload)
    if found:
        return found

    for container_key in PAYLOAD_NESTED_CONTAINERS:
        nested = payload.get(container_key)
        if isinstance(nested, dict):
            found = _search(nested)
            if found:
                return found

    return None


# The age tag's systeme.io rule enrols the contact in that age's free
# Module 1 course and subscribes them to that age's nurture campaign.
# Currency doesn't need its own tag/rule -- it's written directly onto the
# contact as custom fields (checkout_link_class, checkout_link_school),
# which the nurture emails reference via systeme.io merge tags
# ({checkout_link_class} / {checkout_link_school}). Same email content works
# for every currency automatically.
MODULE1_AGE_TAGS = {
    "6-9": "Module-1 Free (6-9yr)",
    "10-12": "Module-1 Free (10-12yr)",
    "13-16": "Module-1 Free (13-16yr)",
    "17+": "Module-1 Free (17+yr)",
}
SEPTEMBER_TAG = "Sept26-FollowUp"

# Class licence checkout link is age- and currency-specific (12 pages).
# NOTE: stored WITHOUT the "https://" scheme on purpose. systeme.io's link
# editor forces its own "https://" in front of whatever's typed into a link's
# URL field, and pairing that with a merge-tag value that also starts with
# "https://" produced a corrupted link in testing (the substituted value's
# colon got dropped, e.g. "https//www.schoolofrecycling.com/..." -> broken
# DNS lookup). Keeping the scheme out of the stored value avoids the
# collision entirely, regardless of the exact cause on systeme.io's end.
CHECKOUT_LINKS_CLASS = {
    "6-9": {
        "EUR": "www.schoolofrecycling.com/wd-p-69-classroom-euro",
        "GBP": "www.schoolofrecycling.com/wd-p-69-classroom-gbp",
        "USD": "www.schoolofrecycling.com/wd-p-69-classroom-usd",
    },
    "10-12": {
        "EUR": "www.schoolofrecycling.com/wd-p-1012-classroom-euro",
        "GBP": "www.schoolofrecycling.com/wd-p-1012-classroom-gbp",
        "USD": "www.schoolofrecycling.com/wd-p-1012-classroom-usd",
    },
    "13-16": {
        "EUR": "www.schoolofrecycling.com/wd-p-1316-classroom-euro",
        "GBP": "www.schoolofrecycling.com/wd-p-1316-classroom-gbp",
        "USD": "www.schoolofrecycling.com/wd-p-1316-classroom-usd",
    },
    "17+": {
        "EUR": "www.schoolofrecycling.com/wd-p-17-classroom-euro",
        "GBP": "www.schoolofrecycling.com/wd-p-17-classroom-gbp",
        "USD": "www.schoolofrecycling.com/wd-p-17-classroom-usd",
    },
}

# School licence checkout link is currency-specific only, not age-specific.
CHECKOUT_LINKS_SCHOOL = {
    "EUR": "www.schoolofrecycling.com/wd-p-school-licence-euro",
    "GBP": "www.schoolofrecycling.com/wd-p-school-licence-gbp",
    "USD": "www.schoolofrecycling.com/wd-p-school-licence-usd",
}

_anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None

CLASSIFY_SYSTEM_PROMPT = """You classify replies to a School of Recycling cold email campaign,
sent to teachers and parents in many countries. Replies may be in ANY language, including
languages different from the one the campaign was sent in. Read and reason about the reply
in its own language -- do not require English or literal keyword matches.

The campaign's 3-email sequence asks the recipient (a teacher or parent) to reply with the
age group they teach, in exchange for free access to Module 1 of the matching course. The
last email adds: if now isn't a good time, reply asking for a follow-up when the new school
year starts (this may be phrased as "September" or as the equivalent northern- or
southern-hemisphere school-year start in the recipient's own country and language).

Read the reply and call classify_reply with:
- intent: "age_group_provided" if they state or imply an age group / grade / class / year / form level
  they teach, in whatever schooling-system terminology their country and language use.
- intent: "september_followup" if they ask to be followed up with at the start of the next school year,
  regardless of language or which month that actually falls in for their country.
- intent: "not_interested" if they decline, ask to be removed, or are clearly negative.
- intent: "unclear" for anything else (questions you can't confidently resolve, blank/garbled replies,
  replies unrelated to the offer).

If intent is "age_group_provided", also set age_group to exactly one of "6-9", "10-12", "13-16", "17+"
by converting whatever grade/class/year/form is mentioned to the age of students at that level in that
country's education system, then mapping to the closest band. If the age/grade is too ambiguous to
place confidently -- including cases where the schooling term doesn't map cleanly to a known system --
use intent "unclear" instead of guessing.

Always also set language to the ISO 639-1 code of the language the reply itself is written in
(e.g. "en", "fr", "de", "es", "nl"), regardless of what language the campaign was sent in."""

CLASSIFY_TOOL = {
    "name": "classify_reply",
    "description": "Record the classification of a cold-email reply.",
    "input_schema": {
        "type": "object",
        "properties": {
            "intent": {
                "type": "string",
                "enum": ["age_group_provided", "september_followup", "not_interested", "unclear"],
            },
            "age_group": {
                "type": "string",
                "enum": AGE_GROUPS,
                "description": "Required when intent is age_group_provided, omitted otherwise.",
            },
            "language": {
                "type": "string",
                "description": "ISO 639-1 code of the language the reply is written in, e.g. 'en', 'fr', 'de'.",
            },
        },
        "required": ["intent", "language"],
    },
}


def classify_reply(reply_text: str, reply_subject: str = "") -> dict:
    if _anthropic_client is None:
        raise RuntimeError("ANTHROPIC_API_KEY is not configured.")

    message = _anthropic_client.messages.create(
        model=CLASSIFIER_MODEL,
        max_tokens=200,
        system=CLASSIFY_SYSTEM_PROMPT,
        tools=[CLASSIFY_TOOL],
        tool_choice={"type": "tool", "name": "classify_reply"},
        messages=[
            {
                "role": "user",
                "content": f"Subject: {reply_subject}\n\nReply:\n{reply_text}",
            }
        ],
    )

    for block in message.content:
        if block.type == "tool_use" and block.name == "classify_reply":
            result = dict(block.input)
            if result.get("intent") != "age_group_provided":
                result["age_group"] = None
            return result

    return {"intent": "unclear", "age_group": None}


# ---------------------------------------------------------------------------
# systeme.io client
#
# NOTE: could not reach developer.systeme.io's live reference while building
# this (blocked upstream), so the exact create/lookup/tag-assign shapes below
# are the best-documented public behaviour, not verified against a real
# response. Smoke-test against your key before relying on it at volume.
# ---------------------------------------------------------------------------

class SystemeIOError(Exception):
    pass


def _systeme_headers() -> dict:
    if not SYSTEME_IO_API_KEY:
        raise SystemeIOError("SYSTEME_IO_API_KEY is not configured.")
    return {"X-API-Key": SYSTEME_IO_API_KEY, "Content-Type": "application/json"}


def _raise_for_status_with_body(resp: httpx.Response) -> None:
    """Like resp.raise_for_status(), but keeps the response body in the error
    instead of discarding it -- systeme.io's error detail lives in the body."""
    if resp.is_error:
        raise SystemeIOError(
            f"{resp.request.method} {resp.request.url} -> {resp.status_code}: {resp.text}"
        )


def _find_contact_id_by_email(client: httpx.Client, email: str) -> str | None:
    resp = client.get(
        f"{SYSTEME_IO_BASE_URL}/contacts",
        headers=_systeme_headers(),
        params={"email": email},
    )
    _raise_for_status_with_body(resp)
    items = resp.json().get("items", [])
    for item in items:
        if item.get("email", "").lower() == email.lower():
            return str(item.get("id"))
    return None


def _create_contact(client: httpx.Client, email: str) -> str:
    resp = client.post(
        f"{SYSTEME_IO_BASE_URL}/contacts",
        headers=_systeme_headers(),
        json={"email": email},
    )
    if resp.status_code == 422:
        try:
            existing_id = _find_contact_id_by_email(client, email)
        except SystemeIOError as lookup_exc:
            raise SystemeIOError(
                f"Contact create for {email} returned 422 (body: {resp.text}); "
                f"lookup fallback also failed: {lookup_exc}"
            ) from lookup_exc
        if existing_id:
            return existing_id
        raise SystemeIOError(
            f"Contact create for {email} returned 422 with no matching existing "
            f"contact found via lookup. systeme.io response body: {resp.text}"
        )
    _raise_for_status_with_body(resp)
    return str(resp.json()["id"])


def _find_tag_id_by_name(client: httpx.Client, tag_name: str) -> str | None:
    """Search GET /tags for an exact (case/whitespace-insensitive) name match.

    systeme.io uses cursor pagination, not a page number: each response has
    "items" + "hasMore", and the next page is fetched via
    startingAfter=<id of the last item just received>. Confirmed via
    /automation/debug/systeme-tags against the live API -- a "page" query
    param (tried first) is silently ignored and always returns the same
    first page, which is why that approach missed tags that existed further
    back in the list. Capped at 20 iterations as a safety net.
    """
    target = tag_name.strip().lower()
    starting_after = None
    for _ in range(20):
        params = {"limit": 100}
        if starting_after is not None:
            params["startingAfter"] = starting_after
        resp = client.get(
            f"{SYSTEME_IO_BASE_URL}/tags",
            headers=_systeme_headers(),
            params=params,
        )
        _raise_for_status_with_body(resp)
        data = resp.json()
        items = data.get("items", [])
        for tag in items:
            if str(tag.get("name", "")).strip().lower() == target:
                return str(tag["id"])
        if not items or not data.get("hasMore"):
            return None
        starting_after = items[-1]["id"]
    return None


def _get_or_create_tag_id(client: httpx.Client, tag_name: str) -> str:
    existing_id = _find_tag_id_by_name(client, tag_name)
    if existing_id:
        return existing_id

    resp = client.post(
        f"{SYSTEME_IO_BASE_URL}/tags",
        headers=_systeme_headers(),
        json={"name": tag_name},
    )
    if resp.status_code == 422:
        existing_id = _find_tag_id_by_name(client, tag_name)
        if existing_id:
            return existing_id
        raise SystemeIOError(
            f"Tag create for {tag_name!r} returned 422 with no matching existing tag "
            f"found via paginated lookup. systeme.io response body: {resp.text}"
        )
    _raise_for_status_with_body(resp)
    return str(resp.json()["id"])


def _assign_tag(client: httpx.Client, contact_id: str, tag_name: str) -> str:
    tag_id = _get_or_create_tag_id(client, tag_name)
    resp = client.post(
        f"{SYSTEME_IO_BASE_URL}/contacts/{contact_id}/tags",
        headers=_systeme_headers(),
        json={"tagId": int(tag_id)},
    )
    _raise_for_status_with_body(resp)
    return tag_id


def _set_custom_fields(client: httpx.Client, contact_id: str, fields: dict[str, str]) -> None:
    """Set custom field values (e.g. checkout_link_class) on a contact.

    NOTE: the exact update-contact request shape (PATCH vs PUT, "fields" as a
    slug/value array vs flat keys) wasn't verifiable against live systeme.io
    docs while this was written -- same blind spot as the other systeme.io
    calls in this file. If this errors, the response body (surfaced via
    _raise_for_status_with_body) will show the real expected shape.
    """
    resp = client.patch(
        f"{SYSTEME_IO_BASE_URL}/contacts/{contact_id}",
        headers={**_systeme_headers(), "Content-Type": "application/merge-patch+json"},
        json={"fields": [{"slug": slug, "value": value} for slug, value in fields.items()]},
    )
    _raise_for_status_with_body(resp)


def upsert_contact_and_tags(
    email: str, tag_names: list[str], custom_fields: dict[str, str] | None = None
) -> tuple[str, list[str]]:
    """Create/find the contact once, assign each of tag_names, and set any custom_fields."""
    with httpx.Client(timeout=15) as client:
        contact_id = _create_contact(client, email)
        tag_ids = [_assign_tag(client, contact_id, name) for name in tag_names]
        if custom_fields:
            _set_custom_fields(client, contact_id, custom_fields)
        return contact_id, tag_ids


# ---------------------------------------------------------------------------
# Webhook
# ---------------------------------------------------------------------------

def _verify_webhook_secret(request: Request, x_webhook_secret: str | None) -> None:
    if not INSTANTLY_WEBHOOK_SECRET:
        return  # not configured yet -- allow through during setup/testing
    provided = x_webhook_secret or request.query_params.get("secret")
    if provided != INSTANTLY_WEBHOOK_SECRET:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid webhook secret.")


def _dedupe_key(payload: dict, lead_email: str, reply_text: str) -> str:
    explicit_id = payload.get("event_id") or payload.get("id") or payload.get("reply_id")
    if explicit_id:
        return f"id:{explicit_id}"
    raw = f"{lead_email}|{payload.get('campaign_id', '')}|{reply_text}"
    return "hash:" + hashlib.sha256(raw.encode()).hexdigest()


def _log(conn, dedupe_key, lead_email, campaign_id, reply_subject, reply_text,
          intent, age_group, language, country, currency, action, tag_applied,
          systeme_contact_id, error, raw_payload):
    conn.execute(
        """
        INSERT OR IGNORE INTO reply_automation_log
            (dedupe_key, lead_email, campaign_id, reply_subject, reply_text,
             intent, age_group, language, country, currency, action, tag_applied,
             systeme_contact_id, error, raw_payload)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (dedupe_key, lead_email, campaign_id, reply_subject, reply_text,
         intent, age_group, language, country, currency, action, tag_applied,
         systeme_contact_id, error, raw_payload),
    )
    conn.commit()


@router.post("/webhooks/instantly-reply", tags=["Automation"], summary="Instantly reply webhook")
async def instantly_reply_webhook(
    request: Request,
    x_webhook_secret: str | None = Header(default=None),
):
    _verify_webhook_secret(request, x_webhook_secret)
    payload = await request.json()

    if payload.get("event_type") != "reply_received":
        return {"status": "ignored", "reason": f"event_type={payload.get('event_type')!r}"}

    lead_email = payload.get("lead_email")
    reply_text = payload.get("reply_text") or payload.get("reply_text_snippet") or ""
    reply_subject = payload.get("reply_subject", "")
    campaign_id = payload.get("campaign_id")

    if not lead_email or not reply_text:
        raise HTTPException(status_code=422, detail="Payload missing lead_email or reply_text.")

    dedupe_key = _dedupe_key(payload, lead_email, reply_text)
    conn = get_db()

    existing = conn.execute(
        "SELECT id FROM reply_automation_log WHERE dedupe_key = ?", (dedupe_key,)
    ).fetchone()
    if existing:
        conn.close()
        return {"status": "duplicate", "dedupe_key": dedupe_key}

    intent, age_group, language, country, currency, action, tag_applied, systeme_contact_id, error = (
        "unclear", None, None, None, None, "none", None, None, None
    )

    try:
        classification = classify_reply(reply_text, reply_subject)
        intent = classification.get("intent", "unclear")
        age_group = classification.get("age_group")
        language = classification.get("language")

        if intent == "age_group_provided" and age_group in MODULE1_AGE_TAGS:
            age_tag = MODULE1_AGE_TAGS[age_group]
            country = _extract_country(payload)
            custom_fields = None
            if country is not None:
                currency = currency_for_country(country)
                custom_fields = {
                    "checkout_link_class": CHECKOUT_LINKS_CLASS[age_group][currency],
                    "checkout_link_school": CHECKOUT_LINKS_SCHOOL[currency],
                }

            systeme_contact_id, _ = upsert_contact_and_tags(lead_email, [age_tag], custom_fields)
            tag_applied = age_tag

            if country is None:
                action = "tagged_module1_currency_pending"
                error = "Got Module 1 access, but no country field in the webhook payload -- checkout links not set yet."
            else:
                action = "tagged_module1"
        elif intent == "september_followup":
            tag_applied = SEPTEMBER_TAG
            systeme_contact_id, _ = upsert_contact_and_tags(lead_email, [SEPTEMBER_TAG])
            action = "tagged_september"
        elif intent == "not_interested":
            action = "logged_not_interested"
        else:
            action = "logged_unclear"
    except (SystemeIOError, httpx.HTTPError, RuntimeError) as exc:
        error = str(exc)
        action = "error"

    _log(
        conn, dedupe_key, lead_email, campaign_id, reply_subject, reply_text,
        intent, age_group, language, country, currency, action, tag_applied,
        systeme_contact_id, error, json.dumps(payload),
    )
    conn.close()

    return {
        "status": "processed",
        "action": action,
        "intent": intent,
        "age_group": age_group,
        "language": language,
        "country": country,
        "currency": currency,
        "tag_applied": tag_applied,
        "error": error,
    }


@router.get(
    "/automation/log",
    tags=["Automation", "Gated"],
    summary="Review recent reply-automation activity (requires X-API-Key)",
)
def automation_log(
    action: str | None = None,
    limit: int = 50,
    _key: str = Depends(require_api_key),
):
    conn = get_db()
    if action:
        rows = conn.execute(
            "SELECT * FROM reply_automation_log WHERE action = ? ORDER BY id DESC LIMIT ?",
            (action, limit),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM reply_automation_log ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.get(
    "/automation/stats",
    tags=["Automation", "Gated"],
    summary="Aggregate counts for the reply-automation dashboard (requires X-API-Key)",
)
def automation_stats(_key: str = Depends(require_api_key)):
    conn = get_db()

    totals = conn.execute("SELECT COUNT(*) AS n FROM reply_automation_log").fetchone()["n"]

    by_action = {
        r["action"]: r["n"]
        for r in conn.execute(
            "SELECT action, COUNT(*) AS n FROM reply_automation_log GROUP BY action"
        ).fetchall()
    }

    by_age_group = {
        r["age_group"]: r["n"]
        for r in conn.execute(
            """SELECT age_group, COUNT(*) AS n FROM reply_automation_log
               WHERE action IN ('tagged_module1', 'tagged_module1_currency_pending')
               GROUP BY age_group"""
        ).fetchall()
    }

    by_currency = {
        r["currency"]: r["n"]
        for r in conn.execute(
            """SELECT currency, COUNT(*) AS n FROM reply_automation_log
               WHERE action = 'tagged_module1' GROUP BY currency"""
        ).fetchall()
    }

    by_day = [
        dict(r)
        for r in conn.execute(
            """SELECT date(received_at) AS day, COUNT(*) AS n
               FROM reply_automation_log
               GROUP BY day ORDER BY day DESC LIMIT 14"""
        ).fetchall()
    ]

    by_language = {
        (r["language"] or "unknown"): r["n"]
        for r in conn.execute(
            """SELECT language, COUNT(*) AS n FROM reply_automation_log
               GROUP BY language ORDER BY n DESC"""
        ).fetchall()
    }

    last_received_at = conn.execute(
        "SELECT MAX(received_at) AS t FROM reply_automation_log"
    ).fetchone()["t"]

    conn.close()

    return {
        "total_replies": totals,
        "by_action": by_action,
        "module1_by_age_group": by_age_group,
        "module1_by_currency": by_currency,
        "by_language": by_language,
        "by_day": by_day,
        "last_received_at": last_received_at,
        "errors": by_action.get("error", 0),
        "needs_currency_review": by_action.get("tagged_module1_currency_pending", 0),
    }


@router.get(
    "/automation/debug/systeme-tags",
    tags=["Automation", "Gated"],
    summary="TEMPORARY: raw systeme.io GET /tags response, for diagnosing the tag-lookup bug (requires X-API-Key)",
)
def debug_systeme_tags(name: str = "", page: int = 1, _key: str = Depends(require_api_key)):
    """Hits systeme.io's GET /tags directly and returns it close to raw, so we can see
    the actual response shape (pagination fields, exact tag name strings) instead of
    guessing. Pass ?name=... to also report whether that exact string is present."""
    with httpx.Client(timeout=15) as client:
        resp = client.get(
            f"{SYSTEME_IO_BASE_URL}/tags",
            headers=_systeme_headers(),
            params={"page": page},
        )
    body = resp.text
    try:
        parsed = resp.json()
    except ValueError:
        parsed = None

    items = parsed.get("items", []) if isinstance(parsed, dict) else None
    result = {
        "status_code": resp.status_code,
        "top_level_keys": list(parsed.keys()) if isinstance(parsed, dict) else None,
        "items_count_this_page": len(items) if items is not None else None,
        "item_names_this_page": [t.get("name") for t in items] if items is not None else None,
        "raw_body": body[:4000],
    }
    if name:
        result["exact_match_found_this_page"] = bool(
            items and any(t.get("name") == name for t in items)
        )
        result["case_insensitive_match_found_this_page"] = bool(
            items and any(str(t.get("name", "")).strip().lower() == name.strip().lower() for t in items)
        )
    return result


@router.get("/dashboard", tags=["Automation"], summary="HTML dashboard for reply automation (requires ?key=)")
def dashboard(key: str = ""):
    if not is_valid_key(key):
        return HTMLResponse(
            "<p style='font-family:sans-serif;padding:40px'>"
            "Missing or invalid <code>?key=</code>. Append your SoR API key to the URL.</p>",
            status_code=401,
        )
    return HTMLResponse(_DASHBOARD_HTML.replace("__KEY__", key))


_DASHBOARD_HTML = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>SoR Reply Automation Dashboard</title>
<style>
  :root { color-scheme: light dark; }
  body { font-family: -apple-system, Segoe UI, Roboto, sans-serif; margin: 0; padding: 24px;
         background: #f6f7f8; color: #1a1a1a; }
  @media (prefers-color-scheme: dark) { body { background: #14161a; color: #e8e8e8; } }
  h1 { font-size: 20px; margin: 0 0 4px; }
  .sub { color: #777; font-size: 13px; margin-bottom: 20px; }
  .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-bottom: 24px; }
  .card { background: white; border-radius: 10px; padding: 14px 16px; box-shadow: 0 1px 3px rgba(0,0,0,.08); }
  @media (prefers-color-scheme: dark) { .card { background: #20232a; } }
  .card .n { font-size: 26px; font-weight: 700; }
  .card .l { font-size: 12px; color: #888; margin-top: 2px; }
  .card.err .n { color: #d33; }
  table { width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; font-size: 13px; }
  @media (prefers-color-scheme: dark) { table { background: #20232a; } }
  th, td { text-align: left; padding: 8px 10px; border-bottom: 1px solid rgba(128,128,128,.15); }
  th { font-size: 11px; text-transform: uppercase; color: #888; }
  tr.error { background: rgba(221,51,51,.08); }
  .pill { display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 11px; background: #eee; }
  @media (prefers-color-scheme: dark) { .pill { background: #333; } }
  .section-title { font-size: 13px; text-transform: uppercase; color: #888; margin: 24px 0 8px; }
  .wrap { overflow-x: auto; }
</style>
</head>
<body>
  <h1>Reply Automation Dashboard</h1>
  <div class="sub">Instantly reply → Claude classify → systeme.io tag. Auto-refreshes every 30s. Last reply: <span id="last">–</span></div>

  <div class="cards" id="cards"></div>

  <div class="section-title">Free Module 1 sent, by age group</div>
  <div class="cards" id="age-cards"></div>

  <div class="section-title">Free Module 1 sent, by currency</div>
  <div class="cards" id="currency-cards"></div>

  <div class="section-title">Replies by language</div>
  <div class="cards" id="lang-cards"></div>

  <div class="section-title">Recent activity</div>
  <div class="wrap">
    <table>
      <thead><tr><th>Time</th><th>Email</th><th>Lang</th><th>Intent</th><th>Age</th><th>Country</th><th>Currency</th><th>Action</th><th>Error</th></tr></thead>
      <tbody id="log-body"></tbody>
    </table>
  </div>

<script>
const KEY = "__KEY__";
const headers = { "X-API-Key": KEY };

function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

// received_at is stored as UTC ("YYYY-MM-DD HH:MM:SS", no timezone marker --
// SQLite's datetime('now')). Treat it as UTC explicitly, then render in
// whoever's viewing the dashboard's own local timezone.
function toLocal(utcString) {
  if (!utcString) return utcString;
  const d = new Date(utcString.replace(" ", "T") + "Z");
  if (isNaN(d.getTime())) return utcString;
  return d.toLocaleString(undefined, {
    year: "numeric", month: "2-digit", day: "2-digit",
    hour: "2-digit", minute: "2-digit", second: "2-digit",
  });
}

async function load() {
  const [stats, log] = await Promise.all([
    fetch("/automation/stats", { headers }).then(r => r.json()),
    fetch("/automation/log?limit=100", { headers }).then(r => r.json()),
  ]);

  document.getElementById("last").textContent = stats.last_received_at ? toLocal(stats.last_received_at) : "no replies yet";

  const cards = [
    ["Total replies", stats.total_replies, ""],
    ["Module 1 sent", (stats.by_action.tagged_module1 || 0) + (stats.by_action.tagged_module1_currency_pending || 0), ""],
    ["September follow-up", stats.by_action.tagged_september || 0, ""],
    ["Not interested", stats.by_action.logged_not_interested || 0, ""],
    ["Needs review", stats.by_action.logged_unclear || 0, ""],
    ["Needs currency review", stats.needs_currency_review, stats.needs_currency_review ? "err" : ""],
    ["Errors", stats.errors, "err"],
  ];
  document.getElementById("cards").innerHTML = cards.map(([l, n, cls]) =>
    `<div class="card ${cls}"><div class="n">${esc(n)}</div><div class="l">${esc(l)}</div></div>`
  ).join("");

  const ageGroups = ["6-9", "10-12", "13-16", "17+"];
  document.getElementById("age-cards").innerHTML = ageGroups.map(ag =>
    `<div class="card"><div class="n">${esc(stats.module1_by_age_group[ag] || 0)}</div><div class="l">${esc(ag)}</div></div>`
  ).join("");

  const currencies = ["EUR", "GBP", "USD"];
  document.getElementById("currency-cards").innerHTML = currencies.map(c =>
    `<div class="card"><div class="n">${esc(stats.module1_by_currency[c] || 0)}</div><div class="l">${esc(c)}</div></div>`
  ).join("");

  const langEntries = Object.entries(stats.by_language || {});
  document.getElementById("lang-cards").innerHTML = langEntries.length
    ? langEntries.map(([lang, n]) =>
        `<div class="card"><div class="n">${esc(n)}</div><div class="l">${esc(lang)}</div></div>`
      ).join("")
    : `<div class="card"><div class="n">–</div><div class="l">no data yet</div></div>`;

  document.getElementById("log-body").innerHTML = log.map(r => `
    <tr class="${r.error ? 'error' : ''}">
      <td>${esc(toLocal(r.received_at))}</td>
      <td>${esc(r.lead_email)}</td>
      <td>${esc(r.language || '-')}</td>
      <td><span class="pill">${esc(r.intent || '-')}</span></td>
      <td>${esc(r.age_group || '-')}</td>
      <td>${esc(r.country || '-')}</td>
      <td>${esc(r.currency || '-')}</td>
      <td>${esc(r.action)}</td>
      <td>${esc(r.error || '')}</td>
    </tr>
  `).join("");
}

load();
setInterval(load, 30000);
</script>
</body>
</html>
"""
