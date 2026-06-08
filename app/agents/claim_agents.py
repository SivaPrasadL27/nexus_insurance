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

async def treatment_agent(code):
    valid = code in ["M17"]
    return {
        "value": 0.9 if valid else 0.5,
        "reason": "Valid treatment" if valid else "Unclear mapping"
    }

from datetime import datetime, timedelta, timezone
from app.core.database import SessionLocal
from app.models.claim import Claim


async def fraud_agent(claim_data):

    db = SessionLocal()

    policy_id = claim_data["policy_id"]
    current_amount = claim_data["amount"]

    # ✅ Time window (FIXED)
    last_30_days = datetime.now(timezone.utc) - timedelta(days=30)

    # ✅ Fetch claims
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

    # RULE 1: high frequency
    if claim_count >= 5:
        return {
            "value": 0.2,
            "reason": f"{claim_count} claims in last 30 days"
        }

    # RULE 2: high cumulative amount
    if total_amount + current_amount > 10000:
        return {
            "value": 0.3,
            "reason": "High cumulative claim amount"
        }

    # RULE 3: small claim abuse
    small_claims = [c for c in recent_claims if c.amount < 500]

    if len(small_claims) >= 3:
        return {
            "value": 0.4,
            "reason": "Multiple small claims detected"
        }

    # Default
    return {
        "value": 0.9,
        "reason": "No suspicious patterns"
    }