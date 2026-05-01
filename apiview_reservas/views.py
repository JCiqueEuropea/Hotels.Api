from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import ReservaHabitacion
import json
from view_set_habs.models import Habitacion
from viewset_users.models import User

# Create your views here.
@csrf_exempt
@require_http_methods(["GET"])
def listar_reservas(request):
    reservas = ReservaHabitacion.objects.all()
    reservas_data = [reserva.to_dict() for reserva in reservas]
    return JsonResponse(reservas_data, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def crear_reserva(request):
    data = json.loads(request.body)
    if not data.get('fecha_inicio') or not data.get('fecha_fin') or not data.get('habitacion') or not data.get('usuario'):
        return JsonResponse({'error': 'Faltan campos requeridos'}, status=400)
    if not Habitacion.objects.filter(id=data['habitacion']).exists():
        return JsonResponse({'error': 'Habitación no encontrada'}, status=404)
    if not User.objects.filter(id=data['usuario']).exists():
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
    if data['fecha_inicio'] >= data['fecha_fin']:
        return JsonResponse({'error': 'La fecha de inicio debe ser anterior a la fecha de fin'}, status=400)
    if ReservaHabitacion.objects.filter(habitacion_id=data['habitacion'], fecha_inicio__lt=data['fecha_fin'], fecha_fin__gt=data['fecha_inicio']).exists():
        return JsonResponse({'error': 'La habitación ya está reservada para las fechas seleccionadas'}, status=400)
    
    if Habitacion.objects.get(id=data['habitacion']).numero_disponibles <= 0:
        
        return JsonResponse({'error': 'No hay habitaciones disponibles'}, status=400)
    reserva = ReservaHabitacion.objects.create(
        fecha_inicio=data['fecha_inicio'],
        fecha_fin=data['fecha_fin'],
        habitacion_id=data['habitacion'],
        usuario_id=data['usuario']
    )
    return JsonResponse(reserva.to_dict(), status=201)

@csrf_exempt
@require_http_methods(["GET"])
def obtener_reserva(request, reserva_id):
    try:
        reserva = ReservaHabitacion.objects.get(id=reserva_id)
    except ReservaHabitacion.DoesNotExist:
        return JsonResponse({'error': 'Reserva no encontrada'}, status=404)
    return JsonResponse(reserva.to_dict(), status=200)

@csrf_exempt
@require_http_methods(["PUT"])
def actualizar_reserva(request, reserva_id):
    try:
        reserva = ReservaHabitacion.objects.get(id=reserva_id)
    except ReservaHabitacion.DoesNotExist:
        return JsonResponse({'error': 'Reserva no encontrada'}, status=404)
    
    data = json.loads(request.body)
    if not data.get('fecha_inicio') or not data.get('fecha_fin') or not data.get('habitacion') or not data.get('usuario'):
        return JsonResponse({'error': 'Faltan campos requeridos'}, status=400)
    if not Habitacion.objects.filter(id=data['habitacion']).exists():
        return JsonResponse({'error': 'Habitación no encontrada'}, status=404)
    if not User.objects.filter(id=data['usuario']).exists():
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
    if data['fecha_inicio'] >= data['fecha_fin']:
        return JsonResponse({'error': 'La fecha de inicio debe ser anterior a la fecha de fin'}, status=400)
    if ReservaHabitacion.objects.filter(habitacion_id=data['habitacion'], fecha_inicio__lt=data['fecha_fin'], fecha_fin__gt=data['fecha_inicio']).exclude(id=reserva_id).exists():
        return JsonResponse({'error': 'La habitación ya está reservada para las fechas seleccionadas'}, status=400)
    
    reserva.fecha_inicio = data['fecha_inicio']
    reserva.fecha_fin = data['fecha_fin']
    reserva.habitacion_id = data['habitacion']
    reserva.usuario_id = data['usuario']
    reserva.save()
    
    return JsonResponse(reserva.to_dict(), status=200)

@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_reserva(request, reserva_id):
    try:
        reserva = ReservaHabitacion.objects.get(id=reserva_id)
    except ReservaHabitacion.DoesNotExist:
        return JsonResponse({'error': 'Reserva no encontrada'}, status=404)
    
    reserva.delete()
    return JsonResponse({'message': 'Reserva eliminada exitosamente'}, status=200)

@csrf_exempt
@require_http_methods(["POST"])
def confirmar_reserva(request, reserva_id):
    try:
        reserva = ReservaHabitacion.objects.get(id=reserva_id)
    except ReservaHabitacion.DoesNotExist:
        return JsonResponse({'error': 'Reserva no encontrada'}, status=404)
    
    if reserva.confirmed:
        return JsonResponse({'error': 'La reserva ya está confirmada'}, status=400)
    
    reserva.confirmed = True
    reserva.save()
    
    return JsonResponse(reserva.to_dict(), status=200)