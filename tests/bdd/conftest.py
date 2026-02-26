"""
BDD test configuration.

All step functions must be synchronous — pytest-bdd 8.x does not await async
step functions even with asyncio_mode = "auto". Steps use sync_client
(starlette.testclient.TestClient) which runs the ASGI app in its own event loop.

asyncio_mode = "auto" is still required for session-scoped async fixtures that
set up the test database engine.
"""
import asyncio
import os
import sqlite3

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from starlette.testclient import TestClient

from src.db.base import Base
from src.db.session import get_db
from src.main import app

BDD_TEST_DB_PATH = "./test_bdd.db"
BDD_TEST_DATABASE_URL = f"sqlite+aiosqlite:///{BDD_TEST_DB_PATH}"


@pytest.fixture(scope="session")
def bdd_engine():
    engine = create_async_engine(BDD_TEST_DATABASE_URL, echo=False)

    async def _setup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(_setup())
    yield engine

    async def _teardown():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()

    asyncio.run(_teardown())
    if os.path.exists(BDD_TEST_DB_PATH):
        os.remove(BDD_TEST_DB_PATH)


@pytest.fixture
def sync_client(bdd_engine):
    session_factory = async_sessionmaker(
        bdd_engine, class_=AsyncSession, expire_on_commit=False
    )

    async def override_get_db():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app, raise_server_exceptions=False) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def clean_bdd_db(bdd_engine):
    yield
    conn = sqlite3.connect(BDD_TEST_DB_PATH)
    conn.execute("DELETE FROM users")
    conn.commit()
    conn.close()
