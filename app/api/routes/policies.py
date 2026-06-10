from fastapi import APIRouter

from app.api.schemas.policy_schema import PolicyRequest
from app.services.policy_service import PolicyService

router = APIRouter()


@router.post("/policy")
def create_policy(request: PolicyRequest):

    return PolicyService.create_policy(
        request.model_dump()
    )


@router.get("/policy/{policy_id}")
def get_policy(policy_id: str):

    return PolicyService.get_policy(policy_id)