# Step 2 — Google Workspace Mailboxes

## Why Google Workspace

Google has the highest inbox placement rate (87.2%) for cold email. Zoho and other SMTP providers get flagged by Instantly's warmup pool. Always use Google.

## Setup

1. Go to workspace.google.com
2. Sign up for **Business Starter** ($6/user/month)
3. Use sending domain 1 as primary domain (e.g. schoolofrecycling.org)
4. Add sending domain 2 as secondary domain (e.g. schoolofrecycling.co)

**Important:** Create a separate Google Workspace account for sending — do not add sending domains to the client's existing Workspace account (plan mismatch causes pricing issues).

## Create 10 Mailboxes

Split 5 per domain. Use generic first names, surname = client brand abbreviation.

Example:
| Email | First Name | Last Name |
|-------|-----------|-----------|
| sarah@schoolofrecycling.org | Sarah | SoR |
| james@schoolofrecycling.org | James | SoR |
| emma@schoolofrecycling.org | Emma | SoR |
| tom@schoolofrecycling.org | Tom | SoR |
| cathy@schoolofrecycling.org | Cathy | SoR |
| anna@schoolofrecycling.co | Anna | SoR |
| mark@schoolofrecycling.co | Mark | SoR |
| julia@schoolofrecycling.co | Julia | SoR |
| david@schoolofrecycling.co | David | SoR |
| kate@schoolofrecycling.co | Kate | SoR |

**Tips:**
- Set "Email for sign-in instructions" to client's main email so all passwords arrive in one inbox
- Use auto-generated passwords, save them all before closing each screen
- Do not use the client's own name as one of the sending accounts — confusing when they reply

## DKIM Setup

Google Admin → Apps → Google Workspace → Gmail → Authenticate email → Generate DKIM key → add TXT record to GoDaddy → Start Authentication.

Do this for both sending domains.

## OAuth for Instantly

Google Admin → Security → API controls → App access control → Configure new app → search for Instantly OAuth Email v1 using their Client ID → set scope to All users → Trusted access.

Do this once per domain.

## Per-Account Setup Tasks (do all at once)

For each of the 10 accounts:
1. Log in and change password on first login
2. Set Reply-To to client's main brand email (e.g. martijn@schoolofrecycling.com)

Reply-To setup: Gmail settings → See all settings → Accounts → Send mail as → edit → Reply-To address.
