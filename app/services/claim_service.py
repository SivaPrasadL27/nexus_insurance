import uuid
from app.models.claim import Claim

def create_claim(db, data):
    claim = Claim(
        id=str(uuid.uuid4()),
        customer_id=data["customer_id"],
        amount=data["amount"],
        status="created"
    )
    db.add(claim)
    db.commit()
    return claim