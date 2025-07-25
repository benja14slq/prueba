from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login_usuario, name='login'),         # raíz
    path('login/', views.login_usuario, name='login'),   # login directo
    path('registro/', views.registro, name='registro'),
    path('bienvenida/', views.bienvenida, name='bienvenida'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('api/registro/', views.RegistroAPI.as_view(), name='api_registro'),
    path('api/login/', views.LoginAPI.as_view(), name='api_login'),
    path('api/bienvenida/', views.BienvenidaAPI.as_view(), name='api_bienvenida'),
    path('api/roles/', views.listar_roles),
    path('api/plant-data/', views.get_plant_data, name='plant-data'),
    path('dashboard/', views.dashboard_view, name='dashboard')
]