from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Request
from cost_estimator import router  # Import your router module

from exception_handlers import include_exceptions  # Import the exception setup

app = FastAPI()

# Include all exception handlers
include_exceptions(app)

# Include your business router
app.include_router(router, prefix="/cost-estimator", tags=["Cost Estimation"])

@app.get("/")
def read_root():
    return {"Hello": "World"}
