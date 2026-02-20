import unittest
from datetime import date
from decimal import Decimal
from uuid import uuid4

from hotels_api.core.exceptions.domain_exceptions import DomainValidationError, BusinessRuleViolationException
from hotels_api.domain.value_objects.common import Money, DateRange, Email
from hotels_api.domain.entities.reservation import Reservation


class TestDomainEntities(unittest.TestCase):
    def test_money_negative_raises(self):
        with self.assertRaises(DomainValidationError):
            Money(amount=Decimal("-1.00"), currency="USD")

    def test_date_range_invalid_raises(self):
        with self.assertRaises(DomainValidationError):
            DateRange(start_date=date(2025, 1, 10), end_date=date(2025, 1, 10))

    def test_date_range_overlaps(self):
        a = DateRange(start_date=date(2025, 1, 1), end_date=date(2025, 1, 10))
        b = DateRange(start_date=date(2025, 1, 5), end_date=date(2025, 1, 15))
        self.assertTrue(a.overlaps(b))

    def test_reservation_cannot_approve_if_rejected(self):
        r = Reservation.create(customer_id=uuid4(), room_id=uuid4(), date_range=DateRange(date(2025,1,1), date(2025,1,2)))
        r.reject()
        with self.assertRaises(BusinessRuleViolationException):
            r.approve()

    def test_invalid_email_raises(self):
        with self.assertRaises(DomainValidationError):
            Email("not-an-email")


if __name__ == "__main__":
    unittest.main()
