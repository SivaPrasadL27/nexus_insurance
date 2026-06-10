from pydantic import BaseModel


class ClaimRequest(BaseModel):
    policy_id: str
    hospital: str
    amount: float
    diagnosis: str
    treatment: str