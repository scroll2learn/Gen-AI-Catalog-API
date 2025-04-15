
from app.models.app_user import (
    AppUser,
    AppUserCreate,
    AppUserUpdate,
    AppUserReturn
)
from app.services.base import BaseService


class AppUserService(BaseService):
    model: AppUser = AppUser
    create_model: AppUserCreate = AppUserCreate
    update_model: AppUserUpdate = AppUserUpdate
    return_schema: AppUserReturn = AppUserReturn
    
