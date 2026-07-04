import sqlite3
import json
import os

DB_PATH = os.environ.get("DB_PATH", "sor.db")


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
