from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from apps.usuario.views import Login, logoutUsuario
from apps.usuario.views import ListadoUsuario, RegistrarUsuario, RegistrarUsuarioLogin, InicioListadoUsuario, EditarUsuario, EliminarUsuario


app_name='usuario'

urlpatterns=[
    #URL para el menu de inicio
    path('', Login.as_view()),
    path('usuario/index/',login_required(index), name='index'),

    path('accounts/login/',Login.as_view(), name='login'),
    path('logout/',login_required(logoutUsuario), name='logout'),
    
    path('inicio_usuarios/', login_required(InicioListadoUsuario.as_view()), name='inicio_usuarios'),   
    path('listado_usuarios/', login_required(ListadoUsuario.as_view()), name='listar_usuarios'),
    path('registrar_usuario/', login_required(RegistrarUsuario.as_view()), name='registrar_usuario'),
    path('registrar_usuario/login', RegistrarUsuarioLogin.as_view(), name='registrar_usuario_login'),
    path('actualizar_usuario/<int:pk>/',EditarUsuario.as_view(), name = 'actualizar_usuario'),
    path('eliminar_usuario/<int:pk>/',EliminarUsuario.as_view(), name='eliminar_usuario'),
    
]