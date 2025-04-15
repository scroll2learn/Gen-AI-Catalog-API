from typing import List, Optional
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, Query, Request
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.models.base import StatusMessage
from app.models.data_source_layout import (DataSourceLayoutCreate,
                                           DataSourceLayoutFullReturn,
                                           DataSourceLayoutReturn,
                                           DataSourceLayoutUpdate)
from app.models.connection_registry import ConnectionConfigReturn
from app.utils.auth_wrapper import authorize

router = APIRouter()


@router.get(
    "/list_full/",
    response_model=List[DataSourceLayoutFullReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_full_data_source_layouts(
    *,
    data_src_lyt_id: Optional[int] = None,
    data_src_lyt_name: Optional[str] = None,
    data_src_lyt_key: Optional[str] = None,
    data_src_lyt_pk: Optional[bool] = None,
    data_src_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None,
        description="Field to order by, e.g., 'data_src_lyt_name', 'data_src_lyt_key'",
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    # Get layouts with their fields
    layouts = await ctx.data_source_layout_service.list_full(
        data_src_lyt_id=data_src_lyt_id,
        data_src_lyt_name=data_src_lyt_name,
        data_src_lyt_key=data_src_lyt_key,
        data_src_lyt_pk=data_src_lyt_pk,
        data_src_id=data_src_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )
    
    # For each layout, fetch and add connection config
    for layout in layouts:
        if layout.data_src_id:
            # Get data source to get connection_config_id
            data_source = await ctx.data_source_service.get(layout.data_src_id)
            if data_source and data_source.connection_config_id:
                # Get connection config
                connection_config = await ctx.connection_config_service.get(
                    data_source.connection_config_id
                )
                layout.connection_config = ConnectionConfigReturn.from_orm(connection_config)
    
    return layouts


@router.get(
    "/list/",
    response_model=List[DataSourceLayoutReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_data_source_layouts(
    *,
    data_src_lyt_id: Optional[int] = None,
    data_src_lyt_name: Optional[str] = None,
    data_src_lyt_key: Optional[str] = None,
    data_src_lyt_pk: Optional[bool] = None,
    data_src_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None,
        description="Field to order by, e.g., 'data_src_lyt_name', 'data_src_lyt_key'",
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.data_source_layout_service.list(
        data_src_lyt_id=data_src_lyt_id,
        data_src_lyt_name=data_src_lyt_name,
        data_src_lyt_key=data_src_lyt_key,
        data_src_lyt_pk=data_src_lyt_pk,
        data_src_id=data_src_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/search",
    response_model=List[DataSourceLayoutReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_field_for_word(
    *,
    params: Optional[str] = Query(
        None,
        description="Search any field like, data_src_lyt_name=abc&data_src_lyt_key=cdf",
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.data_source_layout_service.search(params=params)


@router.get(
    "/{data_src_lyt_id}",
    response_model=DataSourceLayoutReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_data_source_layout(
    data_src_lyt_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.data_source_layout_service.get(data_src_lyt_id)


@router.post(
    "/",
    response_model=DataSourceLayoutReturn,
    status_code=http_status.HTTP_201_CREATED,
)
async def create_data_source_layout(
    data_source_layout: DataSourceLayoutCreate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.data_source_layout_service.create(data_source_layout, authorized=authorized)


@router.put(
    "/{data_src_lyt_id}",
    response_model=DataSourceLayoutReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_data_source_layout(
    data_src_lyt_id: int,
    data_source_layout: DataSourceLayoutUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.data_source_layout_service.update_layout(
        data_src_lyt_id, data_source_layout, authorized=authorized
    )


@router.delete(
    "/{data_src_lyt_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_data_source_layout(
    data_src_lyt_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.data_source_layout_service.delete(data_src_lyt_id, authorized=authorized)
    return {"status": status, "message": "The record has been deleted!"}

