from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from hotels_api.domain.entities.room import EventRoom

class EventRoomRepository(ABC):
    @abstractmethod
    def save(self, event_room: EventRoom) -> None:
        pass

    @abstractmethod
    def get_by_id(self, event_room_id: UUID) -> Optional[EventRoom]:
        pass

    @abstractmethod
    def get_all(self, hotel_id: Optional[UUID] = None) -> List[EventRoom]:
        pass
