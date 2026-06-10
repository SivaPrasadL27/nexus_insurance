import uuid

from app.core.database import SessionLocal
from app.models.customer import Customer
from app.models.policy import Policy
from app.models.claim import Claim


class CustomerService:

    @staticmethod
    def create_customer(data):

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

    @staticmethod
    def get_customer(customer_id):

        db = SessionLocal()

        customer = db.query(Customer).filter(
            Customer.id == customer_id
        ).first()

        policies = db.query(Policy).filter(
            Policy.customer_id == customer_id
        ).all()

        claims = db.query(Claim).filter(
            Claim.customer_id == customer_id
        ).all()

        db.close()

        if not customer:
            return {"error": "Customer not found"}

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
                }
                for p in policies
            ],
            "claims": [
                {
                    "claim_id": c.id,
                    "policy_id": c.policy_id,
                    "amount": c.amount,
                    "status": c.status
                }
                for c in claims
            ]
        }