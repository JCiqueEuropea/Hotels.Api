from django.urls import path
from .views import listar_reservas, crear_reserva, obtener_reserva, actualizar_reserva, eliminar_reserva, confirmar_reserva, cancelar_reserva

urlpatterns = [
    path('reservas/sala/', listar_reservas, name='listar_reservas'),
    path('reservas/sala/create/', crear_reserva, name='crear_reserva'),
    path('reservas/sala/<int:reserva_id>/', obtener_reserva, name='obtener_reserva'),
    path('reservas/sala/<int:reserva_id>/update/', actualizar_reserva, name='actualizar_reserva'),
    path('reservas/sala/<int:reserva_id>/delete/', eliminar_reserva, name='eliminar_reserva'),
    path('reservas/sala/<int:reserva_id>/confirmar/', confirmar_reserva, name='confirmar_reserva'),
    path('reservas/sala/<int:reserva_id>/cancelar/', cancelar_reserva, name='cancelar_reserva'),
]