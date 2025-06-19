from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login_usuario, name='login'),         # raíz
    path('login/', views.login_usuario, name='login'),   # login directo
    path('registro/', views.registro, name='registro'),
    path('bienvenida/', views.bienvenida, name='bienvenida'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('api/registro/', views.RegistroAPI.as_view(), name='api_registro'),
    path('api/login/', views.LoginAPI.as_view(), name='api_login'),
    path('api/bienvenida/', views.BienvenidaAPI.as_view(), name='api_bienvenida'),
]