from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
from fastapi import Request
from cost_estimator import router  # Import your router module


app = FastAPI()

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        loc = ".".join(str(l) for l in err["loc"] if l != "body")
        msg = err["msg"]
        if err["type"] == "value_error.jsondecode":
            errors.append({"field": "body", "message": "Invalid or empty JSON body"})
        else:
            errors.append({"field": loc, "message": msg})

    return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content={"errors": errors})


app.include_router(router, prefix="/cost-estimator", tags=["cost-estimator"])

@app.get("/")
def read_root():
    return {"Hello": "World"}