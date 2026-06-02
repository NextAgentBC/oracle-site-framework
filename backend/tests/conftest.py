"""Shared fixtures: a throwaway app on a temp SQLite DB, a test client, and an
admin bearer token — so route-level tests can exercise the real API surface
without Postgres."""
import pytest

from app.auth import issue_jwt
from app.config import Config
from app.extensions import db as _db
from app.main import create_app
from app.models import User


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = "test-secret"
    ADMIN_EMAILS = {"admin@test.local"}
    SITE_LOCALES = ["en", "zh"]
    SITE_DEFAULT_LOCALE = "en"
    WEBCHAT_ENABLED = False
    REVISION_HISTORY = 5  # small cap so pruning is observable in tests


@pytest.fixture
def app(tmp_path):
    TestConfig.SQLALCHEMY_DATABASE_URI = f"sqlite:///{tmp_path / 'test.db'}"
    application = create_app(TestConfig)
    with application.app_context():
        _db.create_all()
        yield application
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth(app):
    """Authorization header for an admin bearer token."""
    with app.app_context():
        user = User(email="admin@test.local", google_sub="cli:admin@test.local",
                    name="Admin", role="admin")
        _db.session.add(user)
        _db.session.commit()
        token = issue_jwt(user)
    return {"Authorization": f"Bearer {token}"}
