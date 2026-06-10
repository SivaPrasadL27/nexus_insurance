from pydantic import BaseModel


class CustomerRequest(BaseModel):
    name: str
    age: int
    salary: float
    address: str