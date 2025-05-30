from fastapi import FastAPI
from fastapi import Request
from cost_estimator import router
from app.core.exception_handler import include_exceptions
from app.core.exception_responses import responses

app = FastAPI(
    title="Cost Estimator API",
    description="Handles input validation and formats structured error responses.",
    version="1.0.0",
    responses=responses
)

include_exceptions(app)

app.include_router(router, prefix="/cost-estimator", tags=["Cost Estimation"])

@app.get("/")
def read_root():
    return {"Hello": "World"}
