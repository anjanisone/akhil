from fastapi import APIRouter, status, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
from app.utils.CostShareCalculator import HealthInsurancePlan
from app.schemas.cost_estimation_input import CostEstimationInput  # ✅ your external model

router = APIRouter()

@router.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    formatted_errors = []
    for error in exc.errors():
        field_path = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        message = error["msg"]
        formatted_errors.append({
            "field": field_path,
            "message": message
        })

    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"errors": formatted_errors}
    )


@router.post("/estimate", status_code=status.HTTP_200_OK)
def estimate_out_of_pocket(payload: CostEstimationInput):
    try:
        plan = HealthInsurancePlan(
            copay=payload.copay,
            coinsurance_rate=payload.coinsurance_rate,
            copay_applies_oopmax=payload.copay_applies_oopmax,
            coins_applies_oopmax=payload.coins_applies_oopmax,
            deductible_applies_oopmax=payload.deductible_applies_oopmax,
            copay_continue_deductible_met=payload.copay_continue_deductible_met,
            copay_continue_oopmax_met=payload.copay_continue_oopmax_met,
            copay_count_to_deductible=payload.copay_count_to_deductible,
            is_deductible_before_copay=payload.is_deductible_before_copay,
            d_calculated=payload.d_calculated,
            oopmax_calculated=payload.oopmax_calculated
        )

        cost = plan.calculate_patient_pay(
            payload.service_cost,
            payload.is_service_covered,
            payload.benefit_limitation,
            payload.deductible_code_exists,
            payload.cost_share_copay,
            payload.cost_share_coinsurance,
            payload.oopmax_i_calculated,
            payload.oopmax_f_calculated,
            payload.di_calculated,
            payload.df_calculated,
            payload.limit_calculated_value,
            payload.limit_type
        )

        return JSONResponse(content={"out_of_pocket_cost": cost})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
