from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.conf.urls.static import static

app_name = 'sistemaGerencialAgro'

urlpatterns = [
    path('', index),
    path('sistemaGerencialAgro/index/', index, name = 'index'),

    
    # ESTA URL ES SOLO PARA QUE FUNCIONE EL EJEMPLO, LUEGO SE BORRARA
    path('istemaGerencialAgro/consultaEstudiante/', consultaEstudiante, name="consulta_estudiante"),
    path('sistemaGerencialAgro/porcentaje/', reportesEstudiantesPorcentajeCarrera.as_view(), name="buscar_porcentaje"),
    path('sistemaGerencialAgro/genero/', reportesEstudiantesPorGenero.as_view(), name="buscar_genero"),
    path('sistemaGerencialAgro/modalidad/', reportesEstudiantesPorModalidad.as_view(), name="buscar_modalidad"),
    path('export/excel', export_estudiantes_csv, name='export_csv'),
]
