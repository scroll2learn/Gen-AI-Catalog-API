import pytest
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.db.base import get_db
from app.api.deps import get_context
from app.api.controllers.pipelines import get_all_pipelines
from app.core.context import Context
from fastapi import Request

# Define test database URL
SQLALCHEMY_TEST_DATABASE_URI = "sqlite+aiosqlite:///:memory:"

# Create the SQLAlchemy test engine
test_engine = create_async_engine(SQLALCHEMY_TEST_DATABASE_URI, echo=True, future=True)

# Create a sessionmaker for the test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine, class_=AsyncSession)



@pytest.fixture
async def test_session():
    # Override db session dependency
    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    # Override context dependency
    async def override_get_context():
        ctx = Context()
        async with TestingSessionLocal() as test_session:
            ctx.db_session = test_session
            yield ctx

    # Apply dependency overrides in FastAPI
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_context] = override_get_context

    # Return the test session
    async with TestingSessionLocal() as session:
        yield session

# Create a fixture for initializing the database
@pytest.fixture(scope="function")
async def init_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)  # Create tables
    yield  # Run tests
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)  # Drop tables after tests


