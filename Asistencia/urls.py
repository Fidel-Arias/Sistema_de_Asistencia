from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import viewAsistencias

router = DefaultRouter()
router.register(r'asistencias', viewAsistencias)

urlpatterns = [
    path('', include(router.urls)),
]