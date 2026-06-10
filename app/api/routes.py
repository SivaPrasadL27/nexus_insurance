from fastapi import APIRouter
from app.pipelines.claim_pipeline import ClaimPipeline
from app.services.graph_service import GraphService
from app.core.database import SessionLocal
from app.models.claim import Claim
from app.models.decision import Decision
from app.models.customer import Customer

import uuid
import json

router = APIRouter()


@router.post("/claim")
async def process_claim(data: dict):

    db = SessionLocal()

    # # Create claim
    # claim = Claim(
    #     id=str(uuid.uuid4()),
    #     customer_id=data.get("customer_id", "unknown"),
    #     amount=data["amount"],
    #     status="processing"
    # )

    # ✅ Validate policy exists
    policy = db.query(Policy).filter(Policy.id == data["policy_id"]).first()

    if not policy:
     db.close()
     return {"error": "Invalid policy_id"}

    # ✅ Create claim linked to policy
    claim = Claim(
        id=str(uuid.uuid4()),
        customer_id=policy.customer_id,
        policy_id=policy.id,
        amount=data["amount"],
        status="processing"
        )


    db.add(claim)
    db.commit()

    # Run pipeline
    pipeline = ClaimPipeline()
    result = await pipeline.run(data)

    # Store decision
    decision = Decision(
        id=str(uuid.uuid4()),
        entity_id=claim.id,
        decision=result["decision"],
        confidence=result["confidence"],
        evidence=json.dumps(result["evidence"])
    )

    db.add(decision)

    claim.status = result["decision"]

    # ✅ Push to Neo4j graph
    GraphService.create_claim_graph(
    customer_id=claim.customer_id,
    policy_id=claim.policy_id,
    claim_id=claim.id,
    hospital=data["hospital"],
    amount=data["amount"]
)

    db.commit()
    
    claim_id = claim.id

    db.close()

    return {
        "claim_id": claim_id,
        "result": result
    }

@router.get("/claim/{claim_id}")
def get_claim(claim_id: str):

    db = SessionLocal()

    # Fetch claim
    claim = db.query(Claim).filter(Claim.id == claim_id).first()

    if not claim:
        db.close()
        return {"error": "Claim not found"}

    # Fetch decision
    decision = db.query(Decision).filter(Decision.entity_id == claim_id).first()

    db.close()

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

from app.models.policy import Policy

@router.post("/policy")
def create_policy(data: dict):

    db = SessionLocal()

    # Step 1: Run Policy Pipeline
    from app.pipelines.policy_pipeline import PolicyPipeline

    pipeline = PolicyPipeline()
    result = pipeline.run(data)

    # ✅ Step 2: Create policy record
    policy = Policy(
        id=str(uuid.uuid4()),
        customer_id=data.get("customer_id", "unknown"),
        premium=result["premium"],
        status=result["decision"],
        coverage_amount=data.get("coverage_amount", 5000),  # default
        policy_type="medical"
    )

    db.add(policy)
    db.commit()

    # ✅ FIX: grab ID before closing session
    policy_id = policy.id

    db.close()

    # ✅ Step 3: Return structured response
    return {
        "policy_id": policy_id,
        "premium": result["premium"],
        "decision": result["decision"]
    }

@router.get("/policy/{policy_id}")
def get_policy(policy_id: str):

    db = SessionLocal()

    policy = db.query(Policy).filter(Policy.id == policy_id).first()

    db.close()

    if not policy:
        return {"error": "Policy not found"}

    return {
        "policy_id": policy.id,
        "customer_id": policy.customer_id,
        "premium": policy.premium,
        "status": policy.status
    }

@router.post("/customer")
def create_customer(data: dict):

    db = SessionLocal()

    customer = Customer(
        id=str(uuid.uuid4()),
        name=data["name"],
        age=data["age"],
        salary=data["salary"],
        address=data["address"]
    )

    db.add(customer)
    db.commit()

    customer_id = customer.id
    db.close()

    return {
        "customer_id": customer_id,
        "message": "Customer created"
    }

@router.get("/customer/{customer_id}")
def get_customer(customer_id: str):

    db = SessionLocal()

    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        db.close()
        return {"error": "Customer not found"}

    # ✅ Fetch policies
    policies = db.query(Policy).filter(Policy.customer_id == customer_id).all()

    # ✅ Fetch claims
    claims = db.query(Claim).filter(Claim.customer_id == customer_id).all()

    db.close()

    return {
        "customer_id": customer.id,
        "name": customer.name,
        "age": customer.age,
        "salary": customer.salary,
        "address": customer.address,
        "policies": [
            {
                "policy_id": p.id,
                "premium": p.premium,
                "status": p.status
            } for p in policies
        ],
        "claims": [
            {
                "claim_id": c.id,
                "policy_id": c.policy_id,
                "amount": c.amount,
                "status": c.status
            } for c in claims
        ]
    }