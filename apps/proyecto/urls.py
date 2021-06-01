from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.conf.urls.static import static

app_name = 'sistemaGerencialAgro'

urlpatterns = [
    
    # Página de inicio del sistema
    path('', index),
    path('sistemaGerencialAgro/index/', index, name = 'index'),


    # Proyectos de Estudiante en Servicio Social por Departamento.
    path('sistemaGerencialAgro/consultaProyectosEstudianteDepartamento/', consultaEstudiantesDepartamento, name="consulta_estudiante_departamento"),
    path('sistemaGerencialAgro/filtrarProyectosEstudiantesDepartamento/', filtrarEstudiantesDepartamento, name="filtrar_estudiante_departamento"),


    # Ejecución del Procedimiento ETL.
    path('sistemaGerencialAgro/procesoETL/', procesoETL, name='procesoETL'),
    path('sistemaGerencialAgro/procedimientoETL/', procedimientoETL, name='procedimientoETL'),

    
    # ESTA URL ES SOLO PARA QUE FUNCIONE EL EJEMPLO, LUEGO SE BORRARA.
    #path('sistemaGerencialAgro/consultaEstudiantes/', consultaEstudiante, name="consulta_estudiante"),
    # Actualizar la BD por medio de la subida del archivo.
    #path('sistemaGerencialAgro/list/', lista, name='lista'),
    #path('sistemaGerencialAgro/actualizarBD/', actualizarBD, name='actualizarBD'),
]
