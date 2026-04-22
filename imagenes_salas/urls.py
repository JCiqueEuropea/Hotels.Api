from .views import ImagenesSalaViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'imagenes_salas', ImagenesSalaViewSet, basename='imagenes_salas')

urlpatterns = router.urls