from typing import List, Optional
from uuid import UUID

from hotels_api.domain.entities.room import Room
from hotels_api.domain.repositories.room_repository import RoomRepository
from hotels_api.domain.value_objects.common import DateRange
from hotels_api.infrastructure.persistence.mappers import room_mapper
from hotels_api.infrastructure.persistence.models.room import RoomModel
from hotels_api.infrastructure.persistence.models.reservation import ReservationModel


class DjangoRoomRepository(RoomRepository):
    def save(self, room: Room) -> None:
        obj = room_mapper.to_model(room)
        obj.save()

    def get_by_id(self, room_id: UUID) -> Optional[Room]:
        try:
            model = RoomModel.objects.get(id=room_id)
            return room_mapper.to_entity(model)
        except RoomModel.DoesNotExist:
            return None

    def get_all(self, filters: dict = None) -> List[Room]:
        qs = RoomModel.objects.all()
        filters = filters or {}
        if "hotel_id" in filters:
            qs = qs.filter(hotel_id=filters["hotel_id"]) 
        if "room_type" in filters:
            qs = qs.filter(room_type=filters["room_type"])
        if "is_active" in filters:
            qs = qs.filter(is_active=filters["is_active"]) 
        else:
            qs = qs.filter(is_active=True)
        if "min_price" in filters:
            qs = qs.filter(price_amount__gte=filters["min_price"]) 
        if "max_price" in filters:
            qs = qs.filter(price_amount__lte=filters["max_price"]) 
        return [room_mapper.to_entity(m) for m in qs.order_by("number").all()]

    def delete(self, room_id: UUID) -> None:
        RoomModel.objects.filter(id=room_id).update(is_active=False)

    def is_available(self, room_id: UUID, date_range: DateRange) -> bool:
        overlapping = ReservationModel.objects.filter(
            room_id=room_id,
            start_date__lt=date_range.end_date,
            end_date__gt=date_range.start_date,
            status__in=["PENDING", "APPROVED"],
        ).exists()
        return not overlapping
