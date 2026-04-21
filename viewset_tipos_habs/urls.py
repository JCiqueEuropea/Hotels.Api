from rest_framework.routers import DefaultRouter
from .views import TipoHabitacionViewSet

router = DefaultRouter()
router.register(r'tipo-hab', TipoHabitacionViewSet, basename='tipo-hab')

urlpatterns = router.urls