from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from hotels_api.domain.entities.reservation import Reservation
from hotels_api.domain.value_objects.reservation_status import ReservationStatus

class ReservationRepository(ABC):
    @abstractmethod
    def save(self, reservation: Reservation) -> None:
        pass

    @abstractmethod
    def get_by_id(self, reservation_id: UUID) -> Optional[Reservation]:
        pass

    @abstractmethod
    def get_all(self, filters: dict = None) -> List[Reservation]:
        pass

    @abstractmethod
    def get_by_room_and_date(self, room_id: UUID, date_range) -> List[Reservation]:
        pass

    @abstractmethod
    def get_occupancy_stats(self, year: int, month: int) -> dict:
        pass
