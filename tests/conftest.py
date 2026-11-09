from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database.base import Base
from database.db import get_db
from main import app
from security.config import settings


@pytest.fixture
def database():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    try:
        yield session_factory
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def client(database, monkeypatch) -> Iterator[TestClient]:
    monkeypatch.setattr(settings, "SECRET_KEY", "test-secret-key", raising=False)

    def override_get_db():
        with database() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def auth_headers():
    from security.utils import create_access_token

    def make_headers(email: str) -> dict[str, str]:
        token = create_access_token({"user_email": email})
        return {"Authorization": f"Bearer {token}"}

    return make_headers
