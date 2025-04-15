from typing import List, Optional
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, Query, Request
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.models.base import (UserDetail, UserDetailBase, UserDetailReturn)
from app.models.base import StatusMessage

router = APIRouter()

@router.get(
    "/list/",
    response_model=List[UserDetailReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_users(
    *,
    user_detail_id: Optional[int] = None,
    username: Optional[str] = None,
    user_email: Optional[str] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(None, description="Field to order by, e.g., 'user_detail_id', 'username'"),
    order_desc: bool = False,
    ctx: Context = Depends(get_context)
):
    return await ctx.user_detail_service.list(
        user_detail_id=user_detail_id,
        username=username,
        user_email=user_email,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )

@router.get(
    "/{user_detail_id}",
    response_model=UserDetailReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_user(
    *,
    user_detail_id: int,
    ctx: Context = Depends(get_context)
):
    return await ctx.user_detail_service.get(id=user_detail_id)

@router.post(
    "",
    response_model=UserDetailReturn,
    status_code=http_status.HTTP_200_OK,
)
async def create_user(
    *,
    obj: UserDetailBase,
    ctx: Context = Depends(get_context)
):
    return await ctx.user_detail_service.create(obj=obj)

@router.put(
    "/{user_detail_id}",
    response_model=UserDetailReturn,
    status_code=http_status.HTTP_200_OK
)
async def update_by_user_id(
    *,
    user_detail_id: int,
    obj: UserDetailBase,
    ctx: Context = Depends(get_context)
):
    return await ctx.user_detail_service.update(id=user_detail_id, obj=obj)

@router.delete(
    "/{user_detail_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK
)
async def delete_user_by_id(
    user_detail_id: int,
    ctx: Context = Depends(get_context)
):
    status = await ctx.user_detail_service.delete(id=user_detail_id)
    return {"status": status, "message": "The record has been deleted!"}
