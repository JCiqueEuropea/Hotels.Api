from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from hotels_api.domain.entities.room import Room, RoomType
from hotels_api.domain.value_objects.common import DateRange

class RoomRepository(ABC):
    @abstractmethod
    def save(self, room: Room) -> None:
        pass

    @abstractmethod
    def get_by_id(self, room_id: UUID) -> Optional[Room]:
        pass

    @abstractmethod
    def get_all(self, filters: dict = None) -> List[Room]:
        pass

    @abstractmethod
    def delete(self, room_id: UUID) -> None:
        pass

    @abstractmethod
    def is_available(self, room_id: UUID, date_range: DateRange) -> bool:
        pass
