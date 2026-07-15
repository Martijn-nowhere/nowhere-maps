import sqlite3
import json
import os
import psycopg2
from datetime import datetime

DB_PATH = os.environ.get("DB_PATH", "sor.db")
SUPABASE_DB_URL = os.environ.get("SUPABASE_DB_URL", "")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS lessons (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            full_description TEXT NOT NULL,
            age_group TEXT NOT NULL,
            availability TEXT NOT NULL DEFAULT 'available',
            edition TEXT NOT NULL DEFAULT 'both',
            price_home_usd INTEGER NOT NULL DEFAULT 37,
            price_classroom_usd INTEGER NOT NULL DEFAULT 147,
            waste_stream TEXT NOT NULL,
            topic_tags TEXT NOT NULL DEFAULT '[]',
            learning_outcomes TEXT NOT NULL DEFAULT '[]',
            pedagogical_approach TEXT NOT NULL,
            content_types TEXT NOT NULL DEFAULT '[]',
            sdg_alignment TEXT NOT NULL DEFAULT '[]',
            language TEXT NOT NULL DEFAULT 'en',
            duration_per_module_minutes INTEGER NOT NULL DEFAULT 25,
            duration_total_minutes INTEGER NOT NULL DEFAULT 125,
            audience TEXT NOT NULL DEFAULT 'both',
            url TEXT NOT NULL,
            is_free INTEGER NOT NULL DEFAULT 0,
            credential_context TEXT NOT NULL DEFAULT '[]',
            worksheet_descriptions TEXT NOT NULL DEFAULT '[]',
            discussion_prompts TEXT NOT NULL DEFAULT '[]'
        );

        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            organisation TEXT NOT NULL,
            key_hash TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS reply_automation_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            received_at TEXT NOT NULL DEFAULT (datetime('now')),
            dedupe_key TEXT NOT NULL UNIQUE,
            lead_email TEXT NOT NULL,
            campaign_id TEXT,
            reply_subject TEXT,
            reply_text TEXT,
            intent TEXT,
            age_group TEXT,
            language TEXT,
            country TEXT,
            currency TEXT,
            action TEXT NOT NULL DEFAULT 'none',
            tag_applied TEXT,
            systeme_contact_id TEXT,
            error TEXT,
            raw_payload TEXT
        );
    """)

    conn.commit()
    conn.close()


def row_to_dict(row):
    if row is None:
        return None
    d = dict(row)
    for field in ("topic_tags", "learning_outcomes", "content_types",
                  "sdg_alignment", "credential_context",
                  "worksheet_descriptions", "discussion_prompts"):
        if field in d and isinstance(d[field], str):
            d[field] = json.loads(d[field])
    d["is_free"] = bool(d.get("is_free", 0))
    return d


# Supabase (Postgres) functions for reply automation logging
def get_supabase_conn():
    """Connect to Supabase Postgres database."""
    if not SUPABASE_DB_URL:
        raise RuntimeError("SUPABASE_DB_URL is not configured")
    return psycopg2.connect(SUPABASE_DB_URL)


def init_supabase_log_table():
    """Create reply_automation_log table in Supabase if it doesn't exist."""
    if not SUPABASE_DB_URL:
        return
    try:
        conn = get_supabase_conn()
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS reply_automation_log (
                id SERIAL PRIMARY KEY,
                received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                dedupe_key TEXT NOT NULL UNIQUE,
                lead_email TEXT NOT NULL,
                campaign_id TEXT,
                reply_subject TEXT,
                reply_text TEXT,
                intent TEXT,
                age_group TEXT,
                language TEXT,
                country TEXT,
                currency TEXT,
                action TEXT NOT NULL DEFAULT 'none',
                tag_applied TEXT,
                systeme_contact_id TEXT,
                error TEXT,
                raw_payload TEXT
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Warning: Could not initialize Supabase log table: {e}")


def log_reply_to_supabase(dedupe_key, lead_email, campaign_id, reply_subject, reply_text,
                          intent, age_group, language, country, currency, action, tag_applied,
                          systeme_contact_id, error, raw_payload):
    """Log a reply to Supabase instead of SQLite."""
    if not SUPABASE_DB_URL:
        return
    try:
        conn = get_supabase_conn()
        c = conn.cursor()
        c.execute("""
            INSERT INTO reply_automation_log
                (dedupe_key, lead_email, campaign_id, reply_subject, reply_text,
                 intent, age_group, language, country, currency, action, tag_applied,
                 systeme_contact_id, error, raw_payload)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (dedupe_key) DO NOTHING
        """, (dedupe_key, lead_email, campaign_id, reply_subject, reply_text,
              intent, age_group, language, country, currency, action, tag_applied,
              systeme_contact_id, error, raw_payload))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging to Supabase: {e}")


def get_logs_from_supabase(action=None, limit=50):
    """Fetch logs from Supabase."""
    if not SUPABASE_DB_URL:
        return []
    try:
        conn = get_supabase_conn()
        c = conn.cursor()
        if action:
            c.execute("""
                SELECT * FROM reply_automation_log
                WHERE action = %s
                ORDER BY id DESC LIMIT %s
            """, (action, limit))
        else:
            c.execute("""
                SELECT * FROM reply_automation_log
                ORDER BY id DESC LIMIT %s
            """, (limit,))
        rows = c.fetchall()
        conn.close()

        # Convert rows to dicts
        columns = [desc[0] for desc in c.description]
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        print(f"Error fetching logs from Supabase: {e}")
        return []


def get_stats_from_supabase():
    """Fetch aggregate stats from Supabase."""
    if not SUPABASE_DB_URL:
        return {}
    try:
        conn = get_supabase_conn()
        c = conn.cursor()

        c.execute("SELECT COUNT(*) as n FROM reply_automation_log")
        total = c.fetchone()[0]

        c.execute("SELECT action, COUNT(*) as n FROM reply_automation_log GROUP BY action")
        by_action = {row[0]: row[1] for row in c.fetchall()}

        c.execute("""
            SELECT age_group, COUNT(*) as n FROM reply_automation_log
            WHERE action IN ('tagged_module1', 'tagged_module1_currency_pending')
            GROUP BY age_group
        """)
        by_age = {row[0]: row[1] for row in c.fetchall()}

        c.execute("""
            SELECT currency, COUNT(*) as n FROM reply_automation_log
            WHERE action = 'tagged_module1' GROUP BY currency
        """)
        by_currency = {row[0]: row[1] for row in c.fetchall()}

        c.execute("""
            SELECT language, COUNT(*) as n FROM reply_automation_log
            GROUP BY language ORDER BY n DESC
        """)
        by_language = {(row[0] or 'unknown'): row[1] for row in c.fetchall()}

        c.execute("""
            SELECT MAX(received_at) as t FROM reply_automation_log
        """)
        last_received = c.fetchone()[0]

        c.execute("""
            SELECT campaign_id, action, COUNT(*) as n FROM reply_automation_log
            WHERE action LIKE 'tagged_district%' OR action LIKE 'logged_district%'
            GROUP BY campaign_id, action
        """)
        district_by_campaign = {}
        for campaign_id, action, n in c.fetchall():
            district_by_campaign.setdefault(campaign_id or "unknown", {})[action] = n

        conn.close()

        return {
            "total_replies": total,
            "by_action": by_action,
            "module1_by_age_group": by_age,
            "module1_by_currency": by_currency,
            "by_language": by_language,
            "district_by_campaign": district_by_campaign,
            "last_received_at": last_received.isoformat() if last_received else None,
            "errors": by_action.get("error", 0),
            "needs_currency_review": by_action.get("tagged_module1_currency_pending", 0),
        }
    except Exception as e:
        print(f"Error fetching stats from Supabase: {e}")
        return {}
