from django.urls import path
from .views import login, loginColaborador, loginAdmin, user_logged_in, admin_logged_in

urlpatterns = [
    path('', login, name='Login'),
    path('platformUser/<str:pk>', user_logged_in, name="Logueado"),
    path('platformAdmin/', admin_logged_in, name="LogueadoAdmin"),
    path('loginColaborador/', loginColaborador, name='LoguingColaborador'),
    path('loginAdmin/', loginAdmin, name='LoguingAdministrador'),
]