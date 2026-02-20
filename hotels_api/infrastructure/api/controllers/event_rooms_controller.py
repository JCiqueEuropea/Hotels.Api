from uuid import UUID

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from hotels_api.infrastructure.persistence.repositories.event_room_repository_impl import DjangoEventRoomRepository
from hotels_api.application.use_cases.event_rooms import (
    CreateEventRoomUseCase, ConfigureEventRoomScheduleUseCase, GetEventRoomsUseCase
)
from hotels_api.application.dto.event_room_dto import (
    CreateEventRoomDTO, UpdateEventRoomScheduleDTO
)
from hotels_api.application.dto.common import PaginationRequestDTO
from hotels_api.infrastructure.api.serializers.event_room_serializers import (
    CreateEventRoomSerializer, UpdateEventRoomScheduleSerializer
)


class EventRoomsView(APIView):
    def get(self, request):
        qp = request.query_params
        page = int(qp.get("page", 1))
        size = int(qp.get("size", 20))
        hotel_id = qp.get("hotel_id")
        hotel_uuid = UUID(hotel_id) if hotel_id else None
        use_case = GetEventRoomsUseCase(DjangoEventRoomRepository())
        result = use_case.execute(hotel_uuid, PaginationRequestDTO(page=page, size=size))
        data = {
            "items": [
                {
                    "id": str(er.id),
                    "hotel_id": str(er.hotel_id),
                    "name": er.name,
                    "capacity": er.capacity,
                    "hourly_rate": {"amount": str(er.hourly_rate_amount), "currency": er.hourly_rate_currency},
                    "schedule": er.schedule,
                }
                for er in result.items
            ],
            "total": result.total,
            "page": result.page,
            "size": result.size,
        }
        return Response(data)

    def post(self, request):
        serializer = CreateEventRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data
        dto = CreateEventRoomDTO(
            hotel_id=payload["hotel_id"],
            name=payload["name"],
            capacity=payload["capacity"],
            hourly_rate_amount=payload["hourly_rate_amount"],
            hourly_rate_currency=payload.get("hourly_rate_currency", "USD"),
        )
        use_case = CreateEventRoomUseCase(DjangoEventRoomRepository())
        er = use_case.execute(dto)
        return Response(
            {
                "id": str(er.id),
                "hotel_id": str(er.hotel_id),
                "name": er.name,
                "capacity": er.capacity,
                "hourly_rate": {"amount": str(er.hourly_rate_amount), "currency": er.hourly_rate_currency},
                "schedule": er.schedule,
            },
            status=status.HTTP_201_CREATED,
        )


class EventRoomDetailView(APIView):
    def put(self, request, id: UUID):
        serializer = UpdateEventRoomScheduleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = UpdateEventRoomScheduleDTO(id=id, schedule=serializer.validated_data["schedule"])
        use_case = ConfigureEventRoomScheduleUseCase(DjangoEventRoomRepository())
        er = use_case.execute(dto)
        return Response(
            {
                "id": str(er.id),
                "hotel_id": str(er.hotel_id),
                "name": er.name,
                "capacity": er.capacity,
                "hourly_rate": {"amount": str(er.hourly_rate_amount), "currency": er.hourly_rate_currency},
                "schedule": er.schedule,
            }
        )
