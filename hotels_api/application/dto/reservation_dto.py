from dataclasses import dataclass
from datetime import date
from typing import Optional, List
from uuid import UUID

@dataclass
class ReservationDTO:
    id: UUID
    customer_id: UUID
    room_id: UUID
    start_date: date
    end_date: date
    status: str

@dataclass
class CreateReservationDTO:
    customer_name: str
    customer_email: str
    customer_phone: str
    room_id: UUID
    start_date: date
    end_date: date

@dataclass
class ReservationFiltersDTO:
    status: Optional[str] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None

@dataclass
class ReservationListDTO:
    items: List[ReservationDTO]
    total: int
    page: int
    size: int

@dataclass
class OccupancyStatsDTO:
    year: int
    month: int
    rooms_total: int
    rooms_occupied: int
    occupancy_rate: float
