import unittest
from datetime import date
from uuid import uuid4, UUID
from typing import List, Optional

from hotels_api.application.use_cases.reservations import (
    CreateReservationUseCase, ApproveReservationUseCase
)
from hotels_api.application.use_cases.statistics import GetOccupancyStatisticsUseCase
from hotels_api.application.dto.reservation_dto import CreateReservationDTO, OccupancyStatsDTO
from hotels_api.core.exceptions.application_exceptions import ConflictException
from hotels_api.domain.repositories.room_repository import RoomRepository
from hotels_api.domain.repositories.reservation_repository import ReservationRepository
from hotels_api.domain.repositories.customer_repository import CustomerRepository
from hotels_api.domain.services.interfaces import NotificationService
from hotels_api.domain.entities.reservation import Reservation
from hotels_api.domain.entities.hotel import Customer
from hotels_api.domain.value_objects.common import DateRange


class FakeRoomRepository(RoomRepository):
    def __init__(self, availability: bool = True):
        self.availability = availability

    def save(self, room):
        pass

    def get_by_id(self, room_id: UUID):
        return None

    def get_all(self, filters: dict = None):
        return []

    def delete(self, room_id: UUID):
        pass

    def is_available(self, room_id: UUID, date_range: DateRange) -> bool:
        return self.availability


class FakeReservationRepository(ReservationRepository):
    def __init__(self):
        self.store = {}

    def save(self, reservation: Reservation) -> None:
        self.store[reservation.id] = reservation

    def get_by_id(self, reservation_id: UUID) -> Optional[Reservation]:
        return self.store.get(reservation_id)

    def get_all(self, filters: dict = None) -> List[Reservation]:
        return list(self.store.values())

    def get_by_room_and_date(self, room_id: UUID, date_range) -> List[Reservation]:
        return []

    def get_occupancy_stats(self, year: int, month: int) -> dict:
        return {"rooms_total": 0, "rooms_occupied": 0, "occupancy_rate": 0.0}


class FakeCustomerRepository(CustomerRepository):
    def __init__(self):
        self.by_id = {}
        self.by_email = {}

    def save(self, customer: Customer) -> None:
        self.by_id[customer.id] = customer
        self.by_email[customer.email.value] = customer

    def get_by_id(self, customer_id: UUID) -> Optional[Customer]:
        return self.by_id.get(customer_id)

    def get_by_email(self, email: str) -> Optional[Customer]:
        return self.by_email.get(email)


class FakeNotificationService(NotificationService):
    def __init__(self):
        self.approved_called = False
        self.rejected_called = False

    def notify_reservation_approved(self, reservation: Reservation, customer: Customer) -> None:
        self.approved_called = True

    def notify_reservation_rejected(self, reservation: Reservation, customer: Customer) -> None:
        self.rejected_called = True


class TestUseCases(unittest.TestCase):
    def test_create_reservation_conflict_if_not_available(self):
        reservation_repo = FakeReservationRepository()
        room_repo = FakeRoomRepository(availability=False)
        customer_repo = FakeCustomerRepository()
        uc = CreateReservationUseCase(reservation_repo, room_repo, customer_repo)
        dto = CreateReservationDTO(
            customer_name="John",
            customer_email="john@example.com",
            customer_phone="+123456789",
            room_id=uuid4(),
            start_date=date(2025, 1, 1),
            end_date=date(2025, 1, 2),
        )
        with self.assertRaises(ConflictException):
            uc.execute(dto)

    def test_approve_reservation_sends_notification(self):
        reservation_repo = FakeReservationRepository()
        customer_repo = FakeCustomerRepository()
        notif = FakeNotificationService()

        # Creamos un cliente y una reserva PENDING
        cust = Customer.create(name="Jane", email="jane@example.com", phone="+111111111")
        customer_repo.save(cust)
        res = Reservation.create(customer_id=cust.id, room_id=uuid4(), date_range=DateRange(date(2025,1,1), date(2025,1,2)))
        reservation_repo.save(res)

        uc = ApproveReservationUseCase(reservation_repository=reservation_repo, customer_repository=customer_repo, notification_service=notif)
        result = uc.execute(res.id)

        self.assertEqual(result.status, "APPROVED")
        self.assertTrue(notif.approved_called)

    def test_get_occupancy_statistics(self):
        reservation_repo = FakeReservationRepository()
        # Sobreescribimos el comportamiento del fake para este test específico
        reservation_repo.get_occupancy_stats = lambda year, month: {
            "rooms_total": 10,
            "rooms_occupied": 5,
            "occupancy_rate": 0.5
        }
        
        uc = GetOccupancyStatisticsUseCase(reservation_repo)
        result = uc.execute(2025, 1)
        
        self.assertEqual(result.rooms_total, 10)
        self.assertEqual(result.rooms_occupied, 5)
        self.assertEqual(result.occupancy_rate, 0.5)
        self.assertEqual(result.year, 2025)
        self.assertEqual(result.month, 1)


if __name__ == "__main__":
    unittest.main()
