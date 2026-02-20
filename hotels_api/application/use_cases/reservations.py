from typing import List, Optional
from uuid import UUID

from hotels_api.domain.entities.reservation import Reservation
from hotels_api.domain.repositories.reservation_repository import ReservationRepository
from hotels_api.domain.repositories.room_repository import RoomRepository
from hotels_api.domain.repositories.customer_repository import CustomerRepository
from hotels_api.domain.services.interfaces import NotificationService
from hotels_api.domain.value_objects.common import DateRange
from hotels_api.domain.value_objects.reservation_status import ReservationStatus
from hotels_api.application.dto.reservation_dto import (
    CreateReservationDTO, ReservationDTO, ReservationListDTO, ReservationFiltersDTO
)
from hotels_api.application.dto.common import PaginationRequestDTO
from hotels_api.core.exceptions.application_exceptions import NotFoundException, ConflictException


def _reservation_to_dto(r: Reservation) -> ReservationDTO:
    return ReservationDTO(
        id=r.id,
        customer_id=r.customer_id,
        room_id=r.room_id,
        start_date=r.date_range.start_date,
        end_date=r.date_range.end_date,
        status=r.status.value,
    )


class CreateReservationUseCase:
    def __init__(self,
                 reservation_repository: ReservationRepository,
                 room_repository: RoomRepository,
                 customer_repository: CustomerRepository):
        self.reservation_repository = reservation_repository
        self.room_repository = room_repository
        self.customer_repository = customer_repository

    def execute(self, dto: CreateReservationDTO) -> ReservationDTO:
        date_range = DateRange(start_date=dto.start_date, end_date=dto.end_date)

        # Verificar disponibilidad de la habitación
        if not self.room_repository.is_available(dto.room_id, date_range):
            raise ConflictException("Room is not available for the selected dates", code="ROOM_NOT_AVAILABLE")

        # Obtener o crear cliente por email
        customer = self.customer_repository.get_by_email(dto.customer_email)
        if not customer:
            from hotels_api.domain.entities.hotel import Customer  # import local para evitar ciclos
            customer = Customer.create(name=dto.customer_name, email=dto.customer_email, phone=dto.customer_phone)
            self.customer_repository.save(customer)

        reservation = Reservation.create(customer_id=customer.id, room_id=dto.room_id, date_range=date_range)
        self.reservation_repository.save(reservation)
        return _reservation_to_dto(reservation)


class ApproveReservationUseCase:
    def __init__(self,
                 reservation_repository: ReservationRepository,
                 customer_repository: CustomerRepository,
                 notification_service: NotificationService):
        self.reservation_repository = reservation_repository
        self.customer_repository = customer_repository
        self.notification_service = notification_service

    def execute(self, reservation_id: UUID) -> ReservationDTO:
        reservation = self.reservation_repository.get_by_id(reservation_id)
        if not reservation:
            raise NotFoundException(f"Reservation {reservation_id} not found", code="RESERVATION_NOT_FOUND")
        reservation.approve()  # Puede lanzar excepción de dominio si es inválido
        self.reservation_repository.save(reservation)

        customer = self.customer_repository.get_by_id(reservation.customer_id)
        if customer:
            self.notification_service.notify_reservation_approved(reservation, customer)
        return _reservation_to_dto(reservation)


class RejectReservationUseCase:
    def __init__(self,
                 reservation_repository: ReservationRepository,
                 customer_repository: CustomerRepository,
                 notification_service: NotificationService):
        self.reservation_repository = reservation_repository
        self.customer_repository = customer_repository
        self.notification_service = notification_service

    def execute(self, reservation_id: UUID) -> ReservationDTO:
        reservation = self.reservation_repository.get_by_id(reservation_id)
        if not reservation:
            raise NotFoundException(f"Reservation {reservation_id} not found", code="RESERVATION_NOT_FOUND")
        reservation.reject()
        self.reservation_repository.save(reservation)

        customer = self.customer_repository.get_by_id(reservation.customer_id)
        if customer:
            self.notification_service.notify_reservation_rejected(reservation, customer)
        return _reservation_to_dto(reservation)


class GetReservationsUseCase:
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository

    def execute(self, filters: ReservationFiltersDTO, pagination: PaginationRequestDTO) -> ReservationListDTO:
        repo_filters = {}
        if filters.status:
            repo_filters["status"] = filters.status.upper()
        if filters.date_from:
            repo_filters["date_from"] = filters.date_from
        if filters.date_to:
            repo_filters["date_to"] = filters.date_to
        reservations: List[Reservation] = self.reservation_repository.get_all(filters=repo_filters)
        total = len(reservations)
        start = (pagination.page - 1) * pagination.size
        end = start + pagination.size
        items = reservations[start:end]
        return ReservationListDTO(
            items=[_reservation_to_dto(r) for r in items],
            total=total,
            page=pagination.page,
            size=pagination.size,
        )
