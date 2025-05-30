from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
from uuid import uuid4

from app.core.exceptions import BadRequestException


async def bad_request_error_handler(request: Request, exc: BadRequestException):
    return JSONResponse(status_code=400)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    try:
        body = await request.json()
    except:
        body = None

    correlation_id = request.headers.get("x-correlation-id") or str(uuid4())

    error_dict = {}
    for err in exc.errors():
        field_path = ".".join(str(loc) for loc in err["loc"])
        message = err["msg"]
        error_dict[field_path] = message

    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={
            "correlationId": correlation_id,
            "type": "https://www.rfc-editor.org/rfc/rfc7231#section-6.5.1",
            "title": "One or more validation errors occurred",
            "status": 400,
            "detail": "Malformed request",
            "errors": error_dict,
            "message": "Additional details",
            "requestBody": body
        }
    )


def include_exceptions(app: FastAPI):
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(BadRequestException, bad_request_error_handler)
    return app
