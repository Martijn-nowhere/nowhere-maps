#!/usr/bin/env python3
"""
setup_systeme.py — SoR Summer Webinar 2026
Creates the funnel, steps, email campaign, and emails via the systeme.io API.

Usage:
    1. Copy .env.example to .env and add your SYSTEME_API_KEY.
    2. Run: python scripts/setup_systeme.py

Operations NOT covered by the systeme.io API are printed as manual instructions
rather than attempted — the script will never invent endpoints.
"""

import os
import sys
import json
import http.client
import urllib.parse
from pathlib import Path


# ── Config ────────────────────────────────────────────────────────────────────

BASE_URL = "api.systeme.io"
API_PATH_PREFIX = "/api"


# ── .env loader (no dependencies required) ───────────────────────────────────

def load_env(env_path: str = ".env") -> None:
    """Load KEY=VALUE pairs from a .env file into os.environ."""
    path = Path(env_path)
    if not path.exists():
        # Try resolving relative to the script's directory
        path = Path(__file__).parent / env_path
    if not path.exists():
        print(f"[ERROR] .env file not found at {env_path} or {path}")
        print("        Copy scripts/.env.example to scripts/.env and add your SYSTEME_API_KEY.")
        sys.exit(1)

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key:
                os.environ.setdefault(key, value)


# ── HTTP helpers ──────────────────────────────────────────────────────────────

def api_request(
    method: str,
    path: str,
    api_key: str,
    body: dict | None = None,
) -> tuple[int, dict | list | None]:
    """
    Make an HTTPS request to the systeme.io API.
    Returns (status_code, parsed_json_body).
    Never raises on HTTP-level errors — caller checks status.
    """
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    encoded_body: bytes | None = None
    if body is not None:
        encoded_body = json.dumps(body).encode("utf-8")
        headers["Content-Length"] = str(len(encoded_body))

    conn = http.client.HTTPSConnection(BASE_URL, timeout=15)
    try:
        conn.request(method, API_PATH_PREFIX + path, body=encoded_body, headers=headers)
        response = conn.getresponse()
        raw = response.read().decode("utf-8")
        status = response.status

        parsed = None
        if raw.strip():
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                parsed = {"_raw": raw}

        return status, parsed
    except OSError as exc:
        print(f"[ERROR] Network error calling {method} {path}: {exc}")
        return 0, None
    finally:
        conn.close()


def check_response(
    label: str,
    status: int,
    data: dict | list | None,
    expected: int = 201,
) -> dict | None:
    """
    Validate a response. Prints a clear error message on failure.
    Returns the data dict on success, None on failure.
    """
    if status == 0:
        print(f"  [FAIL] {label} — no response received (network error)")
        return None
    if status != expected:
        message = ""
        if isinstance(data, dict):
            message = data.get("message") or data.get("error") or data.get("_raw", "")
        print(f"  [FAIL] {label} — HTTP {status}: {message or str(data)}")
        return None
    return data  # type: ignore[return-value]


# ── Funnel creation ───────────────────────────────────────────────────────────

FUNNEL_STEPS = [
    {"name": "Registration",  "stepType": "squeeze_page"},
    {"name": "Thank You",     "stepType": "thank_you_page"},
    {"name": "Sales / Replay","stepType": "sales_page"},
    {"name": "Checkout",      "stepType": "order_form"},
]


def create_funnel(api_key: str) -> str | None:
    """Create the funnel and return its ID, or None on failure."""
    print("\n[1/3] Creating funnel...")
    status, data = api_request("POST", "/funnels", api_key, {"name": "SoR Summer Webinar 2026"})
    result = check_response("Create funnel", status, data, expected=201)
    if result is None:
        return None
    funnel_id = str(result.get("id", ""))
    print(f"  [OK]  Funnel created — ID: {funnel_id}")
    return funnel_id


def create_funnel_steps(api_key: str, funnel_id: str) -> list[dict]:
    """Add steps to the funnel. Returns list of created step records."""
    print("\n[2/3] Adding funnel steps...")
    created = []
    for step in FUNNEL_STEPS:
        status, data = api_request(
            "POST", f"/funnels/{funnel_id}/steps", api_key, step
        )
        result = check_response(f"  Add step '{step['name']}'", status, data, expected=201)
        if result is not None:
            step_id = str(result.get("id", ""))
            print(f"  [OK]  '{step['name']}' step — ID: {step_id}")
            created.append({"name": step["name"], "stepType": step["stepType"], "id": step_id})
        else:
            created.append({"name": step["name"], "stepType": step["stepType"], "id": None})
    return created


# ── Email campaign creation ───────────────────────────────────────────────────

# delayValue/delayType are relative to the previous email in the campaign sequence,
# except Email 1 which fires on tag trigger (delay 0).
#
# Email 2 (24h before event) and Email 3 (1h before event) cannot be scheduled
# relative to the event date via campaign delays — systeme.io doesn't support
# event-relative scheduling through the email campaign API. These are set here
# with placeholder delays and require manual adjustment in the UI (see notes).

EMAIL_CAMPAIGN_EMAILS = [
    {
        "label": "Email 1 — Confirmation",
        "subject": "You're registered — here's what to expect",
        "preview": "Webinar details inside, plus your free Field Kit is confirmed.",
        "body": (
            "Hi [first name],\n\n"
            "You're in. Here's everything you need before the webinar.\n\n"
            "When it is: [WEBINAR_DATE] at [WEBINAR_TIME] — [TIMEZONE]\n\n"
            "How to join: [WEBINAR_LINK]\n\n"
            "Save that link. We'll send a reminder the day before and an hour before.\n\n"
            "Your free bonuses: Because you registered before August 31, you're getting the "
            "Waste Detective Family Field Kit (normally $17) at no charge. "
            "You'll get download instructions after the webinar. "
            "The \"How Plastic Works\" worksheet is also yours.\n\n"
            "The webinar runs about 45 minutes. It's live, so you can ask questions.\n\n"
            "See you there,\n[YOUR NAME]\nSchool of Recycling"
        ),
        "delayValue": 0,
        "delayType": "hour",
        "note": None,
    },
    {
        "label": "Email 2 — Reminder 24h before",
        "subject": "Your webinar is tomorrow — one thing worth knowing",
        "preview": "Show up tomorrow and you'll see this live with a real family.",
        "body": (
            "Hi [first name],\n\n"
            "Quick reminder: the webinar is tomorrow at [WEBINAR_TIME] [TIMEZONE].\n\n"
            "Join link: [WEBINAR_LINK]\n\n"
            "We're walking through an actual lesson from the curriculum — not a polished demo. "
            "You'll see how the age-path split works when siblings are at different levels.\n\n"
            "Reminder: your free Waste Detective Family Field Kit is still confirmed.\n\n"
            "See you tomorrow,\n[YOUR NAME]\nSchool of Recycling"
        ),
        "delayValue": 0,
        "delayType": "hour",
        "note": (
            "MANUAL STEP REQUIRED: Email 2 should send 24h before the webinar date, "
            "not at a fixed offset from Email 1. Set up a separate automation in systeme.io "
            "triggered by a 'webinar-reminder-24h' tag, or schedule it manually for the day before. "
            "The API does not support event-relative scheduling."
        ),
    },
    {
        "label": "Email 3 — Reminder 1h before",
        "subject": "We start in 1 hour",
        "preview": "Here's your link — no hunting around for it later.",
        "body": (
            "Hi [first name],\n\n"
            "One hour to go.\n\n"
            "Join link: [WEBINAR_LINK]\n\n"
            "We'll start on time at [WEBINAR_TIME] [TIMEZONE].\n\n"
            "If you can only stay for part of it, come for the first 30 minutes. "
            "The replay will be available if you need to catch the rest later.\n\n"
            "See you shortly,\n[YOUR NAME]\nSchool of Recycling"
        ),
        "delayValue": 0,
        "delayType": "hour",
        "note": (
            "MANUAL STEP REQUIRED: Email 3 should send 1h before the webinar. "
            "Set up a separate automation triggered by a 'webinar-reminder-1h' tag, "
            "or schedule it manually for 1 hour before the event start time."
        ),
    },
    {
        "label": "Email 4 — Replay + Offer",
        "subject": "In case you missed it — or want to watch again",
        "preview": "Replay is up. Full offer details inside.",
        "body": (
            "Hi [first name],\n\n"
            "The webinar replay is live: [REPLAY_LINK]\n\n"
            "School of Recycling is $37 for 100 days of access — the full curriculum, "
            "two age paths (6-9 and 10-12), one subscription covers every kid in your family aged 6-12.\n\n"
            "Free bonuses until August 31:\n"
            "- Waste Detective Family Field Kit (normally $17)\n"
            "- \"How Plastic Works\" worksheet\n\n"
            "Both included automatically. No codes. After August 31 the Field Kit won't be included.\n\n"
            "Get access: schoolofrecycling.com\n\n"
            "[YOUR NAME]\nSchool of Recycling"
        ),
        "delayValue": 1,
        "delayType": "day",
        "note": (
            "This email is set to 1 day delay from the previous email in the sequence. "
            "Adjust the trigger in the UI so it fires the day after the live webinar, "
            "not 1 day after Email 3."
        ),
    },
    {
        "label": "Email 5 — Last Chance",
        "subject": "Last reminder — bonuses close August 31",
        "preview": "After that, the curriculum stays. The Field Kit doesn't.",
        "body": (
            "Hi [first name],\n\n"
            "Short one.\n\n"
            "August 31 is the last day the Waste Detective Family Field Kit comes free with "
            "School of Recycling. That's a genuine date — it's a summer offer.\n\n"
            "The curriculum itself ($37, 100 days, both age paths) stays available year-round.\n\n"
            "schoolofrecycling.com\n\n"
            "No more emails after this one.\n\n"
            "[YOUR NAME]\nSchool of Recycling"
        ),
        "delayValue": 2,
        "delayType": "day",
        "note": None,
    },
]


def create_email_campaign(api_key: str) -> str | None:
    """Create the email campaign and return its ID, or None on failure."""
    print("\n[3/3] Creating email campaign...")
    status, data = api_request(
        "POST", "/email-campaigns", api_key,
        {"name": "SoR Webinar — Summer Edition"}
    )
    result = check_response("Create email campaign", status, data, expected=201)
    if result is None:
        return None
    campaign_id = str(result.get("id", ""))
    print(f"  [OK]  Campaign created — ID: {campaign_id}")
    return campaign_id


def create_campaign_emails(api_key: str, campaign_id: str) -> list[dict]:
    """Add all 5 emails to the campaign. Returns list of created email records."""
    print("\n      Adding emails to campaign...")
    created = []
    for email in EMAIL_CAMPAIGN_EMAILS:
        payload = {
            "subject": email["subject"],
            "body": email["body"],
            "delayValue": email["delayValue"],
            "delayType": email["delayType"],
        }
        status, data = api_request(
            "POST", f"/email-campaigns/{campaign_id}/emails", api_key, payload
        )
        result = check_response(f"  Add '{email['label']}'", status, data, expected=201)
        email_id = None
        if result is not None:
            email_id = str(result.get("id", ""))
            print(f"  [OK]  '{email['label']}' — ID: {email_id}")
        else:
            print(f"  [--]  '{email['label']}' was not created — see error above")

        if email.get("note"):
            print(f"\n  [NOTE] {email['note']}\n")

        created.append({
            "label": email["label"],
            "subject": email["subject"],
            "id": email_id,
        })
    return created


# ── Summary ───────────────────────────────────────────────────────────────────

def print_summary(
    funnel_id: str | None,
    steps: list[dict],
    campaign_id: str | None,
    emails: list[dict],
) -> None:
    divider = "─" * 60
    print(f"\n{divider}")
    print("SETUP SUMMARY")
    print(divider)

    print(f"\nFunnel ID:    {funnel_id or '[not created]'}")
    print("\nFunnel steps:")
    for s in steps:
        status_str = s["id"] if s["id"] else "[not created]"
        print(f"  {s['name']:<22} ID: {status_str}")

    print(f"\nEmail campaign ID: {campaign_id or '[not created]'}")
    print("\nEmails:")
    for e in emails:
        status_str = e["id"] if e["id"] else "[not created]"
        print(f"  {e['label']:<34} ID: {status_str}")

    print(f"\n{divider}")
    print("MANUAL STEPS STILL REQUIRED IN SYSTEME.IO UI")
    print(divider)
    manual_steps = [
        "1. Open each funnel step in the page builder and paste copy from funnel/*.md",
        "2. Upload funnel/03_salespage.html to the Sales/Replay step (or paste sections)",
        "3. Set the automation trigger: tag 'webinar-registered' fires Email 1 immediately",
        "4. Schedule Email 2 for 24h before the webinar (event-relative — cannot be set via API)",
        "5. Schedule Email 3 for 1h before the webinar (event-relative — cannot be set via API)",
        "6. Add a Webinar step to the funnel in the UI (not available via API)",
        "7. Upload your video to YouTube or Vimeo and paste the URL into the webinar step",
        "8. Set the webinar schedule (recommended: daily 8pm + 12pm local time)",
        "9. Link the registration page to the webinar room in the funnel builder",
        "10. Replace all [PLACEHOLDER] values in email bodies with real content",
        "11. Add your logo and verify brand colors on all pages",
    ]
    for step in manual_steps:
        print(f"  {step}")

    print(f"\n{divider}\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    # Load .env — try relative to CWD first, then relative to script
    load_env(".env")
    api_key = os.environ.get("SYSTEME_API_KEY", "").strip()

    if not api_key or api_key == "your_api_key_here":
        print("[ERROR] SYSTEME_API_KEY is not set or is still the placeholder value.")
        print("        Edit .env and add your real API key from your systeme.io account.")
        sys.exit(1)

    print("=" * 60)
    print("SoR Summer Webinar 2026 — systeme.io Setup")
    print("=" * 60)

    # Step 1: Create funnel
    funnel_id = create_funnel(api_key)
    steps: list[dict] = []
    if funnel_id:
        steps = create_funnel_steps(api_key, funnel_id)
    else:
        print("  [SKIP] Cannot create funnel steps without a funnel ID.")
        steps = [{"name": s["name"], "stepType": s["stepType"], "id": None} for s in FUNNEL_STEPS]

    # Step 2: Create email campaign
    campaign_id = create_email_campaign(api_key)
    emails: list[dict] = []
    if campaign_id:
        emails = create_campaign_emails(api_key, campaign_id)
    else:
        print("  [SKIP] Cannot create emails without a campaign ID.")
        emails = [{"label": e["label"], "subject": e["subject"], "id": None} for e in EMAIL_CAMPAIGN_EMAILS]

    # Summary
    print_summary(funnel_id, steps, campaign_id, emails)


if __name__ == "__main__":
    main()
