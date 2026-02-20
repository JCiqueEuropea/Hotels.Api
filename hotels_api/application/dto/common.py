from dataclasses import dataclass
from datetime import date
from typing import Optional, List

@dataclass
class PaginationRequestDTO:
    page: int = 1
    size: int = 20

@dataclass
class PaginationResultDTO:
    total: int
    page: int
    size: int

@dataclass
class DateRangeDTO:
    start_date: date
    end_date: date
