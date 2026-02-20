from typing import List, Optional
from uuid import UUID

from hotels_api.domain.entities.room import EventRoom
from hotels_api.domain.repositories.event_room_repository import EventRoomRepository
from hotels_api.infrastructure.persistence.mappers import event_room_mapper
from hotels_api.infrastructure.persistence.models.event_room import EventRoomModel


class DjangoEventRoomRepository(EventRoomRepository):
    def save(self, event_room: EventRoom) -> None:
        obj = event_room_mapper.to_model(event_room)
        obj.save()

    def get_by_id(self, event_room_id: UUID) -> Optional[EventRoom]:
        try:
            model = EventRoomModel.objects.get(id=event_room_id)
            return event_room_mapper.to_entity(model)
        except EventRoomModel.DoesNotExist:
            return None

    def get_all(self, hotel_id: Optional[UUID] = None) -> List[EventRoom]:
        qs = EventRoomModel.objects.all()
        if hotel_id:
            qs = qs.filter(hotel_id=hotel_id)
        return [event_room_mapper.to_entity(m) for m in qs.order_by("name").all()]
