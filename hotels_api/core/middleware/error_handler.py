import logging
from typing import Any
from django.http import JsonResponse
from hotels_api.core.exceptions.application_exceptions import (
    ApplicationException,
    NotFoundException,
    ConflictException,
    ValidationException,
)
from hotels_api.core.exceptions.domain_exceptions import (
    DomainException,
    DomainValidationError,
    BusinessRuleViolationException,
)

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware:
    """
    Middleware global que convierte excepciones de Dominio y Aplicación
    en respuestas HTTP JSON consistentes, con formato:
    {
      "error": { "code": "CODE", "message": "..." }
    }

    - Dominio/Aplicación Validation -> 400
    - NotFound -> 404
    - Conflict / BusinessRuleViolation -> 409
    - Otros errores -> 500
    """

    def __init__(self, get_response: Any):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except NotFoundException as ex:
            return self._json_error(ex.code, ex.message, status=404)
        except (ValidationException, DomainValidationError) as ex:
            code = getattr(ex, "code", "VALIDATION_ERROR")
            return self._json_error(code, str(ex), status=400)
        except (ConflictException, BusinessRuleViolationException) as ex:
            code = getattr(ex, "code", "CONFLICT")
            return self._json_error(code, str(ex), status=409)
        except (ApplicationException, DomainException) as ex:
            code = getattr(ex, "code", "ERROR")
            return self._json_error(code, str(ex), status=400)
        except Exception as ex:
            logger.exception("Unhandled exception")
            return self._json_error("INTERNAL_SERVER_ERROR", "Unexpected server error." , status=500)

    @staticmethod
    def _json_error(code: str, message: str, status: int) -> JsonResponse:
        return JsonResponse({"error": {"code": code, "message": message}}, status=status)
