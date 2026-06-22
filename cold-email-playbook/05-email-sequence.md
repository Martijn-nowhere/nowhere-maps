# Step 5 — Email Sequence

## Rules

- Plain text only — no images, no links, no signatures, no formatting
- Reply-based CTA — ask them to reply, not click a link
- Short sentences, easy to read on mobile
- Personalization via `{{firstName}}` and `{{companyName}}`
- Sender name is `{{senderFirstName}}` (auto from mailbox)

## Variables

| Variable | Example output |
|----------|---------------|
| `{{firstName}}` | Sarah |
| `{{companyName}}` | Westfield High School |
| `{{senderFirstName}}` | James |

## Email 1 — Cold Intro

**Subject:** free lesson for your class, {{firstName}}

**Body:**

Hi {{firstName}},

I help English teachers add a real-world topic to their lessons without extra prep.

We built a short module on plastic waste — a 10-minute video and two worksheets for your students. It's free for the first 100 days.

Would something like that be useful at {{companyName}}?

{{senderFirstName}}

---

**Delay before Email 2:** 3 days

---

## Email 2 — Follow-up

**Subject:** Re: free lesson for your class, {{firstName}}

**Body:**

Hi {{firstName}},

Just following up in case this got buried.

The module asks students to think about everyday plastic items — where they come from, how they're made, and what happens when they're thrown away. It fits naturally into discussion or writing lessons.

Takes about 30 minutes total. No setup on your end.

Free for the first 100 days. Happy to send the link if you want to take a look.

{{senderFirstName}}

---

**Delay before Email 3:** 4 days

---

## Email 3 — Final Bump

**Subject:** Re: free lesson for your class, {{firstName}}

**Body:**

Hi {{firstName}},

Last message from me on this.

If the timing isn't right or it's not a fit, no worries at all. Just reply "not interested" and I won't follow up again.

If you do want the free module, just say yes and I'll send it over.

{{senderFirstName}}

---

## Sequence Settings in Instantly

| Setting | Value |
|---------|-------|
| Email 1 → Email 2 delay | 3 days |
| Email 2 → Email 3 delay | 4 days |
| Stop on reply | On |
| Stop on auto-reply | On |

## Post-Reply Handling

When a teacher replies positively:

1. Instantly flags the lead as replied — removed from sequence automatically
2. Reply arrives in the sending mailbox (e.g. sarah@schoolofrecycling.org)
3. Reply-To is set to client's main email — teacher's reply is forwarded to client inbox
4. Client gives teacher access to Module 1 (manually or via automated link)
5. Teacher enters nurture sequence in Systeme.io (3 emails over 2 weeks to convert to paid)

## Notes

- Do not add a PS line unless A/B testing warrants it
- Do not mention competitors or compare pricing in cold sequence
- Do not use "I hope this email finds you well" or similar filler
- The free module is for any age group (6–9, 10–12, 13–16, 17+) — no need to specify in email
- Module 1: plastic waste awareness — video + 2 worksheets (WS1: where does plastic come from/how made/where does it go; WS2: is plastic necessary?)
