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


    # Ejecución del Procedimiento ETL.
    path('sistemaGerencialAgro/procesoETL/<str:username>', login_required(procesoETL), name='procesoETL'),
    path('sistemaGerencialAgro/procedimientoETL/', login_required(procedimientoETL), name='procedimientoETL'),

    
    # --------- REPORTES TACTICOS --------- 

    # Soliictudes de Servicio Social Aprobadas.

    path('sistemaGerencialAgro/consultaSolicitudAprobada/', consultaSolicitud, name="consulta_solicitud"),
    path('sistemaGerencialAgro/filtroSolicitudAprobada/', consultaEstudiantesSolicitudAprobada, name="filtrar_estado_solicitud"),
    path('sistemaGerencialAgro/reporteSolicitudAprobada/<str:estado>/', reporteSolicitudAprobada, name="reporte_solicitud_aprobada"),
    path('sistemaGerencialAgro/exportarSolicitudAprobada/<str:estado>/', exportarEstudiantesSolicitudAprobada, name="exportar_solicitud_aprobada"),

    # Estudiantes en Servicio Social por Período.
    path('sistemaGerencialAgro/consultaServicioSocialPeriodo/', consultaEstudiantesPeriodo, name="consulta_periodo_servsocial"),
    path('sistemaGerencialAgro/filtroServicioSocialPeriodo/', consultaEstudiantesServSocialPeriodo, name="filtrar_periodo_servsocial"),
    path('sistemaGerencialAgro/reporteServicioSocialPeriodo/<str:fecha>/', reporteEstudiantesServSocialPeriodo, name="reporte_periodo_servsocial"),
    path('sistemaGerencialAgro/exportarServicioSocialPeriodo/<str:fecha>/', exportarEstudiantesServSocialPeriodo, name="exportar_periodo_servsocial"),


    # Estudiantes en Servicio Social por Porcentaje.
    path('sistemaGerencialAgro/porcentaje/', consultaEstudiantesPorcentajeCarrera.as_view(), name="buscar_porcentaje"),
    path('sistemaGerencialAgro/reportePorcentaje/', reporteEstudiantesPorcentajeCarrera.as_view(), name="reporte_porcentaje"),

    # Estudiantes en Servicio Social por Genero.
    path('sistemaGerencialAgro/genero/', consultaEstudiantesPorGenero.as_view(), name="buscar_genero"),
    path('sistemaGerencialAgro/reporteGenero/', reporteEstudiantesPorGenero.as_view(), name="reporte_genero"),

    # Proyectos de Estudiante en Servicio Social por Departamento.
    path('sistemaGerencialAgro/consultaProyectosEstudianteDepartamento/', consultaEstudiantesDepartamento, name="consulta_estudiante_departamento"),
    path('sistemaGerencialAgro/filtrarProyectosEstudiantesDepartamento/', filtrarEstudiantesDepartamento, name="filtrar_estudiante_departamento"),
    path('sistemaGerencialAgro/reporteProyectosEstudiantesDepartamento/<str:depto>/', reporteEstudiantesDepartamento, name="reporte_estudiante_departamento"),
    path('sistemaGerencialAgro/exportarProyectosEstudiantesDepartamento/<str:depto>/', exportarEstudiantesDepartamento, name="exportar_estudiante_departamento"),


    # --------- REPORTES GERENCIALES --------- 

    # Estudiantes en Servicio Social por Modalidad.
    path('sistemaGerencialAgro/modalidad/', consultaEstudiantesPorModalidad.as_view(), name="buscar_modalidad"),
    path('sistemaGerencialAgro/reporteModalidad/', reporteEstudiantesPorModalidad.as_view(), name="reporte_modalidad"),
    path('sistemaGerencialAgro/listarEstudiosUniversitarios/', listarEstudioUniversitario, name="listar_estudios_universitarios"),
    path('sistemaGerencialAgro/listarSolicitudes/', listarSolicitudes, name="listar_solicitudes"),
    path('sistemaGerencialAgro/listarServicios/', listarServicios, name="listar_servicios"),

    # Estudiantes en Servicio Social por Carrera.

    # Docentes Tutores de Servicio Social.
    path('sistemaGerencialAgro/consultaEstudiantesPorDocente/', consultaEstudiantesDocente, name="consulta_estudiante_docente"),
    path('sistemaGerencialAgro/filtrarEstudiantesPorDocente/', filtrarEstudiantesDocentes, name="filtrar_estudiante_docente"),
    path('sistemaGerencialAgro/reporteEstudiantesPorDocente1/<str:docent>/', reporteEstudiantesPorDocentes1, name="reporte_estudiante_docente_uno"),
    path('sistemaGerencialAgro/reporteEstudiantesPorDocente2/<str:fecha_inic>/<str:docent>/', reporteEstudiantesPorDocentes2, name="reporte_estudiante_docente_dos"),


    # ->->->->->->->  NOTA: <-<-<-<-<-<-<-
    # LA PERSONA QUE HIZO ESTAS URL DE ABAJO AGREGARLAS A LA SECCION DE ARRIBA QUE CORRESPONDA.

    path('export/excel', export_estudiantes_csv, name='export_csv'),
    

    
    # Actualizar la BD por medio de la subida del archivo.
    #path('sistemaGerencialAgro/list/', lista, name='lista'),
    #path('sistemaGerencialAgro/actualizarBD/', actualizarBD, name='actualizarBD'),

]
