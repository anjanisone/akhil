from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.utils.CostShareCalculator import HealthInsurancePlan  # ✅ import from utils

router = APIRouter()

class CostEstimationInput(BaseModel):
    service_cost: float
    is_service_covered: bool
    benefit_limitation: float | None
    deductible_code_exists: bool
    cost_share_copay: float
    cost_share_coinsurance: float
    oopmax_i_calculated: float
    oopmax_f_calculated: float
    di_calculated: float
    df_calculated: float
    limit_calculated_value: float
    limit_type: str

    # Plan-level configuration
    copay: float
    coinsurance_rate: float
    copay_applies_oopmax: bool
    coins_applies_oopmax: bool
    deductible_applies_oopmax: bool
    copay_continue_deductible_met: bool
    copay_continue_oopmax_met: bool
    copay_count_to_deductible: bool
    is_deductible_before_copay: bool
    d_calculated: float
    oopmax_calculated: float


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