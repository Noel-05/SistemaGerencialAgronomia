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
    path('sistemaGerencialAgro/porcentaje/', consultaEstudiantesPorcentajeCarrera.as_view(), name="buscar_porcentaje"),
    path('sistemaGerencialAgro/genero/', consultaEstudiantesPorGenero.as_view(), name="buscar_genero"),
    path('sistemaGerencialAgro/modalidad/', consultaEstudiantesPorModalidad.as_view(), name="buscar_modalidad"),
    path('export/excel', export_estudiantes_csv, name='export_csv'),
    path('reporte/porcentaje', reporteEstudiantePorcentajeCarrera.as_view(), name="reporte_porcentaje"),
    path('reporte/genero/', reporteEstudianteGenero.as_view(), name="reporte_genero"),
    path('reporte/modalidad/', reporteEstudianteModalidad.as_view(), name="reporte_modalidad"),
]
