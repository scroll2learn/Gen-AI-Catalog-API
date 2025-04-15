from typing import List, Optional
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, Query, Request
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.models.fld_recommendations import (FieldRecommendationsCreate,
                                            FieldRecommendationsReturn,
                                            FieldRecommendationsUpdate)
from app.utils.auth_wrapper import authorize

router = APIRouter()


@router.get(
    "/list/",
    response_model=List[FieldRecommendationsReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_field_recommendations(
    *,
    rule_fld_id: Optional[int] = None,
    rule_name: Optional[str] = None,
    rule_dq_type_id: Optional[int] = None,
    rule_status: Optional[str] = None,
    rule_lyt_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'field_name', 'field_type'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.field_recommendations_service.list(
        rule_fld_id=rule_fld_id,
        rule_name=rule_name,
        rule_dq_type_id=rule_dq_type_id,
        rule_status=rule_status,
        rule_lyt_id=rule_lyt_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/search",
    response_model=List[FieldRecommendationsReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_field_for_word(
    *,
    params: Optional[str] = Query(
        None, description="Search any field like, rule_name=abc&rule_status=cdf"
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.field_recommendations_service.search(params=params)


@router.put(
    "/{rule_id}",
    response_model=FieldRecommendationsReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_field_properties(
    *,
    rule_id: int,
    field_recom: FieldRecommendationsUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.field_recommendations_service.update(id=rule_id, obj=field_recom, authorized=authorized)


@router.post(
    "/bulk/",
    response_model=List[FieldRecommendationsReturn],
    status_code=http_status.HTTP_201_CREATED,
)
async def create_or_update_field_properties(
    flds_recommendations_list: List[FieldRecommendationsCreate],
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.field_recommendations_service.create_field_recommendations(
        flds_recommendations_list=flds_recommendations_list
    )
