
from app.models.platform_region import (
    PlatformRegion,
    PlatformRegionCreate,
    PlatformRegionUpdate,
    PlatformRegionReturn
)
from app.services.base import BaseService


class PlatformRegionService(BaseService):
    model: PlatformRegion = PlatformRegion
    create_model: PlatformRegionCreate = PlatformRegionCreate
    update_model: PlatformRegionUpdate = PlatformRegionUpdate
    return_schema: PlatformRegionReturn = PlatformRegionReturn
    
