from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.exceptions import DataSourceAlreadyExists
from app.models.author_data import FileProcessRequest, ResponseModel
from app.utils.api_wrapper import APIWrapper
from app.utils.auth_wrapper import authorize

router = APIRouter()
api_wrapper = APIWrapper()


@router.post(
    "/process-file",
    response_model=ResponseModel,
    status_code=http_status.HTTP_200_OK,
)
async def author_data(
    request: FileProcessRequest,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    if await ctx.data_source_service.check_source_exists(data_src_name=request.name):
        raise DataSourceAlreadyExists(
            context={"name": request.name}
        )
    response = await api_wrapper.get_file_process(
        name=request.name,
        source_file_path=request.source_file_path,
        lake_zone_id=request.lake_zone_id,
        data_src_status_cd=request.data_src_status_cd,
    )
    ResponseModel(**response)
    return response


@router.get(
    "/get-sample-data",
    response_model=ResponseModel,
    status_code=http_status.HTTP_200_OK,
)
async def get_sample_data(
            data_src_id: int,
            ctx: Context = Depends(get_context),
            authorized: Optional[dict] = Depends(authorize('admin_module', 'view')),
    ):

    data_source = await ctx.data_source_service.get(id=data_src_id)
    data_source_layout = await ctx.data_source_layout_service.list(data_src_id=data_src_id)
    layout_fields = await ctx.layout_fields_service.list(lyt_id=data_source_layout[0].data_src_lyt_id)

    sample_data = await api_wrapper.get_sample_data(
        source_file_path=data_source_layout[0].data_src_file_path,
        data_src_key=data_source.data_src_key,
        num_rows=10)
    
    response = ResponseModel(
        data_source=data_source,
        data_source_layout=data_source_layout[0],
        layout_fields=layout_fields,
        sample_data=sample_data,
    )
    return response
