import uuid
import json

from app.core.database import SessionLocal
from app.models.claim import Claim
from app.models.decision import Decision


class ClaimService:

    @staticmethod
    def create_claim(data):

        db = SessionLocal()

        claim = Claim(
            id=str(uuid.uuid4()),
            customer_id=data.get("customer_id", "unknown"),
            policy_id=data["policy_id"],
            amount=data["amount"],
            status="processing"
        )

        db.add(claim)
        db.commit()
        db.refresh(claim)

        db.close()

        return claim

    @staticmethod
    def store_decision(claim_id, result):

        db = SessionLocal()

        decision = Decision(
            id=str(uuid.uuid4()),
            entity_id=claim_id,
            decision=result["decision"],
            confidence=result["confidence"],
            evidence=json.dumps(result["evidence"])
        )

        db.add(decision)
        db.commit()

        db.close()

    @staticmethod
    def update_claim_status(claim_id, status):

        db = SessionLocal()

        claim = db.query(Claim).filter(
            Claim.id == claim_id
        ).first()

        claim.status = status

        db.commit()
        db.close()

    @staticmethod
    def get_claim(claim_id):

        db = SessionLocal()

        claim = db.query(Claim).filter(
            Claim.id == claim_id
        ).first()

        decision = db.query(Decision).filter(
            Decision.entity_id == claim_id
        ).first()

        db.close()

        if not claim:
            return {"error": "Claim not found"}

        return {
            "claim_id": claim.id,
            "customer_id": claim.customer_id,
            "policy_id": claim.policy_id,
            "amount": claim.amount,
            "status": claim.status,
            "decision": decision.decision if decision else None,
            "confidence": decision.confidence if decision else None,
            "evidence": json.loads(decision.evidence) if decision else None
        }