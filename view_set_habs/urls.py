from rest_framework.routers import DefaultRouter
from .views import HabitacionViewSet

router = DefaultRouter()
router.register(r'habs', HabitacionViewSet, basename='habs')  

urlpatterns = router.urls