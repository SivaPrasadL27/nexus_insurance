from google.adk import Agent
import json


treatment_llm_agent = Agent(
    name="treatment-validator",
    instruction="""
Validate if diagnosis and treatment are medically aligned.

Return ONLY JSON:
{
  "value": float,
  "reason": "short explanation"
}
"""
)


async def treatment_agent(claim_data):

    try:

        response = await treatment_llm_agent.run({
            "diagnosis_code": claim_data["diagnosis"],
            "treatment": claim_data["treatment"]
        })

        output = json.loads(response.output)

        return {
            "value": float(output.get("value", 0.5)),
            "reason": output.get("reason", "Treatment reasoning")
        }

    except Exception as e:

        return {
            "value": 0.5,
            "reason": str(e)
        }