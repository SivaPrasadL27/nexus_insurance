from app.services.graph_service import GraphService


async def graph_signal(hospital):

    result = GraphService.hospital_risk_score(
        hospital
    )

    return {
        "value": result["score"],
        "reason": result["reason"]
    }