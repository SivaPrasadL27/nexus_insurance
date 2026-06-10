from fastapi import APIRouter

from app.api.schemas.customer_schema import CustomerRequest
from app.services.customer_service import CustomerService

router = APIRouter()


@router.post("/customer")
def create_customer(request: CustomerRequest):

    return CustomerService.create_customer(
        request.model_dump()
    )


@router.get("/customer/{customer_id}")
def get_customer(customer_id: str):

    return CustomerService.get_customer(customer_id)