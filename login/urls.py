from django.urls import path
from dj_rest_auth.views import LoginView, LogoutView
from .views import has_admin_privileges


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('check-admin/', has_admin_privileges, name='check_admin'),
]