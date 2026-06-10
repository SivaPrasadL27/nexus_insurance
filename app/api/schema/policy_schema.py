from pydantic import BaseModel


class PolicyRequest(BaseModel):
    customer_id: str
    age: int
    salary: float
    coverage_amount: float