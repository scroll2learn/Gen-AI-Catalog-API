from app.models.joins import (
    Joins,
    JoinsCreate,
    JoinsUpdate,
    JoinsReturn,
    JoinOn,
    JoinOnCreate,
    JoinOnUpdate,
    JoinOnReturn,
)

from app.services.base import BaseService


class JoinsService(BaseService):
    model: Joins = Joins
    create_model: JoinsCreate = JoinsCreate
    update_model: JoinsUpdate = JoinsUpdate
    return_schema: JoinsReturn = JoinsReturn
    name_field: str = 'join_name'
    key_field: str = 'join_key'


class JoinOnService(BaseService):
    model: JoinOn = JoinOn
    create_model: JoinOnCreate = JoinOnCreate
    update_model: JoinOnUpdate = JoinOnUpdate
    return_schema: JoinOnReturn = JoinOnReturn
