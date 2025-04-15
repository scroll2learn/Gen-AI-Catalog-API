
from app.models.release_bundle import (
    BHReleaseBundle,
    BHReleaseBundleCreate,
    BHReleaseBundleUpdate,
    BHReleaseBundleReturn
)
from app.services.base import BaseService


class BHReleaseBundleService(BaseService):
    model: BHReleaseBundle = BHReleaseBundle
    create_model: BHReleaseBundleCreate = BHReleaseBundleCreate
    update_model: BHReleaseBundleUpdate = BHReleaseBundleUpdate
    return_schema: BHReleaseBundleReturn = BHReleaseBundleReturn
    
