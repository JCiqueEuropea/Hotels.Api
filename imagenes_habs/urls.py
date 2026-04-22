from .views import ImagenHabitacionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'imagenes_habs', ImagenHabitacionViewSet, basename='imagenes_habs')
urlpatterns = router.urls