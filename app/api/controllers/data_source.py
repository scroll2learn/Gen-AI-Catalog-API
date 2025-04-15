from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs

from app.utils.data_source_utils import get_text_embedding
from fastapi import APIRouter, Depends, Query, Request
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.exceptions import DSMissingRequiredParameter
from app.models.base import StatusMessage
from app.models.data_source import (DataSource, DataSourceCreate, DataSourceMetadataCreate,
                                    DataSourceMetadataReturn,
                                    DataSourceMetadataUpdate, DataSourceReturn,
                                    DataSourceUpdate)
from app.utils.auth_wrapper import authorize

router = APIRouter()


@router.get(
    "/list_datasets/",
    status_code=http_status.HTTP_200_OK,
)
async def get_all_datasets(
    *,
    bh_project_id: Optional[int] = None,
    bh_project_cld_id: Optional[str] = None,
    bh_project_name: Optional[str] = None,
    lake_zone_id: Optional[int] = None,
    lake_zone_cd: Optional[int] = None,
    data_src_id: Optional[int] = None,
    data_src_name: Optional[str] = None,
    data_src_key: Optional[str] = None,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.data_source_service.get_all_datasets(
        bh_project_id=bh_project_id,
        bh_project_cld_id=bh_project_cld_id,
        bh_project_name=bh_project_name,
        lake_zone_id=lake_zone_id,
        lake_zone_cd=lake_zone_cd,
        data_src_id=data_src_id,
        data_src_name=data_src_name,
        data_src_key=data_src_key,
    )


@router.get(
    "/dataset_by_project/",
    status_code=http_status.HTTP_200_OK,
)
async def get_all_datasets_by_project(
    *,
    bh_project_id: Optional[int] = None,
    bh_project_cld_id: Optional[str] = None,
    bh_project_name: Optional[str] = None,
    lake_zone_id: Optional[int] = None,
    lake_zone_cd: Optional[int] = None,
    data_src_id: Optional[int] = None,
    data_src_name: Optional[str] = None,
    data_src_key: Optional[str] = None,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):

    datasets = await ctx.data_source_service.get_all_datasets_by_project(
        bh_project_id=bh_project_id,
        bh_project_cld_id=bh_project_cld_id,
        bh_project_name=bh_project_name,
        lake_zone_id=lake_zone_id,
        lake_zone_cd=lake_zone_cd,
        data_src_id=data_src_id,
        data_src_name=data_src_name,
        data_src_key=data_src_key,
    )
    return datasets


@router.get(
    "/list/",
    response_model=List[DataSourceReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_data_sources(
    *,
    data_src_id: Optional[int] = None,
    data_src_name: Optional[str] = None,
    data_src_key: Optional[str] = None,
    data_src_status_cd: Optional[int] = None,
    lake_zone_id: Optional[int] = None,
    connection_config_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'data_src_name', 'data_src_key'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.data_source_service.list(
        data_src_id=data_src_id,
        data_src_name=data_src_name,
        data_src_key=data_src_key,
        data_src_status_cd=data_src_status_cd,
        lake_zone_id=lake_zone_id,
        connection_config_id=connection_config_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/list-by-fields/",
    status_code=http_status.HTTP_200_OK,
)
async def get_all_data_sources(
    *,
    data_src_id: Optional[int] = None,
    data_src_name: Optional[str] = None,
    data_src_key: Optional[str] = None,
    data_src_status_cd: Optional[int] = None,
    lake_zone_id: Optional[int] = None,
    connection_config_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'data_src_name', 'data_src_key'"
    ),
    order_desc: bool = False,
    fields: Optional[str] = Query(
        None, description="Comma-separated fields to include in the response"
    ),
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.data_source_service.list_by_fields(
        data_src_id=data_src_id,
        data_src_name=data_src_name,
        data_src_key=data_src_key,
        data_src_status_cd=data_src_status_cd,
        lake_zone_id=lake_zone_id,
        connection_config_id=connection_config_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
        fields=fields,
    )


@router.get(
    "/search",
    response_model=List[DataSourceReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_field_for_word(
    *,
    params: Optional[str] = Query(
        None, description="Search any field like, data_source_name=abc&data_src_key=cdf"
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.data_source_service.search(params=params)


@router.get(
    "/check_src_exists",
    response_model=bool,
    status_code=http_status.HTTP_200_OK,
)
async def check_data_source_exists(
    data_src_name: Optional[str] = None,
    data_src_key: Optional[str] = None,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    if data_src_name is None and data_src_key is None:
        raise DSMissingRequiredParameter
    return await ctx.data_source_service.check_source_exists(
        data_src_name=data_src_name,
        data_src_key=data_src_key,
    )


@router.get(
    "/{data_src_id}",
    response_model=DataSourceReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_data_source(
    data_src_id: int, 
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    data_source = await ctx.data_source_service.get(data_src_id)
    if data_source.connection_config_id:
        connection_config = await ctx.connection_config_service.get(data_source.connection_config_id)
        data_source.connection_config = connection_config
    return data_source


@router.post(
    "/",
    response_model=DataSourceReturn,
    status_code=http_status.HTTP_201_CREATED,
)
async def create_data_source(
    data_source: DataSourceCreate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    embedding = await get_text_embedding(data_source.data_src_name, data_source.data_src_desc)
    data_source_obj = DataSource(
        **data_source.dict(),
        data_src_embeddings=embedding
    )
    return await ctx.data_source_service.create(data_source_obj, authorized=authorized)


@router.patch(
    "/{data_src_id}",
    response_model=DataSourceReturn,
    status_code=http_status.HTTP_200_OK,
)
async def patch_data_source(
    data_src_id: int,  # Match the name of the path parameter
    data_source: DataSourceUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    current_data_source = await ctx.data_source_service.get(data_src_id)
    updated_fields = []
    if data_source.data_src_name:
        if data_source.data_src_name != current_data_source.data_src_name:
            updated_fields.append('name')
    else:
        data_source.data_src_name = current_data_source.data_src_name
    if data_source.data_src_desc:
        if data_source.data_src_desc != current_data_source.data_src_desc:
            updated_fields.append('desc')
    else:
        data_source.data_src_desc = current_data_source.data_src_desc
    if updated_fields:
        embedding = await get_text_embedding(data_source.data_src_name, data_source.data_src_desc)
        data_source.data_src_embeddings=embedding
    else:
        data_source.data_src_embeddings=current_data_source.data_src_embeddings
    
    return await ctx.data_source_service.update(data_src_id, data_source, authorized=authorized)


@router.delete(
    "/{data_src_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_data_source(
    data_src_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.data_source_service.delete(data_src_id, authorized=authorized)
    return {"status": status, "message": "The record has been deleted!"}


@router.get(
    "/data_src_mtd/list/",
    response_model=List[DataSourceMetadataReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_data_source_metadata(
    *,
    data_src_id: Optional[int] = None,
    data_src_mtd_id: Optional[int] = None,
    data_src_mtd_name: Optional[str] = None,
    data_src_mtd_key: Optional[str] = None,
    data_src_mtd_type_cd: Optional[int] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'data_src_id', 'data_src_mtd_id'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.data_source_mtd_service.list(
        data_src_id=data_src_id,
        data_src_mtd_id=data_src_mtd_id,
        data_src_mtd_name=data_src_mtd_name,
        data_src_mtd_key=data_src_mtd_key,
        data_src_mtd_type_cd=data_src_mtd_type_cd,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/data_src_mtd/search",
    response_model=DataSourceMetadataReturn,
    status_code=http_status.HTTP_200_OK,
)
async def search_data_source_metadata(
    *,
    params: Optional[str] = Query(
        None,
        description="Search any field like, data_src_mtd_id=1&data_src_mtd_name=abc",
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.data_source_mtd_service.search(params=params)


@router.get(
    "/data_src_mtd/{data_src_mtd_id}",
    response_model=DataSourceMetadataReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_data_source_metadata(
    data_src_mtd_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.data_source_mtd_service.get(data_src_mtd_id)


@router.post(
    "/data_src_mtd/",
    response_model=DataSourceMetadataReturn,
    status_code=http_status.HTTP_201_CREATED,
)
async def create_data_source_metadata(
    data_source_metadata: DataSourceMetadataCreate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.data_source_mtd_service.create(data_source_metadata, authorized=authorized)


@router.put(
    "/data_src_mtd/{data_src_mtd_id}",
    response_model=DataSourceMetadataReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_data_source_metadata(
    data_src_mtd_id: int,
    data_source_metadata: DataSourceMetadataUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.data_source_mtd_service.update(
        data_src_mtd_id, data_source_metadata, authorized=authorized
    )


@router.delete(
    "/data_src_mtd/{data_src_mtd_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_data_source_metadata(
    data_src_mtd_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.data_source_mtd_service.delete(data_src_mtd_id, authorized=authorized)
    return {"status": status, "message": "The record has been deleted!"}

@router.get(
    "/vector_search/",
    response_model=List[DataSourceReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_field_for_word(
    *,
    params: Optional[str] = Query(
        None, description="Search any field like, data_source_name=abc&data_src_key=cdf"
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
): 
    
    return await ctx.data_source_service.vector_search(params=params)


@router.get(
    "/semantic-search/",
    response_model=List[DataSourceReturn],
    status_code=http_status.HTTP_200_OK,
)
async def semantic_search(
    query: str = Query(..., description="Enter a full sentence to search related data sources"),
    connection_config_id: int = Query(..., description="Filter by connection config ID"),
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    """
    Search for related data sources based on a full sentence.
    """
    return await ctx.data_source_service.semantic_search(query, connection_config_id)


#TODO only for testing will remove later
@router.get(
    "/semantic-search-2/",
    response_model=List[DataSourceReturn],
    status_code=http_status.HTTP_200_OK,
)
async def semantic_search2(
    query: str = Query(..., description="Enter a full sentence to search related data sources"),
    connection_config_id: int = Query(..., description="Filter by connection config ID"),
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    """
    Search for related data sources based on a full sentence.
    """
    return await ctx.data_source_service.semantic_search2(query, connection_config_id)




@router.post("/generate-datasource-descriptions", response_model=dict)
async def generate_datasource_descriptions(
    request: List[int],
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
    ):
    """
    Generate descriptions for multiple data sources using LLM.
    
    Args:
        request (List[int]): List of data source IDs.
        db (AsyncSession): Database session.
    
    Returns:
        dict: Success message or error details.
    """

    return await ctx.data_source_service.create_description(request=request)


@router.post("/update-datasource-embeddings", response_model=dict)
async def update_datasource_embeddings(
    request: List[int],
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    """
    Update embeddings for data sources and their columns.

    Args:
        request (List[int]): List of data source IDs.

    Returns:
        dict: Success message or error details.
    """

    return await ctx.data_source_service.update_embeddings(request=request)
