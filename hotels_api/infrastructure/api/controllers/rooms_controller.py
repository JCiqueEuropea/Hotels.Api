from uuid import UUID
from decimal import Decimal
from typing import Optional

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from hotels_api.infrastructure.persistence.repositories.room_repository_impl import DjangoRoomRepository
from hotels_api.application.use_cases.rooms import (
    CreateRoomUseCase, UpdateRoomUseCase, DeleteRoomUseCase, GetRoomsUseCase
)
from hotels_api.application.dto.room_dto import (
    CreateRoomDTO, UpdateRoomDTO, RoomFiltersDTO
)
from hotels_api.application.dto.common import PaginationRequestDTO
from hotels_api.infrastructure.api.serializers.room_serializers import (
    CreateRoomSerializer, UpdateRoomSerializer
)


class RoomsView(APIView):
    """Colección de Rooms: GET (lista), POST (crear)"""

    def get(self, request):
        qp = request.query_params
        page = int(qp.get("page", 1))
        size = int(qp.get("size", 20))
        hotel_id: Optional[UUID] = None
        if qp.get("hotel_id"):
            hotel_id = UUID(qp.get("hotel_id"))
        room_type = qp.get("room_type")
        is_active = qp.get("is_active")
        is_active_val = None if is_active is None else is_active.lower() == "true"
        min_price = qp.get("min_price")
        max_price = qp.get("max_price")

        filters = RoomFiltersDTO(
            hotel_id=hotel_id,
            room_type=room_type,
            is_active=is_active_val,
            min_price=Decimal(min_price) if min_price is not None else None,
            max_price=Decimal(max_price) if max_price is not None else None,
        )
        pagination = PaginationRequestDTO(page=page, size=size)

        use_case = GetRoomsUseCase(DjangoRoomRepository())
        result = use_case.execute(filters, pagination)
        data = {
            "items": [
                {
                    "id": str(r.id),
                    "hotel_id": str(r.hotel_id),
                    "number": r.number,
                    "room_type": r.room_type,
                    "price": {"amount": str(r.price_amount), "currency": r.price_currency},
                    "is_active": r.is_active,
                }
                for r in result.items
            ],
            "total": result.total,
            "page": result.page,
            "size": result.size,
        }
        return Response(data)

    def post(self, request):
        serializer = CreateRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data
        dto = CreateRoomDTO(
            hotel_id=payload["hotel_id"],
            number=payload["number"],
            room_type=payload["room_type"],
            price_amount=payload["price_amount"],
            price_currency=payload.get("price_currency", "USD"),
        )
        use_case = CreateRoomUseCase(DjangoRoomRepository())
        room = use_case.execute(dto)
        return Response(
            {
                "id": str(room.id),
                "hotel_id": str(room.hotel_id),
                "number": room.number,
                "room_type": room.room_type,
                "price": {"amount": str(room.price_amount), "currency": room.price_currency},
                "is_active": room.is_active,
            },
            status=status.HTTP_201_CREATED,
        )


class RoomDetailView(APIView):
    """Detalle de Room: PUT (actualizar), DELETE (borrado lógico)"""

    def put(self, request, id: UUID):
        serializer = UpdateRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data
        dto = UpdateRoomDTO(
            id=id,
            number=payload.get("number"),
            room_type=payload.get("room_type"),
            price_amount=payload.get("price_amount"),
            price_currency=payload.get("price_currency"),
            is_active=payload.get("is_active"),
        )
        use_case = UpdateRoomUseCase(DjangoRoomRepository())
        room = use_case.execute(dto)
        return Response(
            {
                "id": str(room.id),
                "hotel_id": str(room.hotel_id),
                "number": room.number,
                "room_type": room.room_type,
                "price": {"amount": str(room.price_amount), "currency": room.price_currency},
                "is_active": room.is_active,
            }
        )

    def delete(self, request, id: UUID):
        use_case = DeleteRoomUseCase(DjangoRoomRepository())
        use_case.execute(id)
        return Response(status=status.HTTP_204_NO_CONTENT)
