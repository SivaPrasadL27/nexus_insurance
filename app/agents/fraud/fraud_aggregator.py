from app.agents.fraud.historical_signal import historical_signal
from app.agents.fraud.graph_signal import graph_signal
from app.agents.fraud.llm_signal import llm_signal


async def fraud_agent(claim_data):

    historical = await historical_signal(
        claim_data["policy_id"],
        claim_data["amount"]
    )

    graph = await graph_signal(
        claim_data["hospital"]
    )

    llm = await llm_signal({
        "amount": claim_data["amount"],
        "hospital": claim_data["hospital"]
    })

    final_score = round(
        (
            historical["value"]
            + graph["value"]
            + llm["value"]
        ) / 3,
        2
    )

    return {
        "value": final_score,
        "reason": (
            f"Historical: {historical['reason']} | "
            f"Graph: {graph['reason']} | "
            f"LLM: {llm['reason']}"
        )
    }