import uuid

from app.core.database import SessionLocal
from app.models.policy import Policy
from app.pipelines.policy_pipeline import PolicyPipeline


class PolicyService:

    @staticmethod
    def create_policy(data):

        db = SessionLocal()

        pipeline = PolicyPipeline()

        result = pipeline.run(data)

        policy = Policy(
            id=str(uuid.uuid4()),
            customer_id=data["customer_id"],
            premium=result["premium"],
            status=result["decision"],
            coverage_amount=data["coverage_amount"],
            policy_type="medical"
        )

        db.add(policy)
        db.commit()

        policy_id = policy.id

        db.close()

        return {
            "policy_id": policy_id,
            "premium": result["premium"],
            "decision": result["decision"]
        }

    @staticmethod
    def get_policy(policy_id):

        db = SessionLocal()

        policy = db.query(Policy).filter(
            Policy.id == policy_id
        ).first()

        db.close()

        if not policy:
            return {"error": "Policy not found"}

        return {
            "policy_id": policy.id,
            "customer_id": policy.customer_id,
            "premium": policy.premium,
            "coverage_amount": policy.coverage_amount,
            "status": policy.status
        }