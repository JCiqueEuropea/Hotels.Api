from django.urls import path

from hotels_api.infrastructure.api.controllers.rooms_controller import RoomsView, RoomDetailView
from hotels_api.infrastructure.api.controllers.event_rooms_controller import EventRoomsView, EventRoomDetailView
from hotels_api.infrastructure.api.controllers.reservations_controller import (
    ReservationsView, ApproveReservationView, RejectReservationView
)
from hotels_api.infrastructure.api.controllers.statistics_controller import OccupancyStatisticsView

urlpatterns = [
    # Rooms
    path("rooms", RoomsView.as_view()),
    path("rooms/<uuid:id>", RoomDetailView.as_view()),

    # Event Rooms
    path("event-rooms", EventRoomsView.as_view()),
    path("event-rooms/<uuid:id>", EventRoomDetailView.as_view()),

    # Reservations
    path("reservations", ReservationsView.as_view()),
    path("reservations/<uuid:id>/approve", ApproveReservationView.as_view()),
    path("reservations/<uuid:id>/reject", RejectReservationView.as_view()),

    # Statistics
    path("stats/occupancy", OccupancyStatisticsView.as_view()),
]
