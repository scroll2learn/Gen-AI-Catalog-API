from app.models.fld_recommendations import (
    FieldRecommendations,
    FieldRecommendationsCreate,
    FieldRecommendationsUpdate,
    FieldRecommendationsReturn,
)

from app.services.base import BaseService
from typing import List

class FieldRecommendationsService(BaseService):
    model: FieldRecommendations = FieldRecommendations
    create_model: FieldRecommendationsCreate = FieldRecommendationsCreate
    update_model: FieldRecommendationsUpdate = FieldRecommendationsUpdate
    return_schema: FieldRecommendationsReturn = FieldRecommendationsReturn


    async def create_field_recommendations(
            self,
            flds_recommendations_list: List[FieldRecommendationsCreate]
            ) -> List[FieldRecommendationsReturn]:
        new_list = [self.model.from_orm(obj) for obj in flds_recommendations_list]
        self.context.db_session.add_all(new_list)
        await self.context.db_session.commit()
        for obj in new_list:
            await self.context.db_session.refresh(obj)
        return new_list
