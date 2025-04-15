
from app.models.codes_hdr import (
    CodesHdr,
    CodesHdrCreate,
    CodesHdrUpdate,
    CodesHdrReturn
)
from app.models.codes_hdr import (
    CodesDtl,
    CodesDtlCreate,
    CodesDtlUpdate,
    CodesDtlReturn,
)
from app.services.base import BaseService
from sqlalchemy import select, desc
from typing import Optional, List

class CodesHdrService(BaseService):
    model: CodesHdr = CodesHdr
    create_model: CodesHdrCreate = CodesHdrCreate
    update_model: CodesHdrUpdate = CodesHdrUpdate
    return_schema: CodesHdrReturn = CodesHdrReturn

    async def list(
            self,
            offset: int = 0,
            limit: int = 10,
            order_by: Optional[str] = None,
            order_desc: bool = False,
            **kwargs,
            ) -> List[return_schema]:
        
        query = select(self.model)

        # To provide filter on input fields
        for kw in kwargs.keys():
            if kwargs.keys():
                if kwargs[kw] is not None:
                    query = query.where(getattr(self.model, kw) == kwargs[kw])

        query = query.offset(offset).limit(limit)
        
        if order_by:
            order_expression = getattr(self.model, order_by)
            if order_desc:
                order_expression = desc(order_expression)
            query = query.order_by(order_expression)

        results = await self.context.db_session.execute(query)

        return [self.return_schema.from_orm(result) for result in results.scalars()]
    


class CodesDtlService(BaseService):
    model: CodesDtl = CodesDtl
    create_model: CodesDtlCreate = CodesDtlCreate
    update_model: CodesDtlUpdate = CodesDtlUpdate
    return_schema: CodesDtlReturn = CodesDtlReturn

    async def list(
            self,
            offset: int = 0,
            limit: int = 10,
            order_by: Optional[str] = None,
            order_desc: bool = False,
            **kwargs,
            ) -> List[return_schema]:
        
        query = select(self.model)

        # To provide filter on input fields
        for kw in kwargs.keys():
            if kwargs.keys():
                if kwargs[kw] is not None:
                    query = query.where(getattr(self.model, kw) == kwargs[kw])

        query = query.offset(offset).limit(limit)
        
        if order_by:
            order_expression = getattr(self.model, order_by)
            if order_desc:
                order_expression = desc(order_expression)
            query = query.order_by(order_expression)

        results = await self.context.db_session.execute(query)

        return [self.return_schema.from_orm(result) for result in results.scalars()]
    
