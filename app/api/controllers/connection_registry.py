import json
import os
from typing import List, Optional, Union
from urllib.parse import parse_qs

from fastapi import APIRouter, Body, Depends, HTTPException, Query, Request
from fastapi import status as http_status
from fastapi.responses import JSONResponse

from app.api.deps import get_context
from app.connections.destination.models.bigquery import DestinationBigquery
from app.connections.destination.models.snowflake import DestinationSnowflake
from app.connections.source.models.bigquery import SourceBigQuery
from app.connections.source.models.snowflake import SourceSnowflake
from app.core.context import Context
from app.enums.connection_registry import (ConnectionStatusEnum,
                                           ConnectionTypes, GeographyEnum,
                                           SourceType)
from app.models.base import StatusMessage
from app.models.connection_registry import (ConnectionConfigCreate,
                                            ConnectionConfigReturn,
                                            ConnectionConfigUpdate,
                                            ConnectionRegistryCreate,
                                            ConnectionRegistryReturn,
                                            ConnectionRegistryUpdate)
from app.utils.auth_wrapper import authorize

router = APIRouter()


@router.get(
    "/list/",
    response_model=List[ConnectionRegistryReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_connection_registry(
    *,
    id: Optional[int] = None,
    connection_name: Optional[str] = None,
    connection_id: Optional[int] = None,
    connection_type: Optional[ConnectionTypes] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'connection_name'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    return await ctx.connection_registry.list(
        id=id,
        connection_name=connection_name,
        connection_id=connection_id,
        connection_type=connection_type,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/search",
    response_model=List[ConnectionRegistryReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_field_for_word(
    *,
    params: Optional[str] = Query(
        None, description="Search any field like, connection_name=abc"
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.connection_registry.search(params=params)


@router.get(
    "/{id}",
    response_model=ConnectionRegistryReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_connection_registry_by_id(
    *,
    id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    return await ctx.connection_registry.get(id=id)


@router.post(
    "",
    response_model=ConnectionRegistryReturn,
    status_code=http_status.HTTP_200_OK,
)
async def create_connection_registry(
    *, obj: ConnectionRegistryCreate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.connection_registry.create(obj=obj, authorized=authorized)


@router.put(
    "/{id}",
    response_model=ConnectionRegistryReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_connection_registry(
    *, id: int, obj: ConnectionRegistryUpdate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.connection_registry.update(id=id, obj=obj, authorized=authorized)


@router.delete(
    "/{id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_connection_registry_by_id(
    *, id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.connection_registry.delete(id=id, authorized=authorized)
    return {"status": status, "message": "The record has been deleted!"}


@router.get(
    "/connection_config/list/",
    response_model=List[ConnectionConfigReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_connection_config(
    *,
    id: Optional[int] = None,
    connection_name: Optional[str] = None,
    connection_config_name: Optional[str] = None,
    connection_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'connection_name'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    return await ctx.connection_config_service.list(
        id=id,
        connection_name=connection_name,
        connection_config_name=connection_config_name,
        connection_id=connection_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/connection_config/search",
    response_model=List[ConnectionConfigReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_field_for_word(
    *,
    params: Optional[str] = Query(
        None, description="Search any field like, connection_name=abc"
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.connection_config_service.search(params=params)


@router.get(
    "/connection_config/{id}",
    response_model=ConnectionConfigReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_connection_config_by_id(
    *,
    id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    return await ctx.connection_config_service.get_with_values(id=id)


@router.post(
    "/connection_config",
    response_model=ConnectionConfigReturn,
    status_code=http_status.HTTP_200_OK,
)
async def create_connection_config(
    *, obj: ConnectionConfigCreate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):

    return await ctx.connection_config_service.create(obj, authorized=authorized)


@router.put(
    "/connection_config/{id}",
    response_model=ConnectionConfigReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_connection_config(
    *, id: int, obj: ConnectionConfigUpdate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.connection_config_service.update_config(id=id, item_body=obj, authorized=authorized)


@router.delete(
    "/connection_config/{id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_connection_config_by_id(
    *, id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.connection_config_service.delete(id=id, authorized=authorized)
    return {"status": status, "message": "The record has been deleted!"}


@router.get("/connections_json/list/", status_code=http_status.HTTP_200_OK)
async def get_all_connections(
    *, connection_type: ConnectionTypes, connection_name: str,
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):

    json_file_path = f"app/connections/{connection_type.value}/{connection_name}.json"
    # Check if the JSON file exists
    if not os.path.exists(json_file_path):
        raise HTTPException(status_code=404, detail="JSON file not found")

    try:
        # Read the JSON file
        with open(json_file_path, "r") as file:
            json_content = json.load(file)
            return JSONResponse(content=json_content)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error reading JSON file: {str(e)}"
        )
