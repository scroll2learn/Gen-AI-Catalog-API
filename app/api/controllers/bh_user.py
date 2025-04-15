from typing import List, Optional
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, Query, Request
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.models.base import StatusMessage
from app.models.bh_user import BHUser, BHUserCreate, BHUserReturn, BHUserUpdate

router = APIRouter()


@router.get(
        "/list/",
        response_model=List[BHUser],
        status_code=http_status.HTTP_200_OK,
)
async def get_all_bighammer_users(
                *,
                bh_user_id: Optional[int] = None,
                bh_user_first_name: Optional[str] = None,
                user_status_cd: Optional[str] = None,
                offset: int = 0,
                limit: int = 10,
                order_by: Optional[str] = Query(None, description="Field to order by, e.g., 'bh_user_id', 'bh_user_name'"),
                order_desc: bool = False,
                ctx: Context = Depends(get_context)):
        return await ctx.bh_user_service.list(
              bh_user_id=bh_user_id,
              bh_user_first_name=bh_user_first_name,
              user_status_cd=user_status_cd,
              offset=offset,
              limit=limit,
              order_by=order_by,
              order_desc=order_desc,
        )
 

@router.get(
        "/search",
        response_model=List[BHUser],
        status_code=http_status.HTTP_200_OK,
)
async def search_field_for_word(
                *,
                params: Optional[str] = Query(None, description="Search any field like, bh_project_name=abc&business_url=cdf"),
                request: Request,
                ctx: Context = Depends(get_context)):
        if params is not None:
              params = parse_qs(params)
        else:
              params = parse_qs(request.url.query)
        return await ctx.bh_user_service.search(params=params)


@router.get(
        "/{bh_user_id}",
        response_model=BHUserReturn,
        status_code=http_status.HTTP_200_OK,
)
async def get_bighammer_user(
                *,
                bh_user_id: int,
                ctx: Context = Depends(get_context)):
        return await ctx.bh_user_service.get(id=bh_user_id)



@router.post(
        "",
        response_model=BHUserReturn,
        status_code=http_status.HTTP_200_OK,
)
async def create_bighammer_user(
                *,
                obj: BHUserCreate,
                ctx: Context = Depends(get_context)):
        return await ctx.bh_user_service.create(obj=obj)


@router.put(
    "/{bh_user_id}",
    response_model=BHUserReturn,
    status_code=http_status.HTTP_200_OK
)
async def update_by_bighammer_user_id(
        *,
        bh_user_id: int,
        obj: BHUserUpdate,
        ctx: Context = Depends(get_context)):
    return await ctx.bh_user_service.update(id=bh_user_id, obj=obj)


@router.delete(
    "/{bh_user_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK
)
async def delete_bighammer_user_by_id(
        bh_user_id: int,
        ctx: Context = Depends(get_context)):
    status = await ctx.bh_user_service.delete(id=bh_user_id)

    return {"status": status, "message": "The record has been deleted!"}
