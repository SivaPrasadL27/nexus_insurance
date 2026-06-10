import asyncio

from app.agents.claim_agents import (
    hospital_agent,
    expense_agent
)

from app.agents.treatment_agent import treatment_agent

from app.agents.fraud.fraud_aggregator import fraud_agent

from app.core.database import SessionLocal
from app.models.policy import Policy

from app.rules.coverage_rules import coverage_signal

from app.tse.engine import TruthScoreEngine


class ClaimPipeline:

    def __init__(self):
        self.tse = TruthScoreEngine()

    async def run(self, claim_data):

        db = SessionLocal()

        policy = db.query(Policy).filter(
            Policy.id == claim_data["policy_id"]
        ).first()

        db.close()

        if not policy:
            return {
                "decision": "reject",
                "confidence": 0.0,
                "level": "low",
                "evidence": [
                    {
                        "agent": "policy_check",
                        "score": 0.0,
                        "reason": "Invalid policy"
                    }
                ]
            }

        coverage = coverage_signal(
            claim_data["amount"],
            policy.coverage_amount
        )

        hospital, expense, treatment, fraud = await asyncio.gather(
            hospital_agent(claim_data["hospital"]),
            expense_agent(claim_data["amount"]),
            treatment_agent(claim_data),
            fraud_agent(claim_data)
        )

        scores = {
            "hospital": hospital,
            "expense": expense,
            "treatment": treatment,
            "coverage": coverage,
            "fraud": fraud
        }

        return self.tse.compute(scores)