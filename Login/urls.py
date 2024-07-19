from django.urls import path
from .views import LoginView

urlpatterns = [
    path('', LoginView.as_view({'get': 'login_user'}), name='Login'),
    path('loginColaborador/', LoginView.as_view({'get':'login_colaborador'}), name='LoguingColaborador'),
    path('loginAdmin/', LoginView.as_view({'get':'login_admin'}), name='LoguingAdministrador'),
]