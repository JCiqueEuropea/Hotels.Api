from dataclasses import dataclass
from uuid import UUID, uuid4
from hotels_api.domain.value_objects.common import DateRange
from hotels_api.domain.value_objects.reservation_status import ReservationStatus
from hotels_api.core.exceptions.domain_exceptions import BusinessRuleViolationException

@dataclass
class Reservation:
    id: UUID
    customer_id: UUID
    room_id: UUID
    date_range: DateRange
    status: ReservationStatus

    @classmethod
    def create(cls, customer_id: UUID, room_id: UUID, date_range: DateRange) -> 'Reservation':
        return cls(
            id=uuid4(),
            customer_id=customer_id,
            room_id=room_id,
            date_range=date_range,
            status=ReservationStatus.PENDING
        )

    def approve(self):
        if self.status == ReservationStatus.REJECTED:
            raise BusinessRuleViolationException("Reservation cannot be approved because it is rejected.")
        self.status = ReservationStatus.APPROVED

    def reject(self):
        self.status = ReservationStatus.REJECTED
