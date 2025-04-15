from typing import Optional

from fastapi import APIRouter, Depends
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.utils.api_wrapper import APIWrapper
from app.utils.auth_wrapper import authorize

router = APIRouter()
api_wrapper = APIWrapper()


@router.get("/get-field-properties", status_code=http_status.HTTP_200_OK)
async def get_field_properties(
    field_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    field_object = await ctx.layout_fields_service.get(id=field_id)
    data_source_layout = await ctx.data_source_layout_service.get(
        id=field_object.lyt_id
    )
    data_source = await ctx.data_source_service.get(id=data_source_layout.data_src_id)

    response = await api_wrapper.get_field_properties(
        source_file_path=data_source_layout.data_src_file_path,
        data_src_key=data_source.data_src_key,
        field_name=field_object.lyt_fld_name,
    )
    return response
