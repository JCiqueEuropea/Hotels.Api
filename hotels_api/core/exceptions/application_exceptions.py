class ApplicationException(Exception):
    """Base class for application-layer exceptions (use cases)."""
    def __init__(self, message: str, code: str = "APPLICATION_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class NotFoundException(ApplicationException):
    def __init__(self, message: str, code: str = "NOT_FOUND"):
        super().__init__(message, code)

class ConflictException(ApplicationException):
    def __init__(self, message: str, code: str = "CONFLICT"):
        super().__init__(message, code)

class ValidationException(ApplicationException):
    def __init__(self, message: str, code: str = "VALIDATION_ERROR"):
        super().__init__(message, code)
