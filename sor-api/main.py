"""
School of Recycling — Curriculum Intelligence API v1
"""

from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from auth import require_api_key
from database import get_db, init_db, init_supabase_log_table, row_to_dict
from email_automation import router as email_automation_router
from seed_data import seed

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="School of Recycling — Curriculum Intelligence API",
    description=(
        "Machine-readable curriculum data for School of Recycling (SoR), "
        "a K-12 online waste and plastic education platform.\n\n"
        "**Public endpoints** return lesson metadata — no authentication required.\n\n"
        "**Gated endpoints** return full detail including learning outcomes, worksheet "
        "descriptions, and discussion prompts — require `X-API-Key` header.\n\n"
        "**Request an API key:** `POST /request-access`\n\n"
        "**Website:** https://schoolofrecycling.com"
    ),
    version="1.0.0",
    contact={
        "name": "School of Recycling",
        "url": "https://schoolofrecycling.com",
        "email": "hello@schoolofrecycling.com",
    },
    license_info={"name": "Proprietary — © SoR LLC"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


app.include_router(email_automation_router)


@app.on_event("startup")
def startup():
    init_db()
    seed()
    init_supabase_log_table()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

PUBLIC_FIELDS = {
    "id", "title", "description", "age_group", "availability", "edition",
    "price_home_usd", "price_classroom_usd", "waste_stream", "topic_tags",
    "pedagogical_approach", "content_types", "sdg_alignment", "language",
    "duration_per_module_minutes", "duration_total_minutes", "audience",
    "url", "is_free", "credential_context",
}

SDG_LABELS = {
    4: "Quality Education",
    8: "Decent Work and Economic Growth",
    10: "Reduced Inequalities",
    11: "Sustainable Cities and Communities",
    12: "Responsible Consumption and Production",
    13: "Climate Action",
    14: "Life Below Water",
    17: "Partnerships for the Goals",
}


def to_public(lesson: dict) -> dict:
    return {k: v for k, v in lesson.items() if k in PUBLIC_FIELDS}


def query_lessons(
    age_group: Optional[str] = None,
    waste_stream: Optional[str] = None,
    sdg: Optional[int] = None,
    availability: Optional[str] = None,
    is_free: Optional[bool] = None,
    audience: Optional[str] = None,
) -> list[dict]:
    conditions, params = [], []

    if sdg is not None:
        base = "SELECT l.* FROM lessons l, json_each(l.sdg_alignment) je"
        conditions.append("CAST(je.value AS INTEGER) = ?")
        params.append(sdg)
    else:
        base = "SELECT * FROM lessons l"

    if age_group:
        conditions.append("l.age_group = ?")
        params.append(age_group)
    if waste_stream:
        conditions.append("l.waste_stream = ?")
        params.append(waste_stream)
    if availability:
        conditions.append("l.availability = ?")
        params.append(availability)
    if is_free is not None:
        conditions.append("l.is_free = ?")
        params.append(1 if is_free else 0)
    if audience:
        conditions.append("(l.audience = ? OR l.audience = 'both')")
        params.append(audience)

    where = (" WHERE " + " AND ".join(conditions)) if conditions else ""
    sql = base + where + " ORDER BY l.age_group, l.id"

    conn = get_db()
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]


def _check_api_key(request: Request) -> bool:
    """Returns True if a valid API key is present, False if absent, raises 403 if invalid."""
    key = request.headers.get("X-API-Key")
    if not key:
        return False
    require_api_key(key)
    return True


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class AccessRequest(BaseModel):
    email: EmailStr
    organisation: str


# ---------------------------------------------------------------------------
# Public endpoints
# ---------------------------------------------------------------------------

@app.api_route("/healthz", methods=["GET", "HEAD"], include_in_schema=False)
def healthz():
    return {"status": "ok"}


@app.get("/about", tags=["Public"], summary="Machine-readable SoR organisation profile")
def about():
    return {
        "name": "School of Recycling",
        "legal_entity": "SoR LLC",
        "tagline": "Teaching children how waste systems actually work, starting with plastic.",
        "mission": (
            "School of Recycling provides K-12 curriculum that builds accurate mental models "
            "of waste systems — emphasising systems thinking, critical inquiry, and real-world "
            "trade-offs over simplified rules."
        ),
        "website": "https://schoolofrecycling.com",
        "contact_email": "hello@schoolofrecycling.com",
        "memberships": ["UNEP GPML", "UN Global Compact"],
        "sdgs_addressed": [4, 10, 11, 12, 13, 14, 17],
        "languages_v1": ["en"],
        "subject_areas": [
            "waste management", "plastic pollution", "circular economy",
            "environmental education", "systems thinking",
        ],
        "audience": "K-12 students, home educators, classroom teachers",
        "editions": {
            "home": {"price_usd": 37, "description": "For home learners and individual families"},
            "classroom": {"price_usd": 147, "description": "For schools and teachers — multi-student licence"},
        },
        "content_per_course": {
            "video_modules": 5,
            "pdf_worksheets": 10,
            "discussion_prompts": "included per module",
            "reflection_questions": "included per module",
            "activities": "included per module",
        },
        "api": {
            "version": "1.0.0",
            "base_url": "https://api.schoolofrecycling.com",
            "docs": "https://api.schoolofrecycling.com/docs",
            "request_access": "POST /request-access",
        },
    }


@app.get("/age-groups", tags=["Public"], summary="Age groups with availability status and lesson counts")
def age_groups():
    conn = get_db()
    rows = conn.execute("""
        SELECT age_group,
               COUNT(*) AS lesson_count,
               SUM(CASE WHEN availability = 'available' THEN 1 ELSE 0 END) AS available_count
        FROM lessons
        GROUP BY age_group
        ORDER BY age_group
    """).fetchall()
    conn.close()
    result = []
    for r in rows:
        ag = dict(r)
        ag["status"] = "available" if ag["available_count"] > 0 else "coming_soon"
        result.append(ag)
    return result


@app.get("/waste-streams", tags=["Public"], summary="Waste streams covered with availability status")
def waste_streams():
    conn = get_db()
    rows = conn.execute("""
        SELECT waste_stream,
               COUNT(*) AS lesson_count,
               SUM(CASE WHEN availability = 'available' THEN 1 ELSE 0 END) AS available_count
        FROM lessons
        GROUP BY waste_stream
        ORDER BY waste_stream
    """).fetchall()
    conn.close()
    result = []
    for r in rows:
        ws = dict(r)
        ws["status"] = "available" if ws["available_count"] > 0 else "coming_soon"
        result.append(ws)
    return result


@app.get("/sdgs", tags=["Public"], summary="SDGs covered and which lessons map to each")
def sdgs():
    conn = get_db()
    rows = conn.execute("""
        SELECT CAST(je.value AS INTEGER) AS sdg_number,
               GROUP_CONCAT(l.id) AS lesson_ids,
               COUNT(*) AS lesson_count
        FROM lessons l, json_each(l.sdg_alignment) je
        WHERE l.availability = 'available'
        GROUP BY sdg_number
        ORDER BY sdg_number
    """).fetchall()
    conn.close()
    return [
        {
            "sdg": r["sdg_number"],
            "label": SDG_LABELS.get(r["sdg_number"], f"SDG {r['sdg_number']}"),
            "lesson_count": r["lesson_count"],
            "lesson_ids": r["lesson_ids"].split(",") if r["lesson_ids"] else [],
        }
        for r in rows
    ]


@app.get(
    "/lessons",
    tags=["Public", "Gated"],
    summary="List lessons — filterable. Provide X-API-Key + full=true for gated detail.",
)
def list_lessons(
    request: Request,
    age_group: Optional[str] = Query(None, description="6-9 | 10-12 | 13-16 | 17+"),
    waste_stream: Optional[str] = Query(None, description="plastic | organic | e-waste | textile"),
    sdg: Optional[int] = Query(None, description="SDG number, e.g. 12"),
    availability: Optional[str] = Query(None, description="available | coming_soon"),
    is_free: Optional[bool] = Query(None, description="true = free lessons only"),
    audience: Optional[str] = Query(None, description="home_learner | classroom"),
    full: bool = Query(False, description="Include gated fields (requires X-API-Key)"),
):
    lessons = query_lessons(age_group, waste_stream, sdg, availability, is_free, audience)

    if full:
        key = request.headers.get("X-API-Key")
        if not key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="X-API-Key header is required when full=true.",
            )
        require_api_key(key)
        return lessons

    return [to_public(l) for l in lessons]


@app.get("/lessons/{lesson_id}", tags=["Public"], summary="Public metadata for a single lesson")
def get_lesson(lesson_id: str):
    conn = get_db()
    row = conn.execute("SELECT * FROM lessons WHERE id = ?", (lesson_id,)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Lesson '{lesson_id}' not found.")
    return to_public(row_to_dict(row))


@app.get("/search", tags=["Public"], summary="Keyword search across title, description, and topic_tags")
def search(q: str = Query(..., min_length=1, description="Search query")):
    term = f"%{q}%"
    conn = get_db()
    rows = conn.execute("""
        SELECT * FROM lessons
        WHERE title LIKE ?
           OR description LIKE ?
           OR topic_tags LIKE ?
        ORDER BY availability DESC, age_group
    """, (term, term, term)).fetchall()
    conn.close()
    return [to_public(row_to_dict(r)) for r in rows]


@app.post(
    "/request-access",
    tags=["Public"],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit email + organisation to request an API key — reviewed manually by SoR",
)
def request_access(body: AccessRequest):
    conn = get_db()
    conn.execute(
        "INSERT INTO api_keys (email, organisation) VALUES (?, ?)",
        (body.email, body.organisation),
    )
    conn.commit()
    conn.close()
    return {
        "status": "received",
        "message": (
            "Your request has been received. SoR reviews all access requests manually "
            "and will contact you at the email provided. Typical response: 2–3 business days."
        ),
        "email": body.email,
        "organisation": body.organisation,
    }


# ---------------------------------------------------------------------------
# Gated endpoints
# ---------------------------------------------------------------------------

@app.get(
    "/lessons/{lesson_id}/full",
    tags=["Gated"],
    summary="Full lesson detail including learning outcomes, worksheets, and discussion prompts",
)
def get_lesson_full(lesson_id: str, _key: str = Depends(require_api_key)):
    conn = get_db()
    row = conn.execute("SELECT * FROM lessons WHERE id = ?", (lesson_id,)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Lesson '{lesson_id}' not found.")
    return row_to_dict(row)
