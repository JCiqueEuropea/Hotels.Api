from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, List, Dict
from uuid import UUID

@dataclass
class EventRoomDTO:
    id: UUID
    hotel_id: UUID
    name: str
    capacity: int
    hourly_rate_amount: Decimal
    hourly_rate_currency: str
    schedule: Dict

@dataclass
class CreateEventRoomDTO:
    hotel_id: UUID
    name: str
    capacity: int
    hourly_rate_amount: Decimal
    hourly_rate_currency: str = "USD"

@dataclass
class UpdateEventRoomScheduleDTO:
    id: UUID
    schedule: Dict

@dataclass
class EventRoomListDTO:
    items: List[EventRoomDTO]
    total: int
    page: int
    size: int
