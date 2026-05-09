from django.urls import path
from dj_rest_auth.views import LoginView, LogoutView
from .views import has_admin_privileges, auth_me


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('auth-me/', auth_me, name='auth_me'),
    path('check-admin/', has_admin_privileges, name='check_admin'),
]