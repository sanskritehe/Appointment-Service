from pydantic import BaseModel

class ErrorResponseModel(BaseModel):
    detail: str
    error_code: str = "unknown_error"  # Default value for error_code.
    metadata: dict | None = None
