from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
@csrf_exempt
@require_http_methods(["GET"])
def has_admin_privileges(request):
    user = request.user
    print("Checking admin privileges for user:", user)
    if user.is_authenticated and user.is_hotel_manager:
        print("User is authenticated. Is hotel manager:", user.is_hotel_manager)
        return JsonResponse({'is_admin': True}, status=200)
    else:
        print("User is not authenticated or does not have 'is_hotel_manager' attribute.")
        return JsonResponse({'is_admin': False}, status=401)