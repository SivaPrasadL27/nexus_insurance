import asyncio
from app.agents.claim_agents import (
    hospital_agent,
    expense_agent,
    treatment_agent,
    fraud_agent
)

from app.engines.tse import TruthScoreEngine
from app.core.database import SessionLocal
from app.models.policy import Policy


class ClaimPipeline:

    def __init__(self):
        self.tse = TruthScoreEngine()

    async def run(self, claim_data):

        db = SessionLocal()

        # ✅ Step 1: Fetch policy
        policy = db.query(Policy).filter(
            Policy.id == claim_data["policy_id"]
        ).first()

        if not policy:
            db.close()
            return {
                "decision": "reject",
                "confidence": 0.0,
                "level": "low",
                "evidence": [
                    {
                        "agent": "policy_check",
                        "score": 0.0,
                        "reason": "Invalid policy_id"
                    }
                ]
            }

        # ✅ Step 2: Coverage scoring (NEW)
        if claim_data["amount"] <= policy.coverage_amount:
            coverage_score = {
                "value": 0.95,
                "reason": f"Within coverage ({policy.coverage_amount})"
            }
        else:
            coverage_score = {
                "value": 0.2,
                "reason": f"Exceeds coverage limit ({policy.coverage_amount})"
            }

        # ✅ Step 3: Parallel AI agents
        hospital, expense, treatment = await asyncio.gather(
            hospital_agent(claim_data["hospital"]),
            expense_agent(claim_data["amount"]),
            # treatment_agent(claim_data["diagnosis"]),
            treatment_agent(claim_data),
            fraud_agent(claim_data)
        )

        # ✅ Step 4: Combine scores (UPDATED)
        scores = {
            "hospital": hospital,
            "expense": expense,
            "treatment": treatment,
            "coverage": coverage_score,
            "fraud": fraud
        }

        db.close()

        # ✅ Step 5: TSE decision
        result = self.tse.compute(scores)

        return result