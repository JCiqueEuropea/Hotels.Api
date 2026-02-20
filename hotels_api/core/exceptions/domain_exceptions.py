class DomainException(Exception):
    """Base class for domain exceptions"""
    def __init__(self, message: str, code: str = "DOMAIN_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class DomainValidationError(DomainException):
    def __init__(self, message: str):
        super().__init__(message, code="VALIDATION_ERROR")

class BusinessRuleViolationException(DomainException):
    def __init__(self, message: str, code: str = "BUSINESS_RULE_VIOLATION"):
        super().__init__(message, code)
