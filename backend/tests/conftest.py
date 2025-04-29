import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.models import Base
from app.db.session import get_db


# ---------- FIXTURE: FastAPI TestClient (for non-DB API testing) ----------

@pytest.fixture(scope="module")
def test_client():
    """Basic FastAPI TestClient without DB override."""
    return TestClient(app)


# ---------- FIXTURE: Mock DB (for unit tests) ----------

@pytest.fixture
def mock_db():
    """Mock SQLAlchemy session."""
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    db.query.return_value.all.return_value = []
    return db


# ---------- FIXTURE: In-memory SQLite DB session ----------

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Provides a transactional test DB session with fresh tables."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


# ---------- FIXTURE: TestClient with DB override ----------

@pytest.fixture(scope="function")
def test_client_with_db(db_session):
    """FastAPI TestClient with dependency override to use in-memory DB."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

