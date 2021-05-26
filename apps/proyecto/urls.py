from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.conf.urls.static import static

app_name = 'sistemaGerencialAgro'

urlpatterns = [
    path('', login_required(index)),
    path('sistemaGerencialAgro/index/', login_required(index), name = 'index'),

    
    # ESTA URL ES SOLO PARA QUE FUNCIONE EL EJEMPLO, LUEGO SE BORRARA
    path('istemaGerencialAgro/consultaEstudiante/', login_required(consultaEstudiante), name="consulta_estudiante"),
]
