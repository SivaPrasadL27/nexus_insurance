from datetime import datetime, timedelta, timezone

from app.core.database import SessionLocal
from app.models.claim import Claim


async def historical_signal(policy_id, current_amount):

    db = SessionLocal()

    claims = db.query(Claim).filter(
        Claim.policy_id == policy_id
    ).all()

    db.close()

    last_30_days = datetime.now(
        timezone.utc
    ) - timedelta(days=30)

    recent_claims = []
    total_amount = 0

    for c in claims:
        if c.created_at >= last_30_days:
            recent_claims.append(c)
            total_amount += c.amount

    claim_count = len(recent_claims)

    if claim_count >= 5:
        return {
            "value": 0.2,
            "reason": "High claim frequency"
        }

    if total_amount + current_amount > 10000:
        return {
            "value": 0.3,
            "reason": "High cumulative amount"
        }

    return {
        "value": 0.9,
        "reason": "Historical pattern normal"
    }