import asyncio
from app.agents.claim_agents import hospital_agent, expense_agent, treatment_agent
from app.engines.tse import TruthScoreEngine

class ClaimPipeline:

    def __init__(self):
        self.tse = TruthScoreEngine()

    async def run(self, claim_data):

        # ✅ Parallel execution
        hospital, expense, treatment = await asyncio.gather(
            hospital_agent(claim_data["hospital"]),
            expense_agent(claim_data["amount"]),
            treatment_agent(claim_data["diagnosis"])
        )

        scores = {
            "hospital": hospital,
            "expense": expense,
            "treatment": treatment
        }

        result = self.tse.compute(scores)

        return result