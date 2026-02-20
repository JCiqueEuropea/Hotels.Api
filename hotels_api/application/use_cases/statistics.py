from dataclasses import dataclass

from hotels_api.domain.repositories.reservation_repository import ReservationRepository
from hotels_api.application.dto.reservation_dto import OccupancyStatsDTO


class GetOccupancyStatisticsUseCase:
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository

    def execute(self, year: int, month: int) -> OccupancyStatsDTO:
        stats = self.reservation_repository.get_occupancy_stats(year=year, month=month)
        return OccupancyStatsDTO(
            year=year,
            month=month,
            rooms_total=stats.get("rooms_total", 0),
            rooms_occupied=stats.get("rooms_occupied", 0),
            occupancy_rate=stats.get("occupancy_rate", 0.0),
        )
