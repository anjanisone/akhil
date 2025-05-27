from fastapi import APIRouter, Request, Depends, Header, Cookie
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from uuid import uuid4
from typing import Optional, Dict
from starlette.status import HTTP_400_BAD_REQUEST
from cost_estimation_input import CostEstimatorRequest

router = APIRouter()


def get_headers(
    access_token: Optional[str] = Cookie(None),
    x_correlation_id: Optional[str] = Header(None),
    x_client_ref_id: Optional[str] = Header(None)
) -> Dict[str, Optional[str]]:
    return {
        "access_token": access_token,
        "x_correlation_id": x_correlation_id,
        "x_client_ref_id": x_client_ref_id
    }


@router.post("/membercost/v1/estimate/search/retrieve")
async def estimate_cost(
    payload: CostEstimatorRequest,
    request: Request,
    headers: dict = Depends(get_headers)
):
    try:
        body = await request.json()
        payload = CostEstimatorRequest.parse_obj(body)

        # Your success logic here
        return {"status": "success"}

    except ValidationError as e:
        # Get correlation ID or generate fallback
        correlation_id = headers.get("x_correlation_id") or str(uuid4())

        # Prepare error dict in required format
        error_dict = {
            ".".join(str(loc) for loc in err["loc"]): err["msg"]
            for err in e.errors()
        }

        # Return with stringified JSON for `errors`
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={
                "correlationId": correlation_id,
                "type": "https://www.rfc-editor.org/rfc/rfc7231#section-6.5.1",
                "title": "One or more validation errors occurred",
                "status": 400,
                "detail": "Malformed request",
                "errors": str(error_dict).replace("'", '"'),  # Match JSON string
                "message": "Additional details"
            }
        )

    except Exception:
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={
                "correlationId": headers.get("x_correlation_id") or str(uuid4()),
                "type": "https://www.rfc-editor.org/rfc/rfc7231#section-6.5.1",
                "title": "Invalid JSON body",
                "status": 400,
                "detail": "Could not parse request body as valid JSON",
                "errors": "{}",
                "message": "Please ensure the request body is well-formed JSON."
            }
        )