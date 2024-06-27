from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UniversidadViewSet

router = DefaultRouter()
router.register('universidad', UniversidadViewSet)

urlpatterns = [
    path('', include(router.urls)),
]