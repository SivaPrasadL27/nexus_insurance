from datetime import datetime, timedelta, timezone
from app.core.database import SessionLocal
from app.models.claim import Claim
from google.adk import Agent
import json
from app.services.graph_service import GraphService



# Create ADK agent (initialize ONCE)
treatment_llm_agent = Agent(
    name="treatment-validator",
    instruction="""
You are a medical insurance validation expert.

Your job is to evaluate whether a diagnosis code and procedure are valid and medically consistent.

Input:
- diagnosis_code
- treatment_description

Output ONLY JSON:
{
  "value": float (0 to 1),
  "reason": "short explanation"
}

Rules:
- Valid match → 0.8 to 1.0
- Unclear → 0.5
- Invalid → 0.1 to 0.3

Be strict but reasonable.
"""
)

fraud_llm_agent = Agent(
    name="fraud-analyzer",
    instruction="""
You are an insurance fraud detection expert.

Analyze the provided insurance claim behavior.

Evaluate:
- suspicious claim frequency
- abnormal patterns
- risky hospital usage
- excessive claim activity

Output ONLY JSON:

{
  "value": float (0 to 1),
  "reason": "short concise explanation"
}

Scoring:
- 0.8-1.0 = safe
- 0.5 = suspicious
- 0.1-0.3 = highly suspicious

Be conservative and explain reasoning clearly.
"""
)



async def hospital_agent(hospital_name):
    valid = hospital_name.lower() in ["austin medical center"]
    return {
        "value": 1.0 if valid else 0.3,
        "reason": "Verified hospital" if valid else "Unknown hospital"
    }

async def expense_agent(amount):
    if amount < 1500:
        return {"value": 0.9, "reason": "Within normal range"}
    return {"value": 0.4, "reason": "Too high"}

# async def treatment_agent(code):
#     valid = code in ["M17"]
#     return {
#         "value": 0.9 if valid else 0.5,
#         "reason": "Valid treatment" if valid else "Unclear mapping"
#     }

async def treatment_agent(claim_data):
    """
    ADK-powered treatment validation agent
    """

    try:
        #  Prepare input
        prompt_input = {
            "diagnosis_code": claim_data["diagnosis"],
            "treatment_description": claim_data.get("treatment", "general treatment")
        }

        #  Call ADK agent
        response = await treatment_llm_agent.run(prompt_input)

        #  Parse JSON safely
        output = json.loads(response.output)

        return {
            "value": float(output.get("value", 0.5)),
            "reason": output.get("reason", "LLM reasoning")
        }

    except Exception as e:
        #  fallback
        return {
            "value": 0.5,
            "reason": f"Fallback due to error: {str(e)}"
        }




# async def fraud_agent(claim_data):

#     db = SessionLocal()

#     policy_id = claim_data["policy_id"]
#     current_amount = claim_data["amount"]

#     # Time window (FIXED)
#     last_30_days = datetime.now(timezone.utc) - timedelta(days=30)

#     # Fetch claims
#     claims = db.query(Claim).filter(
#         Claim.policy_id == policy_id
#     ).all()

#     db.close()

#     recent_claims = []
#     total_amount = 0

    
#     for c in claims:
#         if c.created_at >= last_30_days:
#             recent_claims.append(c)
#             total_amount += c.amount

#     claim_count = len(recent_claims)

#     # RULE 1: high frequency
#     if claim_count >= 5:
#         return {
#             "value": 0.2,
#             "reason": f"{claim_count} claims in last 30 days"
#         }

#     # RULE 2: high cumulative amount
#     if total_amount + current_amount > 10000:
#         return {
#             "value": 0.3,
#             "reason": "High cumulative claim amount"
#         }

#     # RULE 3: small claim abuse
#     small_claims = [c for c in recent_claims if c.amount < 500]

#     if len(small_claims) >= 3:
#         return {
#             "value": 0.4,
#             "reason": "Multiple small claims detected"
#         }

#     # Default
#     return {
#         "value": 0.9,
#         "reason": "No suspicious patterns"
#     }


async def fraud_agent(claim_data):

    db = SessionLocal()

    policy_id = claim_data["policy_id"]
    current_amount = claim_data["amount"]
    hospital = claim_data["hospital"]

    last_30_days = datetime.now(timezone.utc) - timedelta(days=30)

    #  Fetch historical claims
    claims = db.query(Claim).filter(
        Claim.policy_id == policy_id
    ).all()

    db.close()

    recent_claims = []
    total_amount = 0

    for c in claims:
        if c.created_at >= last_30_days:
            recent_claims.append(c)
            total_amount += c.amount

    claim_count = len(recent_claims)

    # ======================================================
    #  RULE-BASED FRAUD SCORING
    # ======================================================

    rule_score = 0.9
    rule_reason = "No rule-based fraud signals"

    if claim_count >= 5:
        rule_score = 0.2
        rule_reason = "High claim frequency detected"

    elif total_amount + current_amount > 10000:
        rule_score = 0.3
        rule_reason = "High cumulative claim amount"

    elif hospital.lower() not in [
        "austin medical center",
        "st. david's hospital"
    ]:
        rule_score = 0.5
        rule_reason = "Unrecognized hospital network"

    # ======================================================
    #  LLM / ADK FRAUD REASONING
    # ======================================================

    try:

        llm_input = {
            "claim_amount": current_amount,
            "hospital": hospital,
            "historical_claim_count": claim_count,
            "historical_total_amount": total_amount
        }

        response = await fraud_llm_agent.run(llm_input)

        output = json.loads(response.output)

        llm_score = float(output.get("value", 0.5))
        llm_reason = output.get("reason", "LLM fraud reasoning")

    except Exception as e:

        llm_score = 0.5
        llm_reason = f"Fallback LLM error: {str(e)}"

    # ======================================================
    #  HYBRID COMBINATION
    # ======================================================

    # final_score = round((rule_score + llm_score) / 2, 2)
    final_score = round(
    (rule_score + llm_score + graph_score) / 3,
    2
    )

    return {
        "value": final_score,
        "reason": (
            # f"Rule: {rule_reason} | "
            # f"LLM: {llm_reason}"
            
            f"Rule: {rule_reason} | "
            f"LLM: {llm_reason} | "
            f"Graph: {graph_reason}"

        )
    }