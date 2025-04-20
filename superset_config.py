import os

# AUTH_TYPE = "AUTH_DB"
SECRET_KEY = os.environ.get("SUPERSET_SECRET_KEY", "fallback-key")
PUBLIC_ROLE_LIKE_GAMMA = True

FEATURE_FLAGS = {
    "ALERT_REPORTS": True,
    "EMBEDDED_SUPERSET": True,
}

# Dashboard embedding
GUEST_ROLE_NAME = "Public"
GUEST_TOKEN_JWT_SECRET = os.environ.get("GUEST_TOKEN_JWT_SECRET", "fallback-secret")
HTTP_HEADERS={"X-Frame-Options":"ALLOWALL"}

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "fallback-uri")
