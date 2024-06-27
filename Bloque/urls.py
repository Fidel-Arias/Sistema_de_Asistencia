from rest_framework.routers import DefaultRouter
from .views import viewBloques
from django.urls import path, include

router = DefaultRouter()
router.register(r'bloques', viewBloques)

urlpatterns = [
    path('', include(router.urls)),
]
