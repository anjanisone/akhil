responses = {
    400: {
        "description": "Bad Request",
        "headers": {
            "x-correlation-id": {
                "$ref": "https://apiforge.cvshealth.com/api-oas/global-domains/"
                        "cvs-enterprise-domains-v1-1.0.0.yaml#/components/headers/x-correlationid"
            },
            "x-clientrefid": {
                "$ref": "https://apiforge.cvshealth.com/api-oas/global-domains/"
                        "cvs-enterprise-domains-v1-1.0.0.yaml#/components/headers/x-clientrefid"
            }
        },
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "https://apiforge.cvshealth.com/api-oas/global-domains/"
                            "cvs-enterprise-domains-v1-1.0.0.yaml#/components/schemas/error"
                },
                "examples": {
                    "INVALID_INPUTS": {
                        "value": {
                            "correlationId": "06d9197a-1e14-453f-8cf4-637f4eb626ff",
                            "errors": {
                                "body.name": "field required",
                                "body.age": "value is not a valid integer"
                            },
                            "type": "https://www.rfc-editor.org/rfc/rfc7231#section-6.5.1",
                            "title": "One or more validation errors occurred",
                            "status": 400,
                            "detail": "Malformed request",
                            "message": "Additional details"
                        }
                    }
                }
            }
        }
    }
}
