from uuid import UUID
from datetime import date

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from hotels_api.infrastructure.persistence.repositories.reservation_repository_impl import DjangoReservationRepository
from hotels_api.infrastructure.persistence.repositories.room_repository_impl import DjangoRoomRepository
from hotels_api.infrastructure.persistence.repositories.customer_repository_impl import DjangoCustomerRepository
from hotels_api.infrastructure.services.notification import LoggingNotificationService
from hotels_api.application.use_cases.reservations import (
    CreateReservationUseCase, GetReservationsUseCase,
    ApproveReservationUseCase, RejectReservationUseCase
)
from hotels_api.application.dto.reservation_dto import CreateReservationDTO, ReservationFiltersDTO
from hotels_api.application.dto.common import PaginationRequestDTO
from hotels_api.infrastructure.api.serializers.reservation_serializers import CreateReservationSerializer


class ReservationsView(APIView):
    def get(self, request):
        qp = request.query_params
        page = int(qp.get("page", 1))
        size = int(qp.get("size", 20))
        status_filter = qp.get("status")
        date_from = qp.get("date_from")
        date_to = qp.get("date_to")
        date_from_val = date.fromisoformat(date_from) if date_from else None
        date_to_val = date.fromisoformat(date_to) if date_to else None

        filters = ReservationFiltersDTO(status=status_filter, date_from=date_from_val, date_to=date_to_val)
        pagination = PaginationRequestDTO(page=page, size=size)

        use_case = GetReservationsUseCase(DjangoReservationRepository())
        result = use_case.execute(filters, pagination)
        data = {
            "items": [
                {
                    "id": str(r.id),
                    "customer_id": str(r.customer_id),
                    "room_id": str(r.room_id),
                    "start_date": r.start_date.isoformat(),
                    "end_date": r.end_date.isoformat(),
                    "status": r.status,
                }
                for r in result.items
            ],
            "total": result.total,
            "page": result.page,
            "size": result.size,
        }
        return Response(data)

    def post(self, request):
        serializer = CreateReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data
        dto = CreateReservationDTO(
            customer_name=payload["customer_name"],
            customer_email=payload["customer_email"],
            customer_phone=payload["customer_phone"],
            room_id=payload["room_id"],
            start_date=payload["start_date"],
            end_date=payload["end_date"],
        )
        use_case = CreateReservationUseCase(
            reservation_repository=DjangoReservationRepository(),
            room_repository=DjangoRoomRepository(),
            customer_repository=DjangoCustomerRepository(),
        )
        reservation = use_case.execute(dto)
        return Response(
            {
                "id": str(reservation.id),
                "customer_id": str(reservation.customer_id),
                "room_id": str(reservation.room_id),
                "start_date": reservation.start_date.isoformat(),
                "end_date": reservation.end_date.isoformat(),
                "status": reservation.status,
            },
            status=status.HTTP_201_CREATED,
        )


class ApproveReservationView(APIView):
    def post(self, request, id: UUID):
        use_case = ApproveReservationUseCase(
            reservation_repository=DjangoReservationRepository(),
            customer_repository=DjangoCustomerRepository(),
            notification_service=LoggingNotificationService(),
        )
        reservation = use_case.execute(id)
        return Response(
            {
                "id": str(reservation.id),
                "customer_id": str(reservation.customer_id),
                "room_id": str(reservation.room_id),
                "start_date": reservation.start_date.isoformat(),
                "end_date": reservation.end_date.isoformat(),
                "status": reservation.status,
            }
        )


class RejectReservationView(APIView):
    def post(self, request, id: UUID):
        use_case = RejectReservationUseCase(
            reservation_repository=DjangoReservationRepository(),
            customer_repository=DjangoCustomerRepository(),
            notification_service=LoggingNotificationService(),
        )
        reservation = use_case.execute(id)
        return Response(
            {
                "id": str(reservation.id),
                "customer_id": str(reservation.customer_id),
                "room_id": str(reservation.room_id),
                "start_date": reservation.start_date.isoformat(),
                "end_date": reservation.end_date.isoformat(),
                "status": reservation.status,
            }
        )
