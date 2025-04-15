from typing import List, Optional
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, Query, Request
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.models.base import StatusMessage
from app.models.platform_region import (PlatformRegion, PlatformRegionCreate,
                                        PlatformRegionReturn,
                                        PlatformRegionUpdate)
from app.utils.auth_wrapper import authorize

router = APIRouter()


@router.get(
    "/list/",
    response_model=List[PlatformRegion],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_platform_region(
    *,
    id: Optional[int] = None,
    description: Optional[str] = None,
    region_identifier: Optional[str] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None,
        description="Field to order by, e.g., 'platform_region_id', 'platform_region_name'",
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.platform_region_service.list(
        id=id,
        description=description,
        region_identifier=region_identifier,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/search",
    response_model=List[PlatformRegion],
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
    return await ctx.platform_region_service.search(params=params)


@router.get(
    "/{platform_region_id}",
    response_model=PlatformRegionReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_platform_region(
    *, platform_region_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.platform_region_service.get(id=platform_region_id)


@router.post(
    "",
    response_model=PlatformRegionReturn,
    status_code=http_status.HTTP_200_OK,
)
async def create_platform_region(
    *, obj: PlatformRegionCreate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.platform_region_service.create(obj=obj, authorized=authorized)


@router.put(
    "/{platform_region_id}",
    response_model=PlatformRegionReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_by_platform_region_id(
    *,
    platform_region_id: int,
    obj: PlatformRegionUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.platform_region_service.update(id=platform_region_id, obj=obj, authorized=authorized)


@router.delete(
    "/{platform_region_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_platform_region_by_id(
    platform_region_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.platform_region_service.delete(id=platform_region_id, authorized=authorized)

    return {"status": status, "message": "The record has been deleted!"}
