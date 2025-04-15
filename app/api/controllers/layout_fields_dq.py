from typing import List, Optional
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, Query, Request
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.enums import DQ_LEVEL
from app.models.base import StatusMessage
from app.models.layout_fields_dq import (LayoutFieldsDQCreate,
                                         LayoutFieldsDQReturn,
                                         LayoutFieldsDQUpdate)
from app.utils.auth_wrapper import authorize

router = APIRouter()


@router.get(
    "/list/",
    response_model=List[LayoutFieldsDQReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_layout_fields_dq(
    *,
    lyt_fld_id: Optional[int] = None,
    fld_dq_id: Optional[str] = None,
    fld_dq_level: Optional[DQ_LEVEL] = None,
    fld_dq_type_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'field_name', 'field_type'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.layout_fields_dq_service.list(
        lyt_fld_id=lyt_fld_id,
        fld_dq_id=fld_dq_id,
        fld_dq_level=fld_dq_level,
        fld_dq_type_id=fld_dq_type_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/search/",
    response_model=List[LayoutFieldsDQReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_field_dq_for_word(
    *,
    params: Optional[str] = Query(
        None, description="Search any field like, lyt_fld_name=abc&lyt_fld_key=cdf"
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.layout_fields_dq_service.search(params=params)


@router.get(
    "/{fld_dq_id}",
    response_model=LayoutFieldsDQReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_layout_fields_dq(
    *, fld_dq_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.layout_fields_dq_service.get(fld_dq_id=fld_dq_id)


@router.post(
    "/",
    response_model=LayoutFieldsDQReturn,
    status_code=http_status.HTTP_201_CREATED,
)
async def create_layout_fields_dq(
    *, layout_fields_dq_in: LayoutFieldsDQCreate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.layout_fields_dq_service.create(layout_fields_dq_in, authorized=authorized)


@router.put(
    "/{fld_dq_id}",
    response_model=LayoutFieldsDQReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_layout_fields_dq(
    *,
    fld_dq_id: int,
    layout_fields_dq_in: LayoutFieldsDQUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.layout_fields_dq_service.update(fld_dq_id, layout_fields_dq_in, authorized=authorized)


@router.delete(
    "/{fld_dq_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_layout_fields_dq(
    *, fld_dq_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.layout_fields_dq_service.delete(fld_dq_id, authorized=authorized)
    return {"status": status, "message": "The record has been deleted!"}
