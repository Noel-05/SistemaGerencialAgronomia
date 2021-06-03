from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.conf.urls.static import static

app_name = 'sistemaGerencialAgro'

urlpatterns = [

    # Página de inicio del sistema
    path('', login_required(index)),
    path('sistemaGerencialAgro/index/', login_required(index), name = 'index'),


    # Proyectos de Estudiante en Servicio Social por Departamento.
    path('sistemaGerencialAgro/consultaProyectosEstudianteDepartamento/', consultaEstudiantesDepartamento, name="consulta_estudiante_departamento"),
    path('sistemaGerencialAgro/filtrarProyectosEstudiantesDepartamento/', filtrarEstudiantesDepartamento, name="filtrar_estudiante_departamento"),


    # Ejecución del Procedimiento ETL.
    path('sistemaGerencialAgro/procesoETL/', procesoETL, name='procesoETL'),
    path('sistemaGerencialAgro/procedimientoETL/', procedimientoETL, name='procedimientoETL'),

    
    # ESTA URL ES SOLO PARA QUE FUNCIONE EL EJEMPLO, LUEGO SE BORRARA
    path('sistemaGerencialAgro/porcentaje/', consultaEstudiantesPorcentajeCarrera.as_view(), name="buscar_porcentaje"),
    path('sistemaGerencialAgro/listarEstudiosUniversitarios/', listarEstudioUniversitario, name="listar_estudios_universitarios"),
    path('sistemaGerencialAgro/genero/', consultaEstudiantesPorGenero.as_view(), name="buscar_genero"),
    path('sistemaGerencialAgro/listarSolicitudes/', listarSolicitudes, name="listar_solicitudes"),
    path('sistemaGerencialAgro/modalidad/', consultaEstudiantesPorModalidad.as_view(), name="buscar_modalidad"),
    path('sistemaGerencialAgro/listarServicios/', listarServicios, name="listar_servicios"),
    path('sistemaGerencialAgro/reportePorcentaje/', reporteEstudiantesPorcentajeCarrera.as_view(), name="reporte_porcentaje"),
    path('sistemaGerencialAgro/reporteGenero/', reporteEstudiantesPorGenero.as_view(), name="reporte_genero"),
    path('sistemaGerencialAgro/reporteModalidad/', reporteEstudiantesPorModalidad.as_view(), name="reporte_modalidad"),
    path('export/excel', export_estudiantes_csv, name='export_csv'),
    path('sistemaGerencialAgro/consultaSolicitudAprobadas/', consultaSolicitud, name="consulta_solicitud"),
    path('sistemaGerencialAgro/estado/', consultaSolicitudesAprobadas.as_view(), name="buscar_estado"),
    path('sistemaGerencialAgro/consultaSolicitudPeriodo/', consultaSolicitudPeriodo, name="solicitud_periodo"),
    path('sistemaGerencialAgro/periodo/', consultaEstudiantesPorPeriodo.as_view(), name="buscar_periodo"),
    path('reporte/estado', reporteSolicitudAprobada.as_view(), name="reporte_estado"),

    # ESTA URL ES SOLO PARA QUE FUNCIONE EL EJEMPLO, LUEGO SE BORRARA.
    #path('sistemaGerencialAgro/consultaEstudiantes/', consultaEstudiante, name="consulta_estudiante"),
    # Actualizar la BD por medio de la subida del archivo.
    #path('sistemaGerencialAgro/list/', lista, name='lista'),
    #path('sistemaGerencialAgro/actualizarBD/', actualizarBD, name='actualizarBD'),

]
