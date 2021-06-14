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

    path('sistemaGerencialAgro/consultaSolicitudAprobada/', login_required(consultaSolicitud), name="consulta_solicitud"),
    path('sistemaGerencialAgro/filtroSolicitudAprobada/', login_required(consultaEstudiantesSolicitudAprobada), name="filtrar_estado_solicitud"),
    path('sistemaGerencialAgro/reporteSolicitudAprobada/<str:estado>/', login_required(reporteSolicitudAprobada), name="reporte_solicitud_aprobada"),
    path('sistemaGerencialAgro/exportarSolicitudAprobada/<str:estado>/', login_required(exportarEstudiantesSolicitudAprobada), name="exportar_solicitud_aprobada"),

    # Estudiantes en Servicio Social por Período.
    path('sistemaGerencialAgro/consultaServicioSocialPeriodo/', login_required(consultaEstudiantesPeriodo), name="consulta_periodo_servsocial"),
    path('sistemaGerencialAgro/filtroServicioSocialPeriodo/', login_required(consultaEstudiantesServSocialPeriodo), name="filtrar_periodo_servsocial"),
    path('sistemaGerencialAgro/reporteServicioSocialPeriodo/<str:fecha_inicio>/<str:fecha_fin>', login_required(reporteEstudiantesServSocialPeriodo), name="reporte_periodo_servsocial"),
    path('sistemaGerencialAgro/exportarServicioSocialPeriodo/<str:fecha_inicio>/<str:fecha_fin>', login_required(exportarEstudiantesServSocialPeriodo), name="exportar_periodo_servsocial"),

        # Estudiantes en Servicio Social por Porcentaje.
    path('sistemaGerencialAgro/porcentaje/', login_required(consultaEstudiantesPorcentajeCarrera), name="buscar_porcentaje"),
    path('sistemaGerencialAgro/reportePorcentaje/<str:porcentaje>', login_required(reporteEstudiantesPorcentajeCarrera), name="reporte_porcentaje"),
    path('sistemaGerencialAgro/exportarEstudiantesPorcentaje/<str:porcentaje>/', login_required(exportarEstudiantesPorcentaje), name="exportar_estudiantes_porcentaje"),
    
    # Estudiantes en Servicio Social por Genero.
    path('sistemaGerencialAgro/genero/', login_required(consultaEstudiantesPorGenero), name="buscar_genero"),
    path('sistemaGerencialAgro/reporteGenero/<str:sexo>', login_required(reporteEstudiantesPorGenero), name="reporte_genero"),
    path('sistemaGerencialAgro/exportarEstudiantesGenero/<str:sexo>', login_required(exportarEstudiantesPorGenero), name="exportar_estudiantes_genero"),

    # Proyectos de Estudiante en Servicio Social por Departamento.
    path('sistemaGerencialAgro/consultaProyectosEstudianteDepartamento/', login_required(consultaEstudiantesDepartamento), name="consulta_estudiante_departamento"),
    path('sistemaGerencialAgro/filtrarProyectosEstudiantesDepartamento/', login_required(filtrarEstudiantesDepartamento), name="filtrar_estudiante_departamento"),
    path('sistemaGerencialAgro/reporteProyectosEstudiantesDepartamento/<str:depto>/', login_required(reporteEstudiantesDepartamento), name="reporte_estudiante_departamento"),
    path('sistemaGerencialAgro/exportarProyectosEstudiantesDepartamento/<str:depto>/', login_required(exportarEstudiantesDepartamento), name="exportar_estudiante_departamento"),


    # --------- REPORTES GERENCIALES --------- 

    # Estudiantes en Servicio Social por Modalidad.
    path('sistemaGerencialAgro/modalidad/', login_required(consultaEstudiantesPorModalidad), name="buscar_modalidad"),
    path('sistemaGerencialAgro/reporteModalidad/<str:modalidad>/', login_required(reporteEstudiantesPorModalidad), name="reporte_modalidad"),
    path('sistemaGerencialAgro/reporteModalidad/<str:modalidad>/<str:fecha>/', login_required(reporteEstudiantesPorModalidadFecha), name="reporte_modalidad_fecha"),
    path('sistemaGerencialAgro/exportarEstudiantesModalidad/<str:modalidad>', login_required(exportarEstudiantesPorModalidad),name="exportar_estudiantes_modalidad"),
    path('sistemaGerencialAgro/exportarEstudiantesModalidad/<str:fecha>/<str:modalidad>', login_required(exportarEstudiantesPorModalidadFecha),name="exportar_estudiantes_modalidad_fecha"),
    path('sistemaGerencialAgro/listarEstudiosUniversitarios/', login_required(listarEstudioUniversitario), name="listar_estudios_universitarios"),
    path('sistemaGerencialAgro/listarSolicitudes/', login_required(listarSolicitudes), name="listar_solicitudes"),
    path('sistemaGerencialAgro/listarServicios/', login_required(listarServicios), name="listar_servicios"),

    # Estudiantes en Servicio Social por Carrera.
    path('sistemaGerencialAgro/consultaCarreraPeriodo/', login_required(consultaEstudiantesCarrera), name="consulta_periodo_carrera"),
    path('sistemaGerencialAgro/filtroCarreraPeriodo/', login_required(consultaEstudiantesCarreraPeriodo), name="filtrar_periodo_carrera"),
    path('sistemaGerencialAgro/reporteCarreraPeriodo1/<str:carrera>/', login_required(reporteEstudianteCarreraPeriodo1), name="reporte_carrera_periodo_uno"),
    path('sistemaGerencialAgro/reporteCarreraPeriodo2/<str:fecha>/<str:carrera>/', login_required(reporteEstudianteCarreraPeriodo2), name="reporte_carrera_periodo_dos"),
    path('sistemaGerencialAgro/exportarCarreraPeriodo1/<str:carrera>/', login_required(exportarEstudianteCarreraPeriodo1), name="exportar_carrera_periodo_uno"),
    path('sistemaGerencialAgro/exportarCarreraPeriodo2/<str:fecha>/<str:carrera>/', login_required(exportarEstudianteCarreraPeriodo2), name="exportar_carrera_periodo_dos"),

    # Docentes Tutores de Servicio Social.
    path('sistemaGerencialAgro/consultaEstudiantesPorDocente/', login_required(consultaEstudiantesDocente), name="consulta_estudiante_docente"),
    path('sistemaGerencialAgro/filtrarEstudiantesPorDocente/', login_required(filtrarEstudiantesDocentes), name="filtrar_estudiante_docente"),
    path('sistemaGerencialAgro/reporteEstudiantesPorDocente1/<str:docent>/', login_required(reporteEstudiantesPorDocentes1), name="reporte_estudiante_docente_uno"),
    path('sistemaGerencialAgro/reporteEstudiantesPorDocente2/<str:fecha_inic>/<str:docent>/', login_required(reporteEstudiantesPorDocentes2), name="reporte_estudiante_docente_dos"),
    path('sistemaGerencialAgro/exportarEstudiantesPorDocente1/<str:fecha_inic>/<str:docent>/', login_required(exportarEstudiantesDocente1), name="exportar_estudiante_docente_uno"),
    path('sistemaGerencialAgro/exportarEstudiantesPorDocente2/<str:docent>/', login_required(exportarEstudiantesDocente2), name="exportar_estudiante_docente_dos"),
    
    # Actualizar la BD por medio de la subida del archivo.
    #path('sistemaGerencialAgro/list/', lista, name='lista'),
    path('sistemaGerencialAgro/actualizarBD/', actualizarBD, name='actualizarBD'),

]
