from dataclasses import dataclass
from uuid import UUID, uuid4
from enum import Enum
from hotels_api.domain.value_objects.common import Money

class RoomType(Enum):
    SINGLE = "SINGLE"
    DOUBLE = "DOUBLE"
    SUITE = "SUITE"
    DELUXE = "DELUXE"

@dataclass
class Room:
    id: UUID
    hotel_id: UUID
    number: str
    room_type: RoomType
    price: Money
    is_active: bool = True

    @classmethod
    def create(cls, hotel_id: UUID, number: str, room_type: RoomType, price: Money) -> 'Room':
        return cls(
            id=uuid4(),
            hotel_id=hotel_id,
            number=number,
            room_type=room_type,
            price=price
        )

    def deactivate(self):
        self.is_active = False

    def activate(self):
        self.is_active = True

@dataclass
class EventRoom:
    id: UUID
    hotel_id: UUID
    name: str
    capacity: int
    hourly_rate: Money
    schedule: dict = None # Simularemos un horario simple

    @classmethod
    def create(cls, hotel_id: UUID, name: str, capacity: int, hourly_rate: Money) -> 'EventRoom':
        return cls(
            id=uuid4(),
            hotel_id=hotel_id,
            name=name,
            capacity=capacity,
            hourly_rate=hourly_rate,
            schedule={}
        )

    def configure_schedule(self, schedule_data: dict):
        # Lógica para configurar horario
        self.schedule = schedule_data
