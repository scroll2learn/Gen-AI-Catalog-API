from typing import List, Optional
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.models.base import StatusMessage
from app.models.customer import (ConnectionDtlCreate, ConnectionDtlReturn,
                                 ConnectionDtlUpdate, CustomerCreate,
                                 CustomerReturn, CustomerUpdate)
from app.utils.auth_wrapper import authorize

router = APIRouter()


@router.get(
    "/list/",
    response_model=List[CustomerReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_customer(
    *,
    customer_id: Optional[int] = None,
    relation_ship_owner: Optional[str] = None,
    relation_ship_owner_email: Optional[str] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'relation_ship_owner'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.customer_service.list(
        customer_id=customer_id,
        relation_ship_owner=relation_ship_owner,
        relation_ship_owner_email=relation_ship_owner_email,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/search",
    response_model=List[CustomerReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_field_for_word(
    *,
    params: Optional[str] = Query(
        None,
        description="Search any field like, relation_ship_owner=abc&business_url=cdf",
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.customer_service.search(params=params)


@router.get(
    "/{customer_id}",
    response_model=CustomerReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_customer(
    *, customer_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.customer_service.get(id=customer_id)


@router.post(
    "",
    response_model=CustomerReturn,
    status_code=http_status.HTTP_200_OK,
)
async def create_customer(
    *, obj: CustomerCreate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.customer_service.create(obj=obj, authorized=authorized)


@router.put(
    "/{customer_id}", response_model=CustomerReturn, status_code=http_status.HTTP_200_OK
)
async def update_by_customer_id(
    *, customer_id: int, obj: CustomerUpdate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.customer_service.update(id=customer_id, obj=obj, authorized=authorized)


@router.delete(
    "/{customer_id}", response_model=StatusMessage, status_code=http_status.HTTP_200_OK
)
async def delete_customer_by_id(
    customer_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.customer_service.delete(id=customer_id, authorized=authorized)

    return {"status": status, "message": "The record has been deleted!"}


@router.get(
    "/connection_dtl/list/",
    response_model=List[ConnectionDtlReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_connection_dtl(
    *,
    connection_dtl_id: Optional[int] = None,
    connection_dtl_name: Optional[str] = None,
    connection_dtl_url: Optional[str] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None,
        description="Field to order by, e.g., 'connection_dtl_name', 'connection_dtl_desc'",
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.connection_dtl_service.list(
        connection_dtl_id=connection_dtl_id,
        connection_dtl_name=connection_dtl_name,
        connection_dtl_url=connection_dtl_url,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/connection_dtl/search",
    response_model=List[ConnectionDtlReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_connection_dtl_field_for_word(
    *,
    params: Optional[str] = Query(
        None,
        description="Search any field like, connection_dtl_name=abc&connection_dtl_url=cdf",
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.connection_dtl_service.search(params=params)


@router.get(
    "/connection_dtl/{connection_dtl_id}",
    response_model=ConnectionDtlReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_connection_dtl(
    *, connection_dtl_id: int, ctx: Context = Depends(get_context)
):
    return await ctx.connection_dtl_service.get(id=connection_dtl_id)


@router.post(
    "/connection_dtl",
    response_model=ConnectionDtlReturn,
    status_code=http_status.HTTP_200_OK,
)
async def create_connection_dtl(
    *, obj: ConnectionDtlCreate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.connection_dtl_service.create(obj=obj, authorized=authorized)


@router.put(
    "/connection_dtl/{connection_dtl_id}",
    response_model=ConnectionDtlReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_connection_dtl_by_id(
    *,
    connection_dtl_id: int,
    obj: ConnectionDtlUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.connection_dtl_service.update(id=connection_dtl_id, obj=obj, authorized=authorized)


@router.delete(
    "/connection_dtl/{connection_dtl_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_connection_dtl_by_id(
    connection_dtl_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.connection_dtl_service.delete(id=connection_dtl_id, authorized=authorized)
    return {"status": status, "message": "The record has been deleted!"}


#     test_connection_service: TestConnectionService = ctx.test_connection_service
#     response= await ctx.test_connection_service.test_aws_connection(credentials=credentials)
#     ConnectionTestResponse(**response)
#     return response
