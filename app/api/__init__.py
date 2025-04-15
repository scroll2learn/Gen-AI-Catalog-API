from fastapi import APIRouter

from app.api.controllers import (
    bh_project,
    data_source,
    data_source_layout,
    layout_fields,
    layout_fields_dq,
    bh_user,
    app_user,
    codes_hdr,
    fld_dq_types,
    platform_region,
    customer,
    engine_integrations,
    author_data,
    fld_properties,
    fld_recommendations,
    pipelines,
    publish_data,
    aws,
    connection_registry,
    flow,
    env_zone,
    schema,
    release_bundle,
    bh_airflow,
    import_db_catalog,
    bh_cluster,
    user_detail
)

api_router = APIRouter()
api_router.include_router(user_detail.router, prefix="/bh-user-detail", tags=['User Detail Endpoints'])
api_router.include_router(bh_project.router, prefix='/bh_project', tags=['BigHammer Project'])
api_router.include_router(data_source.router, prefix='/data_source', tags=['Data Source'])
api_router.include_router(data_source_layout.router, prefix='/data_source_layout', tags=['Data Source Layout'])
api_router.include_router(layout_fields.router, prefix='/layout_fields', tags=['Layout Fields'])
api_router.include_router(layout_fields_dq.router, prefix='/layout_fields_dq', tags=['Layout Fields DQ'])
api_router.include_router(bh_user.router, prefix='/bh_user', tags=['BigHammer User'])
api_router.include_router(app_user.router, prefix='/app_user', tags=['BigHammer App User'])
api_router.include_router(codes_hdr.router, prefix='/codes_hdr', tags=['Code Tables'])
api_router.include_router(fld_dq_types.router, prefix='/fld_dq_types', tags=['Field DQ Types'])
api_router.include_router(platform_region.router, prefix='/platform_region', tags=['Platform Region Data'])
api_router.include_router(customer.router, prefix='/customer', tags=['Customer Data'])
api_router.include_router(engine_integrations.router, prefix='/engine_integrations', tags=['Engine Integrations'])
api_router.include_router(author_data.router, prefix='/author_data', tags=['Author Data'])
api_router.include_router(fld_properties.router, prefix='/field_properties', tags=['Field Properties'])
api_router.include_router(fld_recommendations.router, prefix='/field_recommendations', tags=['Field Recommendations'])
api_router.include_router(pipelines.router, prefix='/pipeline', tags=['Pipeline'])
api_router.include_router(publish_data.router, prefix='/publish_data', tags=['Publish Data'])
api_router.include_router(aws.router, prefix='/aws', tags=['aws'])
api_router.include_router(connection_registry.router, prefix='/connection_registry', tags=['connection_registry'])
api_router.include_router(import_db_catalog.router, prefix="/import_db_catalog", tags=['Import DB Catalog'])
api_router.include_router(flow.router, prefix='/flow', tags=['flow'])
api_router.include_router(env_zone.router, prefix='/environment', tags=['Environment'])
api_router.include_router(schema.router, prefix='/schema', tags=['Schema'])
api_router.include_router(release_bundle.router, prefix="/release_bundle", tags=['Release Bundle'])
api_router.include_router(bh_airflow.router, prefix="/bh_airflow", tags=['Airflow Endpoints'])
api_router.include_router(bh_cluster.router, prefix="/bh_cluster", tags=['Cluster Endpoints'])
