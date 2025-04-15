"""
Purpose:  Provides user to import existing database to the catalog

Prerequisite
1. User creates a connection to the databse 

How it works
1. API Method 1 : Get tables from the database for a given connection
a. User select a connection
b. API understand the type databse (Example: postgre, bigquery, snowflake)
c. It uses sqlalchemy to get the list of schema, tables from  the connection

2. API Method 1 : Import tables to bighammer catalog
a. User select the list of tables to be imported to bighammer catalog
b. for each table, create one entry in datasource and one entry in layout
c. for each column, create one entry in field

Design requrieemtns
1. Ensure the solution works multiple type databses
2. Test it with PostGre, SQLLite
"""

from app.utils.auth_wrapper import authorize
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.api.deps import get_context
from typing import List, Optional
from app.celery_conf.tasks import create_data_source_async

router = APIRouter()


@router.get(
    "/connection_config/{connection_config_id}/get-connection-credentials",
    response_model=dict,
    status_code=200,
)
async def get_connection_credentials(
    *, 
    connection_config_id: int,
    ctx = Depends(get_context),  
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    """Fetch and return stored credentials from AWS Secrets Manager without encryption"""

    return await ctx.connection_config_service.get_credentials(id=connection_config_id)


@router.get(
    "/connection_config/{connection_config_id}/get-schemas",
    response_model=list,
    status_code=200,
)
async def get_connection_credentials(
    *, 
    connection_config_id: int,
    ctx = Depends(get_context),  
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    """Fetch and return stored credentials from AWS Secrets Manager without encryption"""

    return await ctx.connection_config_service.get_schemas_from_db_credentials(id=connection_config_id)


@router.get(
    "/connection_config/{connection_config_id}/schemas/{schema}/tables",
    response_model=List[str],
    status_code=200,
)
async def get_schema_tables(
    *, 
    connection_config_id: int,
    schema: str,
    ctx = Depends(get_context),  
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    """Fetch all tables for a given schema using credentials stored in AWS Secrets Manager"""

    return await ctx.connection_config_service.get_tables_from_db_schema(id=connection_config_id, schema=schema)


@router.post(
    "/connection_config/{connection_config_id}/create_data_source",
    response_model=dict,
    status_code=201,
)
async def create_data_source(
    *,
    bh_project_id: int,
    connection_config_id: int,
    create_description: Optional[bool] = None,
    schema: str,
    tables: List[str],  # List of selected tables
    background_tasks: BackgroundTasks,
    ctx = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    """Create Data Source and Data Source Layout for selected tables"""

    # Validate input
    if not tables:
        raise HTTPException(status_code=400, detail="At least one table must be selected")
    background_tasks.add_task(create_data_source_async, bh_project_id, connection_config_id, schema, tables, create_description, authorized, ctx)
    return {
        "message": "Data source and layouts created successfully",
        "tables": tables
    }
