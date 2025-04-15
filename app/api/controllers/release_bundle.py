from typing import List, Optional
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.models.base import StatusMessage
from app.models.flow import Flow
from app.models.release_bundle import (BHReleaseBundle, BHReleaseBundleBase, 
                                       BHReleaseBundleCreate, BHReleaseBundleReturn, 
                                       BHReleaseBundleUpdate)
from app.utils.auth_wrapper import authorize
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter()

@router.get(
    "/list/",
    response_model=List[BHReleaseBundleReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_release_bundle(
    *,
    bh_bundle_id: Optional[int] = None,
    bh_bundle_name: Optional[str] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(None, description="Field to order bu, e.g., 'bh_bundle_id', 'bh_bundle_name' "),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    # authorized: Optional[dict] = Depends(authorize("admin_module", "view"))
):
    return await ctx.release_bundle_service.list(
        bh_bundle_id = bh_bundle_id,
        bh_bundle_name = bh_bundle_name,
        offset = offset,
        limit = limit,
        order_by = order_by,
        order_desc = order_desc
    )

@router.get(
    "/search",
    response_model=List[BHReleaseBundleReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_field_for_word(
    *,
    params: Optional[str] = Query(
        None, description="Search any field like, bh_bundle_name=abc"
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.release_bundle_service.search(params=params)

@router.get(
    "/{bh_bundle_id}",
    response_model=BHReleaseBundleReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_release_bundle(
    *,
    bh_bundle_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    response = await ctx.release_bundle_service.get(id=bh_bundle_id)
    return response
    
@router.post(
    "",
    response_model=BHReleaseBundle,
    status_code=http_status.HTTP_200_OK,
)
async def create_release_bundle(
    *,
    obj: BHReleaseBundleCreate,
    ctx: Context = Depends(get_context),
):
    try:
        flow_ids = obj.flow
        if not flow_ids:
            raise HTTPException(status_code=400, detail="Flow IDs are required.")

        # Verify flows exist
        flows = await ctx.flow_service.get_list(flow_ids)
        if not flows:
            raise HTTPException(status_code=404, detail="No flows found with the provided IDs.")

        # Create release bundle without flow
        bundle_data = obj.dict(exclude={'flow'})
        release_bundle = await ctx.release_bundle_service.create(obj=BHReleaseBundleCreate(**bundle_data))

        # Update all flows in a single query
        await ctx.db_session.execute(
            """
            UPDATE flow
            SET bh_bundle_id = :bh_bundle_id
            WHERE flow_id = ANY(:flow_ids)
            """,
            {"bh_bundle_id": release_bundle.bh_bundle_id, "flow_ids": flow_ids},
        )

        await ctx.db_session.refresh(release_bundle)
        return release_bundle
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/{bh_bundle_id}",
    response_model=BHReleaseBundleReturn,
    status_code=http_status.HTTP_200_OK
)
async def update_release_bundle_id(
    *,
    bh_bundle_id: int,
    obj: BHReleaseBundleUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    return await ctx.release_bundle_service.update(id=bh_bundle_id, obj=obj)

@router.delete(
    "/{bh_bundle_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK
)
async def delete_release_bundle(
    bh_bundle_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
    ):
    status = await ctx.release_bundle_service.delete(id=bh_bundle_id, authorized=authorized)
    return{"status": status, "message": "The recorde has been deleted!"}