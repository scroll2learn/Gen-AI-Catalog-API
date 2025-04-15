from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.models.base import StatusMessage
from app.models.codes_hdr import (CodesDtlCreate, CodesDtlReturn,
                                  CodesDtlUpdate, CodesHdrCreate,
                                  CodesHdrReturn, CodesHdrUpdate)
from app.utils.auth_wrapper import authorize

router = APIRouter()


@router.get(
    "/list/",
    response_model=List[CodesHdrReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_codes_hdr(
    *,
    id: Optional[int] = None,
    type_cd: Optional[str] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'codes_hdr_id', 'codes_hdr_name'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view"))
):
    return await ctx.codes_hdr_service.list(
        id=id,
        type_cd=type_cd,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/{codes_hdr_id}",
    response_model=CodesHdrReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_codes_hdr(
    *,
    codes_hdr_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view"))
):
    return await ctx.codes_hdr_service.get(id=codes_hdr_id)


@router.post(
    "",
    response_model=CodesHdrReturn,
    status_code=http_status.HTTP_200_OK,
)
async def create_codes_hdr(
    *,
    obj: CodesHdrCreate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit"))
):
    return await ctx.codes_hdr_service.create(obj=obj)


@router.put(
    "/{codes_hdr_id}",
    response_model=CodesHdrReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_by_codes_hdr_id(
    *,
    codes_hdr_id: int,
    obj: CodesHdrUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit"))
):
    return await ctx.codes_hdr_service.update(id=codes_hdr_id, obj=obj)


@router.delete(
    "/{codes_hdr_id}", response_model=StatusMessage, status_code=http_status.HTTP_200_OK
)
async def delete_codes_hdr_by_id(
    codes_hdr_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    status = await ctx.codes_hdr_service.delete(id=codes_hdr_id)

    return {"status": status, "message": "The record has been deleted!"}


@router.get(
    "/codes_dtl/",
    response_model=List[CodesDtlReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_codes_dtl(
    *,
    id: Optional[int] = None,
    codes_hdr_id: Optional[int] = None,
    dtl_desc: Optional[str] = None,
    dtl_id_filter: Optional[int] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'codes_dtl_id', 'codes_dtl_name'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view"))
):
    return await ctx.codes_dtl_service.list(
        id=id,
        codes_hdr_id=codes_hdr_id,
        dtl_desc=dtl_desc,
        dtl_id_filter=dtl_id_filter,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/codes_dtl/{id}",
    response_model=CodesDtlReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_codes_dtl(
    *,
    id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view"))
):
    return await ctx.codes_dtl_service.get(id=id)


@router.post(
    "/codes_dtl",
    response_model=CodesHdrReturn,
    status_code=http_status.HTTP_200_OK,
)
async def create_codes_dtl(
    *, obj: CodesDtlCreate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.codes_dtl_service.create(obj=obj)


@router.put(
    "/codes_dtl/{id}",
    response_model=CodesHdrReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_by_codes_dtl_id(
    *, id: int, obj: CodesDtlUpdate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.codes_dtl_service.update(id=id, obj=obj)


@router.delete(
    "/codes_dtl/{id}", response_model=StatusMessage, status_code=http_status.HTTP_200_OK
)
async def delete_codes_dtl_by_id(
    id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.codes_dtl_service.delete(id=id)

    return {"status": status, "message": "The record has been deleted!"}
