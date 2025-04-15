import asyncio
from unittest.mock import AsyncMock, patch, PropertyMock
from app.api.deps import get_context
from app.core.config import Config
from app.db.base import get_db
from app.main import app
from app.utils.auth_wrapper import authorize
from httpx import AsyncClient
import pytest
from app.core.context import Context

from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import text
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker


bh_project_data = {
    "bh_project_name": "test project",
    "bh_github_provider": 4100,
    "bh_github_username": "username",
    "bh_github_email": "test@testexample.com",
    "bh_default_branch": "main",
    "bh_github_url": "https://github.com/username/repo",
    "bh_github_token_url": "testtokentest",
    "tags": {}
}

# client = TestClient(app)
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine

from sqlalchemy.ext.asyncio import create_async_engine
from typing import AsyncIterator

@pytest.fixture(scope="module")
def override_context():
    # Async and sync engines
    async_engine = create_async_engine(
        "postgresql+asyncpg://postgres:postgres@catalog-db/test_db",
        echo=True,
        future=True,
    )
    sync_engine = create_engine(
        "postgresql://postgres:postgres@catalog-db/test_db",
        echo=True,
        future=True,
    )

    AsyncSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession,
    )

    async def get_test_db_session() -> AsyncSession:
        async with AsyncSessionLocal() as session:
            yield session

    async def get_test_context():
        async with Context() as ctx:
            ctx._db_session = AsyncSessionLocal() 
            yield ctx

    # Override dependencies
    app.dependency_overrides[get_db] = get_test_db_session
    app.dependency_overrides[get_context] = get_test_context
    
    # Create schema and tables
    with sync_engine.begin() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS catalogdb"))
        SQLModel.metadata.create_all(bind=connection)

    yield  # Run tests here

    # Cleanup
    with sync_engine.begin() as connection:
        SQLModel.metadata.drop_all(bind=connection)
        connection.execute(text("DROP SCHEMA IF EXISTS catalogdb CASCADE"))
    app.dependency_overrides.clear()


@pytest.mark.asyncio
@patch('app.api.controllers.bh_project.decrypt_string')  # Mock decrypt_string
@patch('app.api.controllers.bh_project.GitWrapper')  # Mock GitWrapper class
@patch('app.api.controllers.bh_project.Context.aws_service', new_callable=PropertyMock)  # Mock aws_service
async def test_create_project(mock_aws_service, mock_git_wrapper, mock_decrypt, override_context):
    # Mock decrypt_string behavior
    mock_decrypt.return_value = "decrypted_token"

    # Mock the GitWrapper methods
    mock_git_instance = AsyncMock()  # Create a mock instance of GitWrapper
    mock_git_wrapper.return_value = mock_git_instance
    mock_git_instance.create_branch.return_value = {"status": 201}  # Mock create_branch method

    # Mock aws_service.secrets.new_secret behavior
    mock_aws_service.return_value.secrets.new_secret = AsyncMock(
        return_value=("mock_secret", "mock_version")
    )
    token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ3N0hRZ1BKR3YyMDZHclRrbG1lODN2TXFGV0VLT01MUGRaVVlRS2VEZW5zIn0.eyJleHAiOjE3MzQwMjA0NTIsImlhdCI6MTczMzk4NDQ1MiwiYXV0aF90aW1lIjoxNzMzOTg0NDUxLCJqdGkiOiI1OGZlMjNjNi1kZDg5LTRmYzUtODI3OS02OWFjNWRmODdiMDMiLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwODAvcmVhbG1zL2JpZ2hhbW1lci1yZWFsbSIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiJmYWIxNGNlOC1lZTE2LTQ3YTUtODI3MS0yZGZiZDk4YWFmYWYiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJiaWdoYW1tZXItdWkiLCJub25jZSI6Ijk3YjdkYjgxLWUxMDYtNGVmOS04NGQ5LWVmMjM0NTAwODE2OSIsInNlc3Npb25fc3RhdGUiOiJkNGQ0NTQ4NS0yYWZjLTQwOWItYjZiNy0wMmM0ZmQ1ZjJmYTEiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbImRlc2lnbmVyLXVzZXIiLCJkZWZhdWx0LXJvbGVzLWJpZ2hhbW1lci1yZWFsbSIsIm9mZmxpbmVfYWNjZXNzIiwiYWRtaW4tdXNlciIsInVtYV9hdXRob3JpemF0aW9uIiwib3BzLXVzZXIiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwic2lkIjoiZDRkNDU0ODUtMmFmYy00MDliLWI2YjctMDJjNGZkNWYyZmExIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJCaWdoYW1tZXIgQWRtaW4iLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJiaWdoYW1tZXItYWRtaW4iLCJnaXZlbl9uYW1lIjoiQmlnaGFtbWVyIiwiZmFtaWx5X25hbWUiOiJBZG1pbiIsImVtYWlsIjoiaW5mb0BiaWdoYW1tZXIuYWkifQ.cavXV_xAEA4lAJoq4NexStHk33O6hxKi7wj8-u5GhNnuahm51JSiZ0vzANexJ_yRxP4mlnKcOBZWAEkvQw213mI5y62Xaf508eQml_R3QoadOi05DOrI8xzvePSlG_uHOuK7zyGDusG7outMwtktUJB5B2cFXEIqiSjxWwujUmevgj4sJSDuBF3A6W0QRQrkCmtpRpq8DT7Wi6ByvX5Wg6YNozfbTr0N2qF_Zv5kS1ysb1-FyF_iVzXhc0_O1dteXwFahopqYfCc_5JOSLr6fVt90bBHyzCoqY3IhABQ74QE8KaTHF62G7tXQhXdbgvl5vh9MBiIRS5T1nQ62stZCw"
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/bh_project",
            json={
                "bh_project_name": "Test Project",
                "bh_github_username": "username",
                "bh_github_email": "test@testexample.com",
                "bh_default_branch": "main",
                "bh_github_url": "https://github.com/username/repo",
                "bh_github_token_url": "test_token",
                "init_vector": "test_vector",
                "tags": {},
            },
            headers={"Authorization": f"Bearer {token}"},
        )
    # Assertions
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["bh_project_name"] == "Test Project"

    # Validate decrypt_string was called with the correct arguments
    mock_decrypt.assert_called_once_with(
        "test_token",
        "test_vector",
    )

    # Validate GitWrapper.create_branch was called
    mock_git_instance.create_branch.assert_called_once_with("main")

    # Validate aws_service.secrets.new_secret was called
    mock_aws_service.return_value.secrets.new_secret.assert_called_once_with(
        "github_test_project_secret",
        '{"github_token": "decrypted_token"}',
    )