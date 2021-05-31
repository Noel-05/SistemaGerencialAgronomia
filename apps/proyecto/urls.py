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
    path('istemaGerencialAgro/consultaEstudiante/', consultaEstudiante, name="consulta_estudiante"),
    path('sistemaGerencialAgro/porcentaje/', consultaEstudiantesPorcentajeCarrera.as_view(), name="buscar_porcentaje"),
    path('sistemaGerencialAgro/genero/', consultaEstudiantesPorGenero.as_view(), name="buscar_genero"),
    path('sistemaGerencialAgro/modalidad/', consultaEstudiantesPorModalidad.as_view(), name="buscar_modalidad"),
    path('export/excel', export_estudiantes_csv, name='export_csv'),
    path('reporte/porcentaje', reporteEstudiantePorcentajeCarrera.as_view(), name="reporte_porcentaje"),
    path('reporte/genero/', reporteEstudianteGenero.as_view(), name="reporte_genero"),
    path('reporte/modalidad/', reporteEstudianteModalidad.as_view(), name="reporte_modalidad"),
    path('istemaGerencialAgro/consultaEstudiante/', login_required(consultaEstudiante), name="consulta_estudiante"),
    path('sistemaGerencialAgro/consultaSolicitudAprobadas/', consultaSolicitud, name="consulta_solicitud"),
    path('sistemaGerencialAgro/estado/', consultaSolicitudesAprobadas.as_view(), name="buscar_estado"),
    path('sistemaGerencialAgro/consultaSolicitudPeriodo/', consultaSolicitudPeriodo, name="solicitud_periodo"),
    path('sistemaGerencialAgro/periodo/', consultaEstudiantesPorPeriodo.as_view(), name="buscar_periodo"),
     path('reporte/estado', reporteSolicitudAprobada.as_view(), name="reporte_estado"),
 


]
