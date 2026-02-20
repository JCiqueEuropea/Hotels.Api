from django.urls import path, include

urlpatterns = [
    path("api/", include("hotels_api.infrastructure.api.urls.routes")),
]
