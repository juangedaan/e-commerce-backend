import pytest
from unittest.mock import MagicMock
from app.services.user_service import create_user, get_user_by_id
from app.schemas.user import UserCreate
from app.db.models import User


def test_create_user():
    db = MagicMock()
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()

    user_data = UserCreate(username="testuser", email="test@example.com")

    # Run service
    user = create_user(user_data, db)

    assert user.username == "testuser"
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


def test_get_user_by_id():
    # Mock a user row and a query
    fake_user = User(id=1, username="testuser", email="test@example.com")
    db = MagicMock()
    query = db.query.return_value
    query.filter.return_value.first.return_value = fake_user

    result = get_user_by_id(1, db)

    assert result == fake_user
    db.query.assert_called_once()

