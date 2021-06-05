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
    path('sistemaGerencialAgro/porcentaje/', consultaEstudiantesPorcentajeCarrera, name="buscar_porcentaje"),
    path('sistemaGerencialAgro/reportePorcentaje/<str:porcentaje>', reporteEstudiantesPorcentajeCarrera, name="reporte_porcentaje"),
    path('sistemaGerencialAgro/exportarEstudiantesPorcentaje/<str:porcentaje>/', exportarEstudiantesPorcentaje, name="exportar_estudiantes_porcentaje"),
    
    # Estudiantes en Servicio Social por Genero.
    path('sistemaGerencialAgro/genero/', consultaEstudiantesPorGenero, name="buscar_genero"),
    path('sistemaGerencialAgro/reporteGenero/<str:sexo>', reporteEstudiantesPorGenero, name="reporte_genero"),
    path('sistemaGerencialAgro/exportarEstudiantesGenero/<str:sexo>',exportarEstudiantesPorGenero, name="exportar_estudiantes_genero"),

    # Proyectos de Estudiante en Servicio Social por Departamento.
    path('sistemaGerencialAgro/consultaProyectosEstudianteDepartamento/', consultaEstudiantesDepartamento, name="consulta_estudiante_departamento"),
    path('sistemaGerencialAgro/filtrarProyectosEstudiantesDepartamento/', filtrarEstudiantesDepartamento, name="filtrar_estudiante_departamento"),
    path('sistemaGerencialAgro/reporteProyectosEstudiantesDepartamento/<str:depto>/', reporteEstudiantesDepartamento, name="reporte_estudiante_departamento"),
    path('sistemaGerencialAgro/exportarProyectosEstudiantesDepartamento/<str:depto>/', exportarEstudiantesDepartamento, name="exportar_estudiante_departamento"),


    # --------- REPORTES GERENCIALES --------- 

    # Estudiantes en Servicio Social por Modalidad.
    path('sistemaGerencialAgro/modalidad/', consultaEstudiantesPorModalidad, name="buscar_modalidad"),
    path('sistemaGerencialAgro/reporteModalidad/<str:modalidad>/', reporteEstudiantesPorModalidad, name="reporte_modalidad"),
    path('sistemaGerencialAgro/reporteModalidad/<str:modalidad>/<str:fecha>/', reporteEstudiantesPorModalidadFecha, name="reporte_modalidad_fecha"),
    path('sistemaGerencialAgro/exportarEstudiantesModalidad/<str:modalidad>', exportarEstudiantesPorModalidad,name="exportar_estudiantes_modalidad"),
    path('sistemaGerencialAgro/exportarEstudiantesModalidad/<str:fecha>/<str:modalidad>', exportarEstudiantesPorModalidadFecha,name="exportar_estudiantes_modalidad_fecha"),
    path('sistemaGerencialAgro/listarEstudiosUniversitarios/', listarEstudioUniversitario, name="listar_estudios_universitarios"),
    path('sistemaGerencialAgro/listarSolicitudes/', listarSolicitudes, name="listar_solicitudes"),
    path('sistemaGerencialAgro/listarServicios/', listarServicios, name="listar_servicios"),

    # Estudiantes en Servicio Social por Carrera.
    path('sistemaGerencialAgro/consultaCarreraPeriodo/', consultaEstudiantesCarrera, name="consulta_periodo_carrera"),
    path('sistemaGerencialAgro/filtroCarreraPeriodo/', consultaEstudiantesCarreraPeriodo, name="filtrar_periodo_carrera"),
    path('sistemaGerencialAgro/reporteCarreraPeriodo1/<str:carrera>/', reporteEstudianteCarreraPeriodo1, name="reporte_carrera_periodo_uno"),
    path('sistemaGerencialAgro/reporteCarreraPeriodo2/<str:fecha>/<str:carrera>/', reporteEstudianteCarreraPeriodo2, name="reporte_carrera_periodo_dos"),
    path('sistemaGerencialAgro/exportarCarreraPeriodo1/<str:carrera>/', exportarEstudianteCarreraPeriodo1, name="exportar_carrera_periodo_uno"),
    path('sistemaGerencialAgro/exportarCarreraPeriodo2/<str:fecha>/<str:carrera>/', exportarEstudianteCarreraPeriodo2, name="exportar_carrera_periodo_dos"),



    # Docentes Tutores de Servicio Social.
    path('sistemaGerencialAgro/consultaEstudiantesPorDocente/', consultaEstudiantesDocente, name="consulta_estudiante_docente"),
    path('sistemaGerencialAgro/filtrarEstudiantesPorDocente/', filtrarEstudiantesDocentes, name="filtrar_estudiante_docente"),
    path('sistemaGerencialAgro/reporteEstudiantesPorDocente1/<str:docent>/', reporteEstudiantesPorDocentes1, name="reporte_estudiante_docente_uno"),
    path('sistemaGerencialAgro/reporteEstudiantesPorDocente2/<str:fecha_inic>/<str:docent>/', reporteEstudiantesPorDocentes2, name="reporte_estudiante_docente_dos"),
    path('sistemaGerencialAgro/exportarEstudiantesPorDocente1/<str:fecha_inic>/<str:docent>/', exportarEstudiantesDocente1, name="exportar_estudiante_docente_uno"),
    path('sistemaGerencialAgro/exportarEstudiantesPorDocente2/<str:docent>/', exportarEstudiantesDocente2, name="exportar_estudiante_docente_dos"),


    # ->->->->->->->  NOTA: <-<-<-<-<-<-<-
    # LA PERSONA QUE HIZO ESTAS URL DE ABAJO AGREGARLAS A LA SECCION DE ARRIBA QUE CORRESPONDA.
    

    
    # Actualizar la BD por medio de la subida del archivo.
    #path('sistemaGerencialAgro/list/', lista, name='lista'),
    #path('sistemaGerencialAgro/actualizarBD/', actualizarBD, name='actualizarBD'),

]
