from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import (
    HTTPException,
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
    MethodNotAllowedException,
    InternalServerErrorException,
    ServiceUnavailableException,
    BadRequestException
)
from starlette.status import HTTP_400_BAD_REQUEST
from uuid import uuid4
from app.core.exception_responses import responses


async def bad_request_error_handler(request: Request, exc: BadRequestException):
    return JSONResponse(content=responses[400], status_code=400)

async def unauthorized_error_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(content=responses[401], status_code=401)

async def forbidden_error_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(content=responses[403], status_code=403)

async def not_found_error_handler(request: Request, exc: NotFoundException):
    return JSONResponse(content=responses[404], status_code=404)

async def method_not_allowed_error_handler(request: Request, exc: MethodNotAllowedException):
    return JSONResponse(content=responses[405], status_code=405)

async def internal_server_error_handler(request: Request, exc: InternalServerErrorException):
    return JSONResponse(content=responses[500], status_code=500)

async def service_unavailable_error_handler(request: Request, exc: ServiceUnavailableException):
    return JSONResponse(content=responses[503], status_code=503)

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
            "errors": str(error_dict).replace("'", '"'),
            "message": "Additional details",
            "requestBody": body
        }
    )


def include_exceptions(app: FastAPI):
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(BadRequestException, bad_request_error_handler)
    app.add_exception_handler(UnauthorizedException, unauthorized_error_handler)
    app.add_exception_handler(ForbiddenException, forbidden_error_handler)
    app.add_exception_handler(NotFoundException, not_found_error_handler)
    app.add_exception_handler(MethodNotAllowedException, method_not_allowed_error_handler)
    app.add_exception_handler(ServiceUnavailableException, service_unavailable_error_handler)
    app.add_exception_handler(Exception, internal_server_error_handler)

    return app
