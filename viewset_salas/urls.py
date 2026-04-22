from .views import SalaViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'salas', SalaViewSet, basename='salas')
urlpatterns = router.urls