from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import viewPonentes

router = DefaultRouter()
router.register(r'ponentes', viewPonentes)

urlpatterns = [
    path('', include(router.urls)),
]