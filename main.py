from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
from fastapi import Request
from uuid import uuid4
from cost_estimator import router  # Import your router module


app = FastAPI()

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    try:
        body = await request.json()
    except:
        body = None

    correlation_id = request.headers.get("x-correlation-id") or str(uuid4())

    error_dict = {
        ".".join(str(loc) for loc in err["loc"]): err["msg"]
        for err in exc.errors()
    }

    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={
            "correlationId": correlation_id,
            "type": "https://www.rfc-editor.org/rfc/rfc7231#section-6.5.1",
            "title": "One or more validation errors occurred",
            "status": 400,
            "detail": "Malformed request",
            "errors": str(error_dict).replace("'", '"'),  # stringified JSON
            "message": "Additional details"
        }
    )


app.include_router(router, prefix="/cost-estimator", tags=["cost-estimator"])

@app.get("/")
def read_root():
    return {"Hello": "World"}