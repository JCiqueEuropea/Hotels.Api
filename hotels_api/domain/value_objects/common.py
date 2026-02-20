import re
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from hotels_api.core.exceptions.domain_exceptions import DomainValidationError

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.value):
            raise DomainValidationError(f"Invalid email address: {self.value}")

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "USD"

    def __post_init__(self):
        if self.amount < 0:
            raise DomainValidationError("Amount cannot be negative")

@dataclass(frozen=True)
class DateRange:
    start_date: date
    end_date: date

    def __post_init__(self):
        if self.start_date >= self.end_date:
            raise DomainValidationError("Start date must be before end date")

    def overlaps(self, other: 'DateRange') -> bool:
        return self.start_date < other.end_date and other.start_date < self.end_date

@dataclass(frozen=True)
class PhoneNumber:
    value: str

    def __post_init__(self):
        if not re.match(r"^\+?[1-9]\d{1,14}$", self.value):
            raise DomainValidationError(f"Invalid phone number: {self.value}")
