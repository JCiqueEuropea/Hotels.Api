from typing import List, Optional
from uuid import UUID
from datetime import date, datetime
from calendar import monthrange

from django.db.models import Q

from hotels_api.domain.entities.reservation import Reservation
from hotels_api.domain.repositories.reservation_repository import ReservationRepository
from hotels_api.infrastructure.persistence.mappers import reservation_mapper
from hotels_api.infrastructure.persistence.models.reservation import ReservationModel
from hotels_api.infrastructure.persistence.models.room import RoomModel


class DjangoReservationRepository(ReservationRepository):
    def save(self, reservation: Reservation) -> None:
        obj = reservation_mapper.to_model(reservation)
        obj.save()

    def get_by_id(self, reservation_id: UUID) -> Optional[Reservation]:
        try:
            model = ReservationModel.objects.get(id=reservation_id)
            return reservation_mapper.to_entity(model)
        except ReservationModel.DoesNotExist:
            return None

    def get_all(self, filters: dict = None) -> List[Reservation]:
        qs = ReservationModel.objects.all()
        filters = filters or {}
        if "status" in filters:
            qs = qs.filter(status=filters["status"]) 
        if "date_from" in filters:
            qs = qs.filter(start_date__gte=filters["date_from"]) 
        if "date_to" in filters:
            qs = qs.filter(end_date__lte=filters["date_to"]) 
        qs = qs.select_related("customer", "room").order_by("-start_date")
        return [reservation_mapper.to_entity(m) for m in qs]

    def get_by_room_and_date(self, room_id: UUID, date_range) -> List[Reservation]:
        qs = ReservationModel.objects.filter(
            room_id=room_id,
            start_date__lt=date_range.end_date,
            end_date__gt=date_range.start_date,
        )
        return [reservation_mapper.to_entity(m) for m in qs]

    def get_occupancy_stats(self, year: int, month: int) -> dict:
        day_count = monthrange(year, month)[1]
        month_start = date(year, month, 1)
        month_end = date(year, month, day_count)
        rooms_total = RoomModel.objects.filter(is_active=True).count()
        occupied_room_count = (
            ReservationModel.objects.filter(
                status="APPROVED",
                start_date__lt=month_end,
                end_date__gt=month_start,
            )
            .values_list("room_id", flat=True)
            .distinct()
            .count()
        )
        occupancy_rate = float(occupied_room_count / rooms_total) if rooms_total else 0.0
        return {
            "rooms_total": rooms_total,
            "rooms_occupied": occupied_room_count,
            "occupancy_rate": round(occupancy_rate, 4),
        }
