from fastapi import FastAPI

from app.api.routes.claims import router as claims_router
from app.api.routes.customers import router as customers_router
from app.api.routes.policies import router as policies_router

from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NEXUS Insurance System")

app.include_router(claims_router)
app.include_router(customers_router)
app.include_router(policies_router)


@app.get("/")
def root():
    return {"message": "NEXUS API running"}