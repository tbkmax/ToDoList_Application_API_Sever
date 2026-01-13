import sys
import os
import asyncio
import uuid
from unittest.mock import AsyncMock, Mock

# Ensure backend-api package root is on sys.path so imports like `models` work when pytest runs
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import types

# If `passlib` isn't installed in this environment, provide a tiny mock so imports succeed
if "passlib" not in sys.modules:
    passlib_mod = types.ModuleType("passlib")
    context_mod = types.ModuleType("passlib.context")

    class CryptContext:
        def __init__(self, schemes=None, deprecated=None):
            pass

        def hash(self, pwd: str) -> str:
            return f"hashed-{pwd}"

    context_mod.CryptContext = CryptContext
    passlib_mod.context = context_mod
    sys.modules["passlib"] = passlib_mod
    sys.modules["passlib.context"] = context_mod

from models.models import User
from schemas.schemas import UserCreate, UserUpdate
from crud.crud import create_user, get_user_by_email, update_user, delete_user


class DummyResult:
    def __init__(self, value=None, rowcount: int | None = None):
        self._value = value
        self.rowcount = rowcount

    def scalar_one_or_none(self):
        return self._value


def test_create_user_calls_db_methods():
    async def run():
        mock_db = AsyncMock()
        # `AsyncSession.add()` is a regular method (not awaited), so mock it with Mock()
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        user_in = UserCreate(email="test@example.com", password="s3cret")

        created = await create_user(mock_db, user_in)

        assert created.email == "test@example.com"
        assert hasattr(created, "password_hash")
        assert created.password_hash != "s3cret"
        mock_db.add.assert_called()
        mock_db.commit.assert_awaited()
        mock_db.refresh.assert_awaited()

    asyncio.run(run())


def test_get_user_by_email_returns_user():
    async def run():
        user = User(email="me@example.com", password_hash="h")
        mock_db = AsyncMock()
        mock_db.execute = AsyncMock(return_value=DummyResult(user))

        got = await get_user_by_email(mock_db, "me@example.com")
        assert got is user
        mock_db.execute.assert_awaited()

    asyncio.run(run())


def test_update_user_returns_updated_user_and_commits():
    async def run():
        user_id = uuid.uuid4()
        updated_user = User(email="updated@example.com", password_hash="h")

        # First execute (the update) can return any object; second (get_user) should return DummyResult(updated_user)
        mock_db = AsyncMock()
        mock_db.execute = AsyncMock(side_effect=[DummyResult(None), DummyResult(updated_user)])
        mock_db.commit = AsyncMock()

        upd = UserUpdate(email="updated@example.com", password="newpw")
        result = await update_user(mock_db, user_id, upd)

        assert result is updated_user
        mock_db.commit.assert_awaited()

    asyncio.run(run())


def test_delete_user_returns_true_when_row_deleted():
    async def run():
        mock_db = AsyncMock()
        mock_db.execute = AsyncMock(return_value=DummyResult(None, rowcount=1))
        mock_db.commit = AsyncMock()

        ok = await delete_user(mock_db, uuid.uuid4())
        assert ok is True
        mock_db.commit.assert_awaited()

    asyncio.run(run())
