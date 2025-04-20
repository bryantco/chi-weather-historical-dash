import os

AUTH_TYPE = "AUTH_DB"
SECRET_KEY = os.environ.get("SUPERSET_SECRET_KEY", "fallback-key")
PUBLIC_ROLE_LIKE_GAMMA = True

FEATURE_FLAGS = {
    "ALERT_REPORTS": True,
    "EMBEDDED_SUPERSET": True,
    "VERSIONED_EXPORT": False
}

# Dashboard embedding
GUEST_ROLE_NAME = "Public"
GUEST_TOKEN_JWT_SECRET = os.environ.get("GUEST_TOKEN_JWT_SECRET")
HTTP_HEADERS={"X-Frame-Options":"ALLOWALL"}
