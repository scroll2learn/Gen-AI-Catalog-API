from fastapi import Depends
from app.api.deps import get_context
from app.core.context import Context

async def create_data_source_async(
    bh_project_id, connection_config_id, schema, tables, create_description, authorized,  ctx: Context = Depends(get_context)
):
    """Handles the full pipeline of data source creation asynchronously."""
    print("Creating data source and layout for each table")
    created_data_sources, data_source_ids = await ctx.connection_config_service.create_data_source_and_layout_for_each_table(
        connection_config_id=connection_config_id,
        schema=schema,
        tables=tables,
        bh_project_id=bh_project_id,
        authorized=authorized,
    )

    if create_description:
        await ctx.data_source_service.create_description(request=data_source_ids)
        await ctx.data_source_service.update_embeddings(request=data_source_ids)

    return {
        "message": "Data source and layouts created successfully",
        "tables": tables,
    }
