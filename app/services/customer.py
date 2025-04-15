
from app.models.customer import (
    Customer,
    CustomerCreate,
    CustomerUpdate,
    CustomerReturn,
    ConnectionDtl,
    ConnectionDtlCreate,
    ConnectionDtlUpdate,
    ConnectionDtlReturn,
   
)
from app.services.base import BaseService



class CustomerService(BaseService):
    model: Customer = Customer
    create_model: CustomerCreate = CustomerCreate
    update_model: CustomerUpdate = CustomerUpdate
    return_schema: CustomerReturn = CustomerReturn


class ConnectionDtlService(BaseService):
    model: ConnectionDtl = ConnectionDtl
    create_model: ConnectionDtlCreate = ConnectionDtlCreate
    update_model: ConnectionDtlUpdate = ConnectionDtlUpdate
    return_schema: ConnectionDtlReturn = ConnectionDtlReturn

    # update_model: ConnectionDtlUpdate = ConnectionDtlUpdate
    # return_schema: ConnectionDtlReturn = ConnectionDtlReturn
