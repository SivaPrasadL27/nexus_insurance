from fastapi import APIRouter

from app.api.schemas.claim_schema import ClaimRequest
from app.orchestration.claim_orchestrator import ClaimOrchestrator
from app.services.claim_service import ClaimService

router = APIRouter()


@router.post("/claim")
async def process_claim(request: ClaimRequest):

    orchestrator = ClaimOrchestrator()

    result = await orchestrator.process_claim(
        request.model_dump()
    )

    return result


@router.get("/claim/{claim_id}")
def get_claim(claim_id: str):

    return ClaimService.get_claim(claim_id)