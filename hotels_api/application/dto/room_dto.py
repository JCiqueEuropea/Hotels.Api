from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, List
from uuid import UUID

@dataclass
class RoomDTO:
    id: UUID
    hotel_id: UUID
    number: str
    room_type: str
    price_amount: Decimal
    price_currency: str
    is_active: bool

@dataclass
class CreateRoomDTO:
    hotel_id: UUID
    number: str
    room_type: str
    price_amount: Decimal
    price_currency: str = "USD"

@dataclass
class UpdateRoomDTO:
    id: UUID
    number: Optional[str] = None
    room_type: Optional[str] = None
    price_amount: Optional[Decimal] = None
    price_currency: Optional[str] = None
    is_active: Optional[bool] = None

@dataclass
class RoomFiltersDTO:
    hotel_id: Optional[UUID] = None
    room_type: Optional[str] = None
    is_active: Optional[bool] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None

@dataclass
class RoomListDTO:
    items: List[RoomDTO]
    total: int
    page: int
    size: int
