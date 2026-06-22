# Step 6 — Client Onboarding & Handover

## Principle

Every account, subscription, and domain should be owned by the client from day one. You set it up, they own it. That way handover is clean and you are never stuck as the middleman for billing or access.

---

## Account Ownership Rules

| Tool | Account owner | Notes |
|------|--------------|-------|
| GoDaddy (sending domains) | Client | Buy domains on their account, not yours |
| Google Workspace | Client | New account separate from existing Workspace |
| Instantly | Client | Their own account, you get added as team member |
| Apollo | Client | Their account, you get added as user |

Never put client tools on your own accounts. If you do, you own the renewal, the billing, and the offboarding problem.

---

## Credit Card & Billing

**Rule:** Client's card pays for all tools from day one.

**How to handle setup:**

1. Create all accounts with the client present (video call or async with Loom)
2. Client enters their own credit card during each signup
3. You handle the technical configuration — they handle the payment

If the client is not technical enough to do this live: have them share their card details securely (use a one-time share tool like privnote.com), add it yourself, then delete the note. Never store client card details.

**Monthly costs to communicate upfront:**

| Tool | Monthly cost |
|------|-------------|
| Google Workspace Starter (10 users) | ~$50 |
| Instantly Hyper Growth | $97 |
| Apollo (basic) | $49 |
| LeadMash (per campaign, one-off) | $6 per 1,000 leads |
| GoDaddy domains (annual, amortised) | ~$3 |
| **Total** | **~$200/month** |

---

## DNS Access During Setup

Client keeps GoDaddy login. During the DNS setup session (30 min, video call):

1. You tell them exactly which records to add (copy-paste from `01-domains-dns.md`)
2. They add the records
3. GoDaddy SMS verification goes to their phone — they confirm it
4. You verify propagation on dnschecker.org

This keeps DNS fully in their hands from the start. No delegation needed.

---

## Your Access During the Project

You need temporary access to:
- Google Workspace admin (to configure DKIM, OAuth, mailboxes)
- Instantly (to set up warmup, campaign, sequence)
- Apollo (to build lead searches)

**How to get access without taking over the account:**

- Google Workspace: client adds you as an admin user, removes you at handover
- Instantly: client adds you as a team member, removes you at handover
- Apollo: client adds you as a user, removes you at handover

Never ask for the owner login. Always work as a team member or admin user.

---

## What You Deliver

At the end of the engagement, hand over a package containing:

### 1. Account Summary Doc
One page per tool:
- Tool name and URL
- Login email
- Where to find the password (their password manager)
- What it does in the system
- Who to contact for support

### 2. DNS Records Reference
All DNS records currently active for each sending domain. So if they ever need to change registrars or something breaks, they know what should be there.

### 3. Campaign Settings Reference
- Sending limits, schedule, warmup settings
- Which mailboxes are on which domain
- Reply-To configuration

### 4. Runbook (monthly tasks)
What the client needs to do themselves to keep it running:

| Task | Frequency | Where |
|------|-----------|-------|
| Check warmup scores | Weekly | Instantly → Mailboxes |
| Check DMARC reports | Weekly | Email (sent to rua address) |
| Monitor campaign reply rate | Weekly | Instantly → Analytics |
| Upload new lead batch | Per campaign wave | Instantly → Leads |
| Pause campaign before school holidays | Per school calendar | Instantly → Campaign |
| Renew sending domains | Annually | GoDaddy |

### 5. This Playbook
Hand over a copy of this full playbook. It contains everything needed to understand, maintain, or rebuild the system from scratch.

---

## Removing Your Access

At handover:
1. Google Workspace: client removes your admin account
2. Instantly: client removes you from team members
3. Apollo: client removes you as user
4. Confirm in writing (email) that access has been removed

---

## Avoiding Lock-in (Your Side)

- Do not use your own domains as sending domains
- Do not put client accounts under your agency billing
- Do not use proprietary tools that only you can access
- Do not be the only person who knows the passwords

If you follow the ownership rules above, any client can continue without you on day one of handover. That is the goal.
