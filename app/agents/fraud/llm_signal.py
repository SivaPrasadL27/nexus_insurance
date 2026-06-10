from google.adk import Agent
import json


fraud_llm_agent = Agent(
    name="fraud-analyzer",
    instruction="""
Analyze insurance claim fraud risk.

Return ONLY JSON:
{
  "value": float,
  "reason": "short explanation"
}
"""
)


async def llm_signal(data):

    try:

        response = await fraud_llm_agent.run(data)

        output = json.loads(response.output)

        return {
            "value": float(output.get("value", 0.5)),
            "reason": output.get("reason", "LLM reasoning")
        }

    except Exception as e:

        return {
            "value": 0.5,
            "reason": str(e)
        }