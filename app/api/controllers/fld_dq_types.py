from typing import List, Optional
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, Query, Request
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.models.base import StatusMessage
from app.models.fld_dq_types import (FieldDQReturn, FieldDQTypesCreate,
                                     FieldDQTypesUpdate)
from app.utils.auth_wrapper import authorize

router = APIRouter()


@router.get(
    "/list/",
    response_model=List[FieldDQReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_fld_dq_types(
    *,
    dq_id: Optional[int] = None,
    dq_name: Optional[str] = None,
    dq_template: Optional[str] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'field_name', 'field_type'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.fields_dq_types_service.list(
        dq_id=dq_id,
        dq_name=dq_name,
        dq_template=dq_template,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/search",
    response_model=List[FieldDQReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_field_for_word(
    *,
    params: Optional[str] = Query(
        None, description="Search any field like, bh_project_name=abc&business_url=cdf"
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.fields_dq_types_service.search(params=params)


@router.get(
    "/{dq_id}",
    response_model=FieldDQReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_fld_dq_type(
    *, dq_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.fields_dq_types_service.get(id=dq_id)


@router.post(
    "/",
    response_model=FieldDQReturn,
    status_code=http_status.HTTP_201_CREATED,
)
async def create_fld_dq_type(
    *, field_dq_type_in: FieldDQTypesCreate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.fields_dq_types_service.create(obj=field_dq_type_in, authorized=authorized)


@router.put(
    "/{dq_id}",
    response_model=FieldDQReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_fld_dq_type(
    *,
    dq_id: int,
    field_dq_type_in: FieldDQTypesUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.fields_dq_types_service.update(id=dq_id, obj=field_dq_type_in, authorized=authorized)


@router.delete(
    "/{dq_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_fld_dq_type(
    *, dq_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.fields_dq_types_service.delete(id=dq_id, authorized=authorized)
    return {"status": status, "message": "The record has been deleted!"}
