from app.models.pulish_data import (
    PublishDetails,
    PublishDetailsCreate,
    PublishDetailsUpdate,
    PublishDetailsReturn,
    PublishQueryDetails,
    PublishQueryDetailsCreate,
    PublishQueryDetailsUpdate,
    PublishQueryDetailsReturn,
)
from app.services.base import BaseService

class PublishDetailsService(BaseService):
    model: PublishDetails = PublishDetails
    create_model: PublishDetailsCreate = PublishDetailsCreate
    update_model: PublishDetailsUpdate = PublishDetailsUpdate
    return_schema: PublishDetailsReturn = PublishDetailsReturn

class PublishQueryDetailsService(BaseService):
    model: PublishQueryDetails = PublishQueryDetails
    create_model: PublishQueryDetailsCreate = PublishQueryDetailsCreate
    update_model: PublishQueryDetailsUpdate = PublishQueryDetailsUpdate
    return_schema: PublishQueryDetailsReturn = PublishQueryDetailsReturn
