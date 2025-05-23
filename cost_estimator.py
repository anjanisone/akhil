from fastapi import APIRouter, status, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
from CostShareCalculator import HealthInsurancePlan
from cost_estimation_input import CostEstimatorRequest  # ✅ your external model

router = APIRouter()


@router.post("/estimate", status_code=status.HTTP_200_OK)
def estimate_out_of_pocket(payload: CostEstimatorRequest):
    try:
        return {
        "membershipId": payload.membershipId,
        "zipCode": payload.zipCode,
        "benefitProductType": payload.benefitProductType,
        "languageCode": payload.languageCode,
        "service": {
            "code": payload.service.code,
            "type": payload.service.type,
            "description": payload.service.description,
            "supportingService": payload.service.supportingService.code,
            "modifier": payload.service.modifier.modifierCode,
            "diagnosisCode": payload.service.diagnosisCode,
            "placeOfService": payload.service.placeOfService.code
        },
        "outOfPocketCost": 100.0  # Placeholder for actual calculation
    }

    except Exception as exec:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing request: {str(exec)}"
        )
