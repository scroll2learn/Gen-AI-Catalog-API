from typing import Optional

from fastapi import APIRouter, Depends
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.exceptions import MissingRequiredParameter
from app.utils.auth_wrapper import authorize

router = APIRouter()


@router.get(
    "/export_tables/",
    status_code=http_status.HTTP_200_OK,
)
async def export_tables(
    *, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.engine_integrations_service.export_tables()


@router.get(
    "/engine_config_export/",
    status_code=http_status.HTTP_200_OK,
)
async def engine_config_export(
    data_source_id: Optional[int] = None,
    data_source_name: Optional[str] = None,
    data_source_key: Optional[str] = None,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    if data_source_id is None and data_source_name is None and data_source_key is None:
        raise MissingRequiredParameter
    return await ctx.engine_integrations_service.engine_config_export(
        data_source_id=data_source_id,
        data_source_name=data_source_name,
        data_source_key=data_source_key,
    )
