from datetime import datetime, timezone
from functools import wraps

import jwt
from flask import current_app, g, jsonify, request
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from .extensions import db
from .models import User


def verify_google_token(credential: str) -> dict:
    if not current_app.config["GOOGLE_CLIENT_ID"]:
        raise ValueError("GOOGLE_CLIENT_ID is not configured")
    return id_token.verify_oauth2_token(
        credential,
        google_requests.Request(),
        current_app.config["GOOGLE_CLIENT_ID"],
    )


def upsert_google_user(payload: dict) -> User:
    email = payload.get("email", "").lower()
    if not email or not payload.get("sub"):
        raise ValueError("Google token did not include email or subject")

    user = User.query.filter((User.email == email) | (User.google_sub == payload["sub"])).first()
    if not user:
        user = User(email=email, google_sub=payload["sub"])
        db.session.add(user)

    user.name = payload.get("name", user.name or "")
    user.picture = payload.get("picture", user.picture or "")
    user.role = "admin" if email in current_app.config["ADMIN_EMAILS"] else user.role
    db.session.commit()
    return user


def issue_jwt(user: User) -> str:
    now = datetime.now(timezone.utc)
    exp = now + current_app.config["JWT_EXPIRES"]
    return jwt.encode(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
            "iss": current_app.config["JWT_ISSUER"],
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )


def require_auth(admin: bool = False):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization", "")
            token = header.removeprefix("Bearer ").strip()
            if not token:
                return jsonify({"error": {"code": "unauthorized", "message": "Missing bearer token"}}), 401
            try:
                payload = jwt.decode(
                    token,
                    current_app.config["SECRET_KEY"],
                    algorithms=["HS256"],
                    issuer=current_app.config["JWT_ISSUER"],
                )
            except jwt.PyJWTError:
                return jsonify({"error": {"code": "unauthorized", "message": "Invalid bearer token"}}), 401
            user = db.session.get(User, int(payload["sub"]))
            if not user:
                return jsonify({"error": {"code": "unauthorized", "message": "User no longer exists"}}), 401
            if admin and user.role != "admin":
                return jsonify({"error": {"code": "forbidden", "message": "Admin access required"}}), 403
            g.current_user = user
            return fn(*args, **kwargs)

        return wrapper

    return decorator

