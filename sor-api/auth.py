import hashlib
import os
from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from database import get_db

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

MASTER_KEY = os.environ.get("SOR_MASTER_KEY", "")


def _hash_key(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()


def is_valid_key(api_key: str) -> bool:
    if not api_key:
        return False

    key_hash = _hash_key(api_key)

    if MASTER_KEY and key_hash == _hash_key(MASTER_KEY):
        return True

    conn = get_db()
    row = conn.execute(
        "SELECT id FROM api_keys WHERE key_hash = ? AND status = 'approved'",
        (key_hash,),
    ).fetchone()
    conn.close()
    return row is not None


def require_api_key(api_key: str = Security(API_KEY_HEADER)) -> str:
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-API-Key header is required for this endpoint.",
        )
    if not is_valid_key(api_key):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or unapproved API key. Request access at POST /request-access.",
        )
    return api_key
