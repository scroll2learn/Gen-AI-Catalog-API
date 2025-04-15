from typing import List, Optional
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, Query, Request
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.models.base import StatusMessage
from app.models.fld_properties import (FieldPropertiesCreate,
                                       FieldPropertiesReturn,
                                       FieldPropertiesUpdate)
from app.utils.auth_wrapper import authorize

router = APIRouter()


@router.get(
    "/list/",
    response_model=List[FieldPropertiesReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_field_properties(
    *,
    fld_id: Optional[int] = None,
    fld_name: Optional[str] = None,
    fld_key: Optional[str] = None,
    lyt_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'field_name', 'field_type'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.field_properties_service.list(
        fld_id=fld_id,
        fld_name=fld_name,
        fld_key=fld_key,
        lyt_id=lyt_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/search",
    response_model=List[FieldPropertiesReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_field_for_word(
    *,
    params: Optional[str] = Query(
        None, description="Search any field like, fld_name=abc&fld_key=cdf"
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.field_properties_service.search(params=params)


@router.get(
    "/{fld_id}",
    response_model=FieldPropertiesReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_field_properties(
    *, fld_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.field_properties_service.get(id=fld_id)


@router.post(
    "/",
    response_model=FieldPropertiesReturn,
    status_code=http_status.HTTP_201_CREATED,
)
async def create_field_properties(
    *, field_in: FieldPropertiesCreate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    
    # field_in.created_by = authorized.get("user_detail_id")
    return await ctx.field_properties_service.create(obj=field_in, authorized=authorized)


@router.post(
    "/bulk/",
    response_model=List[FieldPropertiesReturn],
    status_code=http_status.HTTP_201_CREATED,
)
async def create_or_update_field_properties(
    flds_properties_list: List[FieldPropertiesCreate],
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.field_properties_service.create_or_update_field_properties(
        flds_properties_list=flds_properties_list
    )


@router.put(
    "/{fld_id}",
    response_model=FieldPropertiesReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_field_properties(
    *, fld_id: int, field_in: FieldPropertiesUpdate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.field_properties_service.update(id=fld_id, obj=field_in, authorized=authorized)


@router.delete(
    "/{fld_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_field_properties(
    *, fld_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.field_properties_service.delete(id=fld_id, authorized=authorized)
    return {"status": status, "message": "The record has been deleted!"}
