# SoR Summer Webinar Funnel — Launch Guide

**Offer:** School of Recycling · $37 · 100 days access · Ages 6–9 and 10–12
**Bonus deadline:** August 31 (Summer Edition)
**Platform:** systeme.io

---

## What Was Built

| File | What it is |
|---|---|
| `slides/webinar_slides.html` | 23-slide presenter deck — open in browser, press N for speaker notes |
| `funnel/01_registration_copy.md` | Copy blocks to paste into systeme.io registration page |
| `funnel/02_thankyou_copy.md` | Copy blocks for the thank-you / confirmation page |
| `funnel/03_salespage.html` | Full sales/replay page HTML |
| `emails/sequences.md` | All 5 emails: confirmation, 2 reminders, replay+offer, last chance |
| `scripts/setup_systeme.py` | Python script — creates funnel skeleton + email campaign via API |
| `scripts/.env.example` | Copy to `.env` and add your API key before running the script |

---

## Step-by-Step: How to Launch

### Step 1 — Record the webinar
1. Open `slides/webinar_slides.html` in Chrome or Firefox
2. Press **N** to show speaker notes (visible only to you)
3. Navigate with arrow keys or spacebar
4. Record your screen with Loom, Zoom, OBS, or QuickTime
5. Upload to YouTube (unlisted) or Vimeo — save the URL

### Step 2 — Run the API setup script
```bash
cd webinar/scripts
cp .env.example .env
# Edit .env — paste your SYSTEME_API_KEY
pip install requests python-dotenv
python setup_systeme.py
```
Script prints funnel ID + campaign ID. Save them.

### Step 3 — Build pages in systeme.io UI
The API creates page shells. You fill in content in the builder.

- **Registration page:** use copy from `funnel/01_registration_copy.md`
- **Thank-you page:** use copy from `funnel/02_thankyou_copy.md`
- **Sales/replay page:** open `funnel/03_salespage.html` in a browser to preview it, then either paste the full HTML into a custom HTML block in systeme.io, or copy sections manually

### Step 4 — Set up email sequences in systeme.io UI
1. Open the campaign the script created
2. Paste each email from `emails/sequences.md`
3. Set trigger: tag `webinar-registered` → Email 1 immediately
4. Email 2: 23h delay | Email 3: 47h delay | Email 4: 1 day after webinar ends | Email 5: 3 days

### Step 5 — Set up the automated webinar room (UI only)
1. Funnels → your funnel → Add step → Webinar
2. Paste your YouTube/Vimeo URL
3. Set schedule (recommended: daily 12pm + 8pm)
4. Link registration page to webinar room
5. Set a `watched-webinar` tag to fire at session end (triggers replay emails)

### Step 6 — Test before going live
- [ ] Register as test contact — Email 1 arrives immediately
- [ ] Thank-you page loads after registration
- [ ] Webinar room plays video on schedule
- [ ] CTA button on sales page goes to checkout
- [ ] Test purchase grants access + delivers bonuses
- [ ] Email 4 fires after `watched-webinar` tag is set
- [ ] August 31 date appears correctly on sales page and Email 5

---

## Manual Steps Required in systeme.io UI
- Page content (copy + design) for all funnel steps
- Automation trigger rules
- Webinar room (video URL, schedule, end-of-session tag)
- Checkout linked to $37 product

---

## Webinar 2 — Year-Round Edition (after August 31)
Clone this funnel, then:
1. Change scarcity copy: "bonuses available 48h after you watch" (not August 31)
2. Update Email 5 to reflect 48h window
3. Remove summer-specific language from registration headline
4. Set webinar to run year-round
