from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
@csrf_exempt
@require_http_methods(["GET"])
def has_admin_privileges(request):
    user = request.user
    
    if user.is_authenticated and user.is_hotel_manager:
        return JsonResponse({'is_admin': True}, status=200)
    else:
        return JsonResponse({'is_admin': False}, status=401)
    
@csrf_exempt
@require_http_methods(["GET"])
def auth_me(request):
    user = request.user
    
    if user.is_authenticated:
        return JsonResponse({'username': user.username, 'email': user.email, 'id': user.id}, status=200)
    else:
        return JsonResponse({'error': 'No autenticado'}, status=401)