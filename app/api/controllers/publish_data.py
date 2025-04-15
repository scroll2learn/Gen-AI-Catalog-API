import os
from typing import List, Optional
from urllib.parse import parse_qs

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.models.base import StatusMessage
from app.models.pulish_data import (PublishDetailsCreate, PublishDetailsReturn,
                                    PublishDetailsUpdate,
                                    PublishQueryDetailsCreate,
                                    PublishQueryDetailsReturn,
                                    PublishQueryDetailsUpdate)
from app.utils.auth_wrapper import authorize

load_dotenv()

router = APIRouter()


@router.get(
    "/publish_details/list/",
    response_model=List[PublishDetailsReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_publish_details(
    *,
    delivery_name: Optional[str] = None,
    customer_id: Optional[int] = None,
    bh_project_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'delivery_name'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.publish_details_service.list(
        delivery_name=delivery_name,
        customer_id=customer_id,
        bh_project_id=bh_project_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/publish_details/search",
    response_model=List[PublishDetailsReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_publish_details(
    *,
    params: Optional[str] = Query(
        None, description="Search any field like, delivery_name=abc&customer_id=123"
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.publish_details_service.search(params=params)


@router.get(
    "/publish_details/{publish_id}",
    response_model=PublishDetailsReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_publish_details(
    *, publish_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.publish_details_service.get(id=publish_id)


@router.post(
    "/publish_details",
    response_model=PublishDetailsReturn,
    status_code=http_status.HTTP_200_OK,
)
async def create_publish_details(
    *, obj: PublishDetailsCreate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.publish_details_service.create(obj=obj, authorized=authorized)


@router.put(
    "/publish_details/{publish_id}",
    response_model=PublishDetailsReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_publish_details(
    *, publish_id: int, obj: PublishDetailsUpdate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.publish_details_service.update(id=publish_id, obj=obj, authorized=authorized)


@router.delete(
    "/publish_details/{publish_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_publish_details(
    publish_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.publish_details_service.delete(id=publish_id, authorized=authorized)
    return {"status": status, "message": "The record has been deleted!"}


# PublishQueryDetails endpoints
@router.get(
    "/publish_query_details/list/",
    response_model=List[PublishQueryDetailsReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_publish_query_details(
    *,
    offset: int = 0,
    limit: int = 10,
    is_save: Optional[bool] = None,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'query'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.publish_query_details_service.list(
        offset=offset,
        limit=limit,
        is_save=is_save,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/publish_query_details/search",
    response_model=List[PublishQueryDetailsReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_publish_query_details(
    *,
    params: Optional[str] = Query(None, description="Search any field like, query=abc"),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.publish_query_details_service.search(params=params)


@router.get(
    "/publish_query_details/{query_id}",
    response_model=PublishQueryDetailsReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_publish_query_details(
    *, query_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.publish_query_details_service.get(id=query_id)


@router.post(
    "/publish_query_details",
    response_model=PublishQueryDetailsReturn,
    status_code=http_status.HTTP_200_OK,
)
async def create_publish_query_details(
    *, obj: PublishQueryDetailsCreate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.publish_query_details_service.create(obj=obj, authorized=authorized)


@router.put(
    "/publish_query_details/{query_id}",
    response_model=PublishQueryDetailsReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_publish_query_details(
    *,
    query_id: int,
    obj: PublishQueryDetailsUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.publish_query_details_service.update(id=query_id, obj=obj, authorized=authorized)


@router.delete(
    "/publish_query_details/{query_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_publish_query_details(
    query_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.publish_query_details_service.delete(id=query_id, authorized=authorized)
    return {"status": status, "message": "The record has been deleted!"}
