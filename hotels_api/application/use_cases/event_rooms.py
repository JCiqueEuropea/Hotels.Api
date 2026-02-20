from typing import List
from uuid import UUID
from decimal import Decimal

from hotels_api.domain.entities.room import EventRoom
from hotels_api.domain.repositories.event_room_repository import EventRoomRepository
from hotels_api.domain.value_objects.common import Money
from hotels_api.application.dto.event_room_dto import (
    CreateEventRoomDTO, UpdateEventRoomScheduleDTO, EventRoomDTO, EventRoomListDTO
)
from hotels_api.application.dto.common import PaginationRequestDTO
from hotels_api.core.exceptions.application_exceptions import NotFoundException


def _event_room_to_dto(er: EventRoom) -> EventRoomDTO:
    return EventRoomDTO(
        id=er.id,
        hotel_id=er.hotel_id,
        name=er.name,
        capacity=er.capacity,
        hourly_rate_amount=er.hourly_rate.amount,
        hourly_rate_currency=er.hourly_rate.currency,
        schedule=er.schedule or {},
    )


class CreateEventRoomUseCase:
    def __init__(self, event_room_repository: EventRoomRepository):
        self.event_room_repository = event_room_repository

    def execute(self, dto: CreateEventRoomDTO) -> EventRoomDTO:
        rate = Money(amount=dto.hourly_rate_amount, currency=dto.hourly_rate_currency)
        er = EventRoom.create(hotel_id=dto.hotel_id, name=dto.name, capacity=dto.capacity, hourly_rate=rate)
        self.event_room_repository.save(er)
        return _event_room_to_dto(er)


class ConfigureEventRoomScheduleUseCase:
    def __init__(self, event_room_repository: EventRoomRepository):
        self.event_room_repository = event_room_repository

    def execute(self, dto: UpdateEventRoomScheduleDTO) -> EventRoomDTO:
        er = self.event_room_repository.get_by_id(dto.id)
        if not er:
            raise NotFoundException(f"Event room {dto.id} not found", code="EVENT_ROOM_NOT_FOUND")
        er.configure_schedule(dto.schedule)
        self.event_room_repository.save(er)
        return _event_room_to_dto(er)


class GetEventRoomsUseCase:
    def __init__(self, event_room_repository: EventRoomRepository):
        self.event_room_repository = event_room_repository

    def execute(self, hotel_id: UUID | None, pagination: PaginationRequestDTO) -> EventRoomListDTO:
        event_rooms: List[EventRoom] = self.event_room_repository.get_all(hotel_id=hotel_id)
        total = len(event_rooms)
        start = (pagination.page - 1) * pagination.size
        end = start + pagination.size
        items = event_rooms[start:end]
        return EventRoomListDTO(
            items=[_event_room_to_dto(er) for er in items],
            total=total,
            page=pagination.page,
            size=pagination.size,
        )
