
from starlette.exceptions import HTTPException

class BadRequestException(HTTPException):
    """
    Raised when a request fails due to invalid input, malformed structure, or missing required fields.

    This exception triggers a 400 Bad Request response, which is handled by a centralized
    exception handler. The handler constructs a standardized response payload that includes:

    - `correlationId`: A unique request identifier (generated if not provided)
    - `type`: A reference URL to RFC 7231 section 6.5.1
    - `title`: A message indicating that validation errors occurred
    - `status`: 400
    - `detail`: A summary like "Malformed request"
    - `errors`: A dictionary with specific fields and their validation issues
    - `message`: A generic description
    - `requestBody`: Echo of the request payload, if available

    Usage Example:
    --------------
    ```python
    if not request_data.get("email"):
        raise BadRequestException("Missing required field: email")
    ```
    """
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(status_code=400, detail=detail)
