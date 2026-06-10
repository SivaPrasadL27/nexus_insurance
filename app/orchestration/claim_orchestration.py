from app.pipelines.claim_pipeline import ClaimPipeline
from app.services.claim_service import ClaimService
from app.services.graph_service import GraphService


class ClaimOrchestrator:

    async def process_claim(self, claim_data):

        claim = ClaimService.create_claim(claim_data)

        pipeline = ClaimPipeline()

        result = await pipeline.run(claim_data)

        ClaimService.store_decision(
            claim.id,
            result
        )

        ClaimService.update_claim_status(
            claim.id,
            result["decision"]
        )

        GraphService.create_claim_graph(
            customer_id=claim.customer_id,
            policy_id=claim.policy_id,
            claim_id=claim.id,
            hospital=claim_data["hospital"],
            amount=claim_data["amount"]
        )

        return {
            "claim_id": claim.id,
            "result": result
        }