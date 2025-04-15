from typing import List, Optional
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, Query, Request
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.models.app_user import (AppUser, AppUserCreate, AppUserReturn,
                                 AppUserUpdate)
from app.models.base import StatusMessage

router = APIRouter()


@router.get(
        "/list/",
        response_model=List[AppUser],
        status_code=http_status.HTTP_200_OK,
)
async def get_all_users(
                *,
                id: Optional[int] = None,
                user_id: Optional[str] = None,
                ad_id: Optional[str] = None,
                active: Optional[bool] = None,
                offset: int = 0,
                limit: int = 10,
                order_by: Optional[str] = Query(None, description="Field to order by, e.g., 'app_user_id', 'app_user_name'"),
                order_desc: bool = False,
                ctx: Context = Depends(get_context)):
        return await ctx.app_user_service.list(
              id=id,
              user_id=user_id,
              ad_id=ad_id,
              active=active,
              offset=offset,
              limit=limit,
              order_by=order_by,
              order_desc=order_desc,
        )
 

@router.get(
        "/search",
        response_model=List[AppUser],
        status_code=http_status.HTTP_200_OK,
)
async def search_field_for_word(
                *,
                params: Optional[str] = Query(None, description="Search any field like, user_name=abc"),
                request: Request,
                ctx: Context = Depends(get_context)):
        if params is not None:
              params = parse_qs(params)
        else:
              params = parse_qs(request.url.query)
        return await ctx.app_user_service.search(params=params)


@router.get(
        "/{app_user_id}",
        response_model=AppUserReturn,
        status_code=http_status.HTTP_200_OK,
)
async def get_user(
                *,
                app_user_id: int,
                ctx: Context = Depends(get_context)):
        return await ctx.app_user_service.get(id=app_user_id)



@router.post(
        "",
        response_model=AppUserReturn,
        status_code=http_status.HTTP_200_OK,
)
async def create_user(
                *,
                obj: AppUserCreate,
                ctx: Context = Depends(get_context)):
        return await ctx.app_user_service.create(obj=obj)


@router.put(
    "/{app_user_id}",
    response_model=AppUserReturn,
    status_code=http_status.HTTP_200_OK
)
async def update_by_user_id(
        *,
        app_user_id: int,
        obj: AppUserUpdate,
        ctx: Context = Depends(get_context)):
    return await ctx.app_user_service.update(id=app_user_id, obj=obj)


@router.delete(
    "/{app_user_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK
)
async def delete_user_by_id(
        app_user_id: int,
        ctx: Context = Depends(get_context)):
    status = await ctx.app_user_service.delete(id=app_user_id)

    return {"status": status, "message": "The record has been deleted!"}
