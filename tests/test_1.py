import pytest
from app.api.controllers.pipelines import get_all_pipelines
from app.utils.request_wrapper import RequestWrapper
from app.core.context import Context

@pytest.mark.asyncio
async def test_get_all_pipelines_view_function(init_db):
    # Create the context with the test session
    client = RequestWrapper(base_url="http://localhost:8011")
    responce = await client.call_api("api/v1/pipeline/list", method="get")

    # Assert the expected result
    assert responce.status_code == 200
