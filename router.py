from fastapi import APIRouter
from app.core.constants import (
    API_VERSION_V1,
    SERVER_ROOT_PATH,
    INDEX_ROUTES_TAG
)

from app.api.routes import index, cost_estimator

api_router = APIRouter()

# Include health check
api_router.include_router(
    index.router,
    prefix=f"{SERVER_ROOT_PATH}{API_VERSION_V1}",
    tags=[INDEX_ROUTES_TAG]
)

# Include cost estimation
api_router.include_router(
    cost_estimator.router,
    prefix=f"{SERVER_ROOT_PATH}{API_VERSION_V1}/estimate",
    tags=["Cost Estimator"]
)