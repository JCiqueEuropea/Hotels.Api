from datetime import date

from rest_framework.views import APIView
from rest_framework.response import Response

from hotels_api.infrastructure.persistence.repositories.reservation_repository_impl import DjangoReservationRepository
from hotels_api.application.use_cases.statistics import GetOccupancyStatisticsUseCase


class OccupancyStatisticsView(APIView):
    def get(self, request):
        qp = request.query_params
        year = int(qp.get("year")) if qp.get("year") else date.today().year
        month = int(qp.get("month")) if qp.get("month") else date.today().month
        use_case = GetOccupancyStatisticsUseCase(DjangoReservationRepository())
        stats = use_case.execute(year=year, month=month)
        return Response(
            {
                "year": stats.year,
                "month": stats.month,
                "rooms_total": stats.rooms_total,
                "rooms_occupied": stats.rooms_occupied,
                "occupancy_rate": stats.occupancy_rate,
            }
        )