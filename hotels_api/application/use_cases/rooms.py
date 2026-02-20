from dataclasses import dataclass
from typing import List
from uuid import UUID
from decimal import Decimal

from hotels_api.domain.entities.room import Room, RoomType
from hotels_api.domain.repositories.room_repository import RoomRepository
from hotels_api.domain.value_objects.common import Money
from hotels_api.application.dto.room_dto import (
    CreateRoomDTO, UpdateRoomDTO, RoomDTO, RoomListDTO, RoomFiltersDTO
)
from hotels_api.application.dto.common import PaginationRequestDTO, PaginationResultDTO
from hotels_api.core.exceptions.application_exceptions import NotFoundException, ValidationException


def _room_to_dto(room: Room) -> RoomDTO:
    return RoomDTO(
        id=room.id,
        hotel_id=room.hotel_id,
        number=room.number,
        room_type=room.room_type.name,
        price_amount=room.price.amount,
        price_currency=room.price.currency,
        is_active=room.is_active,
    )


class CreateRoomUseCase:
    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository

    def execute(self, dto: CreateRoomDTO) -> RoomDTO:
        try:
            room_type = RoomType[dto.room_type.upper()]
        except KeyError:
            raise ValidationException(f"Invalid room type: {dto.room_type}", code="ROOM_TYPE_INVALID")
        money = Money(amount=dto.price_amount, currency=dto.price_currency)
        room = Room.create(hotel_id=dto.hotel_id, number=dto.number, room_type=room_type, price=money)
        self.room_repository.save(room)
        return _room_to_dto(room)


class UpdateRoomUseCase:
    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository

    def execute(self, dto: UpdateRoomDTO) -> RoomDTO:
        room = self.room_repository.get_by_id(dto.id)
        if not room:
            raise NotFoundException(f"Room {dto.id} not found", code="ROOM_NOT_FOUND")

        if dto.number is not None:
            room.number = dto.number
        if dto.room_type is not None:
            try:
                room.room_type = RoomType[dto.room_type.upper()]
            except KeyError:
                raise ValidationException(f"Invalid room type: {dto.room_type}", code="ROOM_TYPE_INVALID")
        if dto.price_amount is not None:
            currency = dto.price_currency or room.price.currency
            room.price = Money(amount=dto.price_amount, currency=currency)
        if dto.is_active is not None:
            if dto.is_active:
                room.activate()
            else:
                room.deactivate()

        self.room_repository.save(room)
        return _room_to_dto(room)


class DeleteRoomUseCase:
    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository

    def execute(self, room_id: UUID) -> None:
        # Implementación de borrado lógico a nivel de repositorio
        self.room_repository.delete(room_id)


class GetRoomsUseCase:
    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository

    def execute(self, filters: RoomFiltersDTO, pagination: PaginationRequestDTO) -> RoomListDTO:
        # Convertimos filtros DTO a dict para repositorio
        repo_filters = {}
        if filters.hotel_id is not None:
            repo_filters["hotel_id"] = str(filters.hotel_id)
        if filters.room_type is not None:
            repo_filters["room_type"] = filters.room_type.upper()
        if filters.is_active is not None:
            repo_filters["is_active"] = filters.is_active
        if filters.min_price is not None:
            repo_filters["min_price"] = Decimal(filters.min_price)
        if filters.max_price is not None:
            repo_filters["max_price"] = Decimal(filters.max_price)

        rooms: List[Room] = self.room_repository.get_all(filters=repo_filters)
        total = len(rooms)
        start = (pagination.page - 1) * pagination.size
        end = start + pagination.size
        items = rooms[start:end]
        return RoomListDTO(
            items=[_room_to_dto(r) for r in items],
            total=total,
            page=pagination.page,
            size=pagination.size,
        )
