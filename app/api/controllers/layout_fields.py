from typing import List, Optional
from urllib.parse import parse_qs

from app.utils.data_source_utils import get_text_embedding
from fastapi import APIRouter, Depends, Query, Request
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.models.base import StatusMessage
from app.models.layout_fields import (LayoutFields, LayoutFieldsCreate, LayoutFieldsReturn,
                                      LayoutFieldsUpdate, LayoutBulkDescriptionUpdate)
from app.utils.auth_wrapper import authorize

router = APIRouter()


@router.get(
    "/list/",
    response_model=List[LayoutFieldsReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_layout_fields(
    *,
    lyt_fld_id: Optional[int] = None,
    lyt_fld_name: Optional[str] = None,
    lyt_fld_key: Optional[str] = None,
    lyt_fld_is_pk: Optional[bool] = None,
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
    return await ctx.layout_fields_service.list(
        lyt_fld_id=lyt_fld_id,
        lyt_fld_name=lyt_fld_name,
        lyt_fld_key=lyt_fld_key,
        lyt_fld_is_pk=lyt_fld_is_pk,
        lyt_id=lyt_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/search/",
    response_model=List[LayoutFieldsReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_field_for_word(
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
    return await ctx.data_source_layout_service.search(params=params)


@router.get(
    "/{lyt_fld_id}",
    response_model=LayoutFieldsReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_layout_fields(
    lyt_fld_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.layout_fields_service.get(lyt_fld_id)


@router.post(
    "/",
    response_model=LayoutFieldsReturn,
    status_code=http_status.HTTP_201_CREATED,
)
async def create_layout_fields(
    layout_fields: LayoutFieldsCreate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    embedding = await get_text_embedding(layout_fields.lyt_fld_name, layout_fields.lyt_fld_desc)
    layout_fields_obj = LayoutFields(
        **layout_fields.dict(),
        lyt_fld_embedding=embedding
    )
    return await ctx.layout_fields_service.create(layout_fields_obj, authorized=authorized)


@router.post(
    "/bulk/",
    response_model=List[LayoutFieldsReturn],
    status_code=http_status.HTTP_201_CREATED,
)
async def create_bulk_layout_fields(
    layout_fields: List[LayoutFieldsCreate], ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.layout_fields_service.create_bulk_fields(layout_fields)


@router.put(
    "/{lyt_fld_id}",
    response_model=LayoutFieldsReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_layout_fields(
    lyt_fld_id: int,
    layout_fields: LayoutFieldsUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    current_layout_field = await ctx.layout_fields_service.get(lyt_fld_id)
    updated_fields = []

    if layout_fields.lyt_fld_name:
        if layout_fields.lyt_fld_name != current_layout_field.lyt_fld_name:
            updated_fields.append('name')
    else:
        layout_fields.lyt_fld_name = current_layout_field.lyt_fld_name

    if layout_fields.lyt_fld_desc:
        if layout_fields.lyt_fld_desc != current_layout_field.lyt_fld_desc:
            updated_fields.append('desc')
    else:
        layout_fields.lyt_fld_desc = current_layout_field.lyt_fld_desc

    if updated_fields:
        embedding = await get_text_embedding(layout_fields.lyt_fld_name, layout_fields.lyt_fld_desc)
        layout_fields.lyt_fld_embedding = embedding
    else:
        layout_fields.lyt_fld_embedding = current_layout_field.lyt_fld_embedding

    return await ctx.layout_fields_service.update(lyt_fld_id, layout_fields, authorized=authorized)

@router.delete(
    "/{lyt_fld_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_layout_fields(
    lyt_fld_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.layout_fields_service.delete(lyt_fld_id, authorized=authorized)
    return {"status": status, "message": "The record has been deleted!"}


@router.put(
    "/bulk_pk/",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def update_fields_primary_keys(
    field_ids: List[int], is_pk: bool = False, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    await ctx.layout_fields_service.update_fields_pk(field_ids, is_pk)
    return {"status": True, "message": "The records has been updated!"}


@router.patch(
    "/descriptions/{lyt_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def update_field_descriptions(
    lyt_id: int,
    descriptions: LayoutBulkDescriptionUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    await ctx.layout_fields_service.update_bulk_descriptions(lyt_id, descriptions.descriptions)
    return {"status": True, "message": "Field descriptions have been updated successfully!"}
