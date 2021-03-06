from django.shortcuts import render,redirect
from django.core import serializers
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.conf import settings
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView,View
from django.http import HttpResponse

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from .models import *
import xlwt
import os

import sqlite3
import time
import mechanize
from mechanize import Browser
from datetime import datetime
from .models import *
from .forms import *


#---------------------------------------------------------------------------------------------------------------


"""
Función para mostrar la página de inicio del sistema.
@param      una solicitud de petición (request)
@return     retorna el template base del sistema
@author     Noel Renderos
"""

def index(request):

    return render(
        request,
        'base/base.html',
    )


#---------------------------------------------------------------------------------------------------------------


"""
Función para mostrar imagenes dentro de los reportes en PDF elaborados.
@param      una url relativa
@return     Retorna la configuración de Settings donde estan alojadas las imagenes
@author     Noel Renderos
"""

def link_callback(uri, rel):
    """
    Convierte HTML a URIs absoluta en el Path del sistema para que  xhtml2pdf
    tenga acceso a los recuros
    """
    result = finders.find(uri)

    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
    
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
    
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
    
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    
    return path


#---------------------------------------------------------------------------------------------------------------


"""
Función para recuperar y mostrar el listado de departamentos para su selección y realización del 
filtro correspondiente y de la recuperación de todos los proyectos agrupados por departamento.
@param      una solicitud de petición (request)
@return     retorna el template estudiantesServSocDepartamento con el diccionario detallado en la descripción.
@author     Noel Renderos
"""

def consultaEstudiantesDepartamento(request):

    departamentos = Departamento.objects.all()

    # Se usa doble subrayado para que funcione como el "." en el template (osea un join)
    proyectos_departamento = ServicioSocial.objects.order_by('carnet_estudiante__carnet_estudiante__codigo_carrera__departamento')
    
    context = {
        'proyectos_departamento': proyectos_departamento,
        'departamentos': departamentos,
    }

    return render(
        request,
        'proyecto/estudiantesServSocDepartamento.html', 
        context,
    )


"""
Función para realizar el filtro correspondiente de los proyectos por departamento.
@param      una solicitud de petición (request)
@return     retorna el template estudiantesServSocDepartamento con los proyectos filtrados por departamento.
@author     Noel Renderos
"""

def filtrarEstudiantesDepartamento(request):

    if request.method == 'POST':
        depto = request.POST['departamento']

        # Se usa doble subrayado para que funcione como el "." en el template (osea un join)
        proyectos_departamento_filtro = ServicioSocial.objects.filter(carnet_estudiante__carnet_estudiante__codigo_carrera__departamento=depto)
        departamentos = Departamento.objects.all()

        context = {
            'proyectos_departamento_filtro': proyectos_departamento_filtro,
            'departamentos': departamentos,
            'depto': depto,
        }

        return render(
            request,
            'proyecto/estudiantesServSocDepartamento.html', 
            context,
        )


"""
Función para realizar el PDF correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request) y el departamento a filtrar en la sentencia SQL.
@return     retorna la vista previa del pdf por medio de una peticion request.
@author     Noel Renderos
"""

def reporteEstudiantesDepartamento(request, depto):

    proyectos_departamento_filtro = ServicioSocial.objects.filter(carnet_estudiante__carnet_estudiante__codigo_carrera__departamento=depto)

    template = get_template('reportes/ReporteProyectosDepartamento.html')

    context = {
        'proyectos_departamento_filtro': proyectos_departamento_filtro
    }

    html = template.render(context)
    
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'inline; filename="RT-ProyectosPorDepartamento.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest = response, link_callback=link_callback)
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>'+ html + '</pre>')
    
    return response


"""
Función para realizar el CSV correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request) y el departamento a filtrar en la sentencia SQL.
@return     descarga el archivo CSV con el nombre indicado por medio de una peticion request.
@author     Noel Renderos
"""

def exportarEstudiantesDepartamento(request, depto):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="RT-ProyectosPorDepartamento.csv"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Proyectos por Departamento') 

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Departamento', 'Proyecto', 'Carnet', 'Nombre', 'Apellido', 'Carrera']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    proyectos_departamento_filtro = ServicioSocial.objects.filter(carnet_estudiante__carnet_estudiante__codigo_carrera__departamento=depto)

    for proyDepto in proyectos_departamento_filtro:
        row_num += 1
        row = [proyDepto.carnet_estudiante.carnet_estudiante.codigo_carrera.departamento.nombreDepartamento, proyDepto.codigo_proyecto.descripcion_proyecto, proyDepto.carnet_estudiante.carnet_estudiante.carnet_estudiante.carnet_estudiante, proyDepto.carnet_estudiante.carnet_estudiante.carnet_estudiante.nombre_estudiante, proyDepto.carnet_estudiante.carnet_estudiante.carnet_estudiante.apellido_estudiante, proyDepto.carnet_estudiante.carnet_estudiante.codigo_carrera.nombre_carrera]
        
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response


"""
Función para recuperar y mostrar el listado de estudiantes que tienen a cargo los docentes tutores 
agrupados por el carnet del estudiante.
@param      una solicitud de petición (request)
@return     retorna el template docentesServSocDepartamento con el diccionario detallado en la descripción.
@author     Roberto Paz
"""

def consultaEstudiantesDocente(request):

    docentes = Docente.objects.all()

    # Se usa doble subrayado para que funcione como el "." en el template (osea un join)
    estudiantes_docentes = Solicitud.objects.order_by('carnet_estudiante__carnet_estudiante')
    
    context = {
        'estudiantes_docentes': estudiantes_docentes,
        'docentes': docentes,
    }

    return render(
        request,
        'proyecto/docentesServSocDepartamento.html', 
        context,
    )

"""
Función para realizar el filtro correspondiente de los estudiantes que son tutelados por el docente 
seleccionado.
@param      una solicitud de petición (request)
@return     retorna el template docentesServSocDepartamento con los estudiantes filtrados de a cuerdo
al Docente seleccionado.
@author     Roberto Paz
"""

def filtrarEstudiantesDocentes(request):

    if request.method == 'POST':
        docent = request.POST['docent']
        fecha_inic = request.POST['fecha_inic'] 

        # Se usa doble subrayado para que funcione como el "." en el template (osea un join)
        estudiantes_docentes_filtro = ServicioSocial.objects.order_by('carnet_estudiante__carnet_estudiante__carnet_estudiante')
        docentes = Docente.objects.all()

        context = {
            'estudiantes_docentes_filtro': estudiantes_docentes_filtro,
            'docentes': docentes,
            'docent': docent,
            'fecha_inic': fecha_inic,
        }

        return render(
            request,
            'proyecto/docentesServSocDepartamento.html', 
            context,
        )

"""
Función para realizar el PDF correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request) y el docente para filtrar en la sentencia SQL.
@return     retorna la vista previa del pdf por medio de una peticion request.
@author     Roberto Paz
"""

def reporteEstudiantesPorDocentes1(request, docent):

    estudiantes_docentes_filtro = ServicioSocial.objects.order_by('carnet_estudiante__carnet_estudiante__carnet_estudiante')
    fecha_inic = ""
    docent = docent

    template = get_template('reportes/ReporteEstudianteDocente.html')

    context = {
        'estudiantes_docentes_filtro': estudiantes_docentes_filtro,
        'fecha_inic': fecha_inic,
        'docent': docent,
    }

    html = template.render(context)
    
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'inline; filename="RG-EstudiantesPorDocente.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest = response, link_callback=link_callback)
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>'+ html + '</pre>')
    
    return response

"""
Función para realizar el PDF correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request), la fecha inicial del SS
y el docente a filtrar en la sentencia SQL.
@return     retorna la vista previa del pdf por medio de una peticion request.
@author     Roberto Paz
"""

def reporteEstudiantesPorDocentes2(request, fecha_inic, docent):

    estudiantes_docentes_filtro = ServicioSocial.objects.order_by('carnet_estudiante__carnet_estudiante__carnet_estudiante')
    fecha_inic = fecha_inic
    docent = docent

    template = get_template('reportes/ReporteEstudianteDocente.html')

    context = {
        'estudiantes_docentes_filtro': estudiantes_docentes_filtro,
        'fecha_inic': fecha_inic,
        'docent': docent,
    }

    html = template.render(context)
    
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'inline; filename="RG-EstudiantesPorDocente.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest = response, link_callback=link_callback)
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>'+ html + '</pre>')
    
    return response


"""
Función para realizar el CSV correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request), la fecha inicial del SS y el docente a 
filtrar en la sentencia SQL.
@return     descarga el archivo CSV con el nombre indicado por medio de una peticion request.
@author     Roberto Paz
"""

def exportarEstudiantesDocente1(request, fecha_inic, docent):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="RG-EstudiantesPorDocente.csv"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Estudiantes por Docente') 

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Carnet', 'Nombre', 'Apellido', 'Fecha Inicial']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    estudiantes_docentes_filtro = ServicioSocial.objects.order_by('carnet_estudiante__carnet_estudiante__carnet_estudiante')

    for fil in estudiantes_docentes_filtro:
        if fil.carnet_docente_id == docent:
            fecha_formato_com = datetime.strftime(fil.carnet_estudiante.fecha_inicio, '%Y-%m-%d')  # trasformar
            fecha_formato_imp = datetime.strftime(fil.carnet_estudiante.fecha_inicio, '%d-%m-%Y')  # trasformar
            if fecha_inic <= fecha_formato_com:
                row_num += 1
                row = [fil.carnet_estudiante.carnet_estudiante.carnet_estudiante_id, fil.carnet_estudiante.carnet_estudiante.carnet_estudiante.nombre_estudiante, fil.carnet_estudiante.carnet_estudiante.carnet_estudiante.apellido_estudiante, fecha_formato_imp]
                    
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

"""
Función para realizar el CSV correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request) y el docente a filtrar en la sentencia SQL.
@return     descarga el archivo CSV con el nombre indicado por medio de una peticion request.
@author     Roberto Paz
"""

def exportarEstudiantesDocente2(request, docent):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="RG-EstudiantesPorDocente.csv"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Estudiantes por Docente') 

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Carnet', 'Nombre', 'Apellido', 'Fecha Inicial']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    estudiantes_docentes_filtro = ServicioSocial.objects.order_by('carnet_estudiante__carnet_estudiante__carnet_estudiante')

    for fil in estudiantes_docentes_filtro:
        if fil.carnet_docente_id == docent:
            fecha_formato_imp = datetime.strftime(fil.carnet_estudiante.fecha_inicio, '%d-%m-%Y')  # trasformar
            row_num += 1
            row = [fil.carnet_estudiante.carnet_estudiante.carnet_estudiante_id, fil.carnet_estudiante.carnet_estudiante.carnet_estudiante.nombre_estudiante, fil.carnet_estudiante.carnet_estudiante.carnet_estudiante.apellido_estudiante, fecha_formato_imp]
            print(row)
            
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

#---------------------------------------------------------------------------------------------------------------


"""
Función para mostrar la bitacora de procedimientos ETL ejecutados para su debida administración.
@param      una solicitud de petición (request)
@return     retorna el template procesoETL junto al diccionario de datos con los datos de la bitacora.
@author     Noel Renderos
"""

def procedimientoETL(request):

    bitacora = Bitacora.objects.order_by('-fecha_modificacion', '-hora_modificacion')

    context = {
        'bitacora': bitacora,
    }

    return render(
        request,
        'proyecto/procesoETL.html',
        context
    )


"""
Función para realizar el proceso de Extracción, Transformación y Carga de los datos de la BD Transaccional a la BD Gerencial.
@param      una solicitud de petición (request)
@return     retorna un mensaje de confirmación del procedimiento realizado, junto a la bitacora correspondiente como administración de dichas acciones.
@author     Noel Renderos
"""

def procesoETL(request, username):

    # ----- PARTE DE LA EXTRACCION (E) -----

    # Creamos navegador.
    browser = Browser()
    
    # Definimos que No somos un robot para no activar el robot.txt de la pagina.
    browser.set_handle_robots(False)

    # Definimos la URL que posee el Login.
    browser.open("https://www.pythonanywhere.com/login/")
    
    # Seleccionamos el formulario correspondiente al Login.
    browser.select_form(nr=0)
    
    # Rellenar los campos correspondientes del formulario.
    browser["auth-username"] = "ProyeccionSocialAgronomiaUES"
    browser["auth-password"] = "agronomia2020"
    
    # Enviamos el formulario.
    response = browser.submit()
    
    # Definimos la URL que queremos acceder, en este caso la de descarga de la BD.
    browser.retrieve('https://www.pythonanywhere.com/user/ProyeccionSocialAgronomiaUES/files/home/ProyeccionSocialAgronomiaUES/SistemaAgronomia/db.sqlite3','BDTransaccional.sqlite3')[0] 


    # ----- PARTE DE LA TRANSFORMACIÓN Y CARGA (TL) -----

    # Creamos un objeto de conexión a la base de datos SQLite que acabamos de descargar en la raiz del proyecto
    con = sqlite3.connect("BDTransaccional.sqlite3")

    # Con la conexión hecha, creamos un objeto cursor para iterar dicha base
    cur = con.cursor()

    # El resultado de "cursor.execute" puede ser iterado fila por fila de cada tabla

    # Para la Tabla Departamento
    queryset = Departamento.objects.all()
    if len(queryset) == 0:
        for row in cur.execute('SELECT * FROM app1_departamento;'):
            departamento = Departamento(codigoDepartamento=row[0], nombreDepartamento=row[1], nombreJefeDepartamento=row[2], apellidoJefeDepartamento=row[3])
            departamento.save()
    else:
        i=0
        while i < len(queryset):
            prueba = " "
            for row in cur.execute('SELECT * FROM app1_departamento where codigoDepartamento = "'+str(queryset[i].codigoDepartamento)+'";'):
                prueba = row[0]
            if prueba == " ":
                obtener = Departamento.objects.get(codigoDepartamento=queryset[i].codigoDepartamento)
                obtener.delete()
            else:
                for row in cur.execute('SELECT * FROM app1_departamento;'):
                    departamento = Departamento(codigoDepartamento=row[0], nombreDepartamento=row[1], nombreJefeDepartamento=row[2], apellidoJefeDepartamento=row[3])
                    departamento.save()
            i+=1
    
    # Para la Tabla Carrera
    queryset = Carrera.objects.all()
    if len(queryset) == 0:
        for row in cur.execute('SELECT * FROM app1_carrera;'):
            carrera = Carrera(codigo_carrera=row[0], nombre_carrera=row[1], departamento_id=row[2])
            carrera.save()
    else:
        i=0
        while i < len(queryset):
            prueba = " "
            for row in cur.execute('SELECT * FROM app1_carrera where codigo_carrera = "'+str(queryset[i].codigo_carrera)+'";'):
                prueba = row[0]
            if prueba == " ":
                obtener = Carrera.objects.get(codigo_carrera=queryset[i].codigo_carrera)
                obtener.delete()
            else:
                for row in cur.execute('SELECT * FROM app1_carrera;'):
                    carrera = Carrera(codigo_carrera=row[0], nombre_carrera=row[1], departamento_id=row[2])
                    carrera.save()
            i+=1

    # Para la Tabla Estudiante
    queryset = Estudiante.objects.all()
    if len(queryset) == 0:
        for row in cur.execute('SELECT * FROM app1_estudiante;'):
            estudiante = Estudiante(carnet_estudiante=row[0], nombre_estudiante=row[1], apellido_estudiante=row[2], sexo_estudiante=row[3], telefono_estudiante=row[4], correo_estudiante=row[5], direccion_estudiante=row[6])
            estudiante.save()
    else:
        i=0
        while i < len(queryset):
            prueba = " "
            for row in cur.execute('SELECT * FROM app1_estudiante where carnet_estudiante = "'+str(queryset[i].carnet_estudiante)+'";'):
                prueba = row[0]
            if prueba == " ":
                obtener = Estudiante.objects.get(carnet_estudiante=queryset[i].carnet_estudiante)
                obtener.delete()
            else:
                for row in cur.execute('SELECT * FROM app1_estudiante;'):
                    estudiante = Estudiante(carnet_estudiante=row[0], nombre_estudiante=row[1], apellido_estudiante=row[2], sexo_estudiante=row[3], telefono_estudiante=row[4], correo_estudiante=row[5], direccion_estudiante=row[6])
                    estudiante.save()
            i+=1
    
    # Para la Tabla Estudio Universitario
    queryset = EstudioUniversitario.objects.all()
    if len(queryset) == 0:
        for row in cur.execute('SELECT * FROM app1_estudiouniversitario;'):
            estudioUniversitario = EstudioUniversitario(carnet_estudiante_id=row[0], porc_carrerar_aprob=row[1], unidades_valorativas=row[2], experiencia_areas_conoc=row[3], codigo_carrera_id=row[4], codigo_ciclo=row[5])
            estudioUniversitario.save()
    else:
        i=0
        while i < len(queryset):
            prueba = " "
            for row in cur.execute('SELECT * FROM app1_estudiouniversitario where carnet_estudiante_id = "'+str(queryset[i].carnet_estudiante)+'";'):
                prueba = row[0]
            if prueba == " ":
                obtener = EstudioUniversitario.objects.get(carnet_estudiante_id=queryset[i].carnet_estudiante)
                obtener.delete()
            else:
                for row in cur.execute('SELECT * FROM app1_estudiouniversitario;'):
                    estudioUniversitario = EstudioUniversitario(carnet_estudiante_id=row[0], porc_carrerar_aprob=row[1], unidades_valorativas=row[2], experiencia_areas_conoc=row[3], codigo_carrera_id=row[4], codigo_ciclo=row[5])
                    estudioUniversitario.save()
            i+=1
    
    # Para la Tabla Solicitud
    queryset = Solicitud.objects.all()
    if len(queryset) == 0:
        for row in cur.execute('SELECT * FROM app1_solicitud;'):
            solicitud = Solicitud(carnet_estudiante_id=row[0], horas_semana=row[1], dias_semana=row[2], modalidad=row[3], fecha_inicio=row[4], fecha_fin=row[5], codigo_entidad=row[6])
            solicitud.save()
    else:
        i=0
        while i < len(queryset):
            prueba = " "
            for row in cur.execute('SELECT * FROM app1_solicitud where carnet_estudiante_id = "'+str(queryset[i].carnet_estudiante)+'";'):
                prueba = row[0]
            if prueba == " ":
                obtener = Solicitud.objects.get(carnet_estudiante_id=queryset[i].carnet_estudiante)
                obtener.delete()
            else:
                for row in cur.execute('SELECT * FROM app1_solicitud;'):
                    solicitud = Solicitud(carnet_estudiante_id=row[0], horas_semana=row[1], dias_semana=row[2], modalidad=row[3], fecha_inicio=row[4], fecha_fin=row[5], codigo_entidad=row[6])
                    solicitud.save()
            i+=1
    
    # Para la Tabla Estado Solicitud
    queryset = EstadoSolicitud.objects.all()
    if len(queryset) == 0:
        for row in cur.execute('SELECT * FROM app1_estadosolicitud;'):
            estadosolicitud = EstadoSolicitud(carnet_estudiante_id=row[0], aceptado =row[1], motivo=row[2], observaciones=row[3])
            estadosolicitud.save()
    else:
        i=0
        while i < len(queryset):
            prueba = " "
            for row in cur.execute('SELECT * FROM app1_estadosolicitud where carnet_estudiante_id = "'+str(queryset[i].carnet_estudiante)+'";'):
                prueba = row[0]
            if prueba == " ":
                obtener = EstadoSolicitud.objects.get(carnet_estudiante_id=queryset[i].carnet_estudiante)
                obtener.delete()
            else:
                for row in cur.execute('SELECT * FROM app1_estadosolicitud;'):
                    estadosolicitud = EstadoSolicitud(carnet_estudiante_id=row[0], aceptado =row[1], motivo=row[2], observaciones=row[3])
                    estadosolicitud.save()
            i+=1

    # Para la Tabla Docente
    queryset = Docente.objects.all()
    if len(queryset) == 0:
        for row in cur.execute('SELECT * FROM app1_docente;'):
            docente = Docente(carnet_docente=row[0], nombre_docente =row[1], apellido_docente=row[2], departamento_id=row[3], nombre_rol=row[4])
            docente.save()
    else:
        i=0
        while i < len(queryset):
            prueba = " "
            for row in cur.execute('SELECT * FROM app1_docente where carnet_docente = "'+str(queryset[i].carnet_docente)+'";'):
                prueba = row[0]
            if prueba == " ":
                obtener = Docente.objects.get(carnet_docente=queryset[i].carnet_docente)
                obtener.delete()
            else:
                for row in cur.execute('SELECT * FROM app1_docente;'):
                    docente = Docente(carnet_docente=row[0], nombre_docente =row[1], apellido_docente=row[2], departamento_id=row[3], nombre_rol=row[4])
                    docente.save()
            i+=1

    # Para la Tabla Proyecto
    queryset = Proyecto.objects.all()
    if len(queryset) == 0:
        for row in cur.execute('SELECT * FROM app1_proyecto;'):
            proyecto = Proyecto(codigo_proyecto=row[0], descripcion_proyecto =row[1])
            proyecto.save()
    else:
        i=0
        while i < len(queryset):
            prueba = " "
            for row in cur.execute('SELECT * FROM app1_proyecto where codigo_proyecto = "'+str(queryset[i].codigo_proyecto)+'";'):
                prueba = row[0]
            if prueba == " ":
                obtener = Proyecto.objects.get(codigo_proyecto=queryset[i].codigo_proyecto)
                obtener.delete()
            else:
                for row in cur.execute('SELECT * FROM app1_proyecto;'):
                    proyecto = Proyecto(codigo_proyecto=row[0], descripcion_proyecto =row[1])
                    proyecto.save()
            i+=1
    
    # Para la Tabla ServicioSocial
    queryset = ServicioSocial.objects.all()
    if len(queryset) == 0:
        for row in cur.execute('SELECT * FROM app1_serviciosocial;'):
            serviciosocial = ServicioSocial(carnet_estudiante_id=row[0], carnet_docente_id =row[1], codigo_proyecto_id=row[2])
            serviciosocial.save()
    else:
        i=0
        while i < len(queryset):
            prueba = " "
            for row in cur.execute('SELECT * FROM app1_serviciosocial where carnet_estudiante_id = "'+str(queryset[i].carnet_estudiante)+'";'):
                prueba = row[0]
            if prueba == " ":
                obtener = ServicioSocial.objects.get(carnet_estudiante=queryset[i].carnet_estudiante)
                obtener.delete()
            else:
                for row in cur.execute('SELECT * FROM app1_serviciosocial;'):
                    serviciosocial = ServicioSocial(carnet_estudiante_id=row[0], carnet_docente_id =row[1], codigo_proyecto_id=row[2])
                    serviciosocial.save()
            i+=1

    # Registramos en la bítacora el día que se registro el procedimiento ETL
    now = datetime.now()
    now2 = now.date()
    now3 = time.strftime('%H:%M:%S', time.localtime())
    desc = "Procedimiento ETL ejecutado."
    bitacora = Bitacora(usuario=username, fecha_modificacion=now2, hora_modificacion=now3, descripcion=desc)
    bitacora.save()

    # Cerramos la conexión
    con.close()


    # ----- FIN DEL PROCESO ETL -----

    # Mandamo un mensaje para identificar que se realizo el procedimiento
    mensaje = "Procedimiento ETL Completado."

    bitacora = Bitacora.objects.order_by('-fecha_modificacion', '-hora_modificacion')

    context = {
        'mensaje': mensaje,
        'bitacora': bitacora,
    }

    return render(
        request,
        'proyecto/procesoETL.html', 
        context
    )


#------------------------------------------------------------------------------
"""
Función para recuperar y mostrar el listado de estudios universitarios 
@param      una solicitud de petición (request)
@return     retorna el template EstudiantesPorcentajeCarrera con el diccionario detallado en la descripción.
@author     Elmer Huiza
"""
def listarEstudioUniversitario(request):
    estudios_universitarios = EstudioUniversitario.objects.all()

    return render(
        request,
        'proyecto/EstudiantesPorcentajeCarrera.html',
        {'estudios_universitarios':estudios_universitarios}
    )
"""
Función para realizar el filtro correspondiente de los estudiantes por porcentaje de  carrrera aprobado.
@param      una solicitud de petición (request)
@return     retorna el template EstudiantesPorcentajeCarrera con los estudiantes filtrados por porcentaje de carrera aprobado.
@author     Elmer Huiza
"""
def consultaEstudiantesPorcentajeCarrera(request):
    if request.method == 'POST':
        porcentaje = request.POST['porcentaje']
        estudios_universitarios = EstudioUniversitario.objects.all()
        estudios_universitarios = estudios_universitarios.filter(porc_carrerar_aprob__gte=porcentaje)

    return render(
        request,
        'proyecto/EstudiantesPorcentajeCarrera.html',
        {'estudios_universitarios':estudios_universitarios,
        'porcentaje':porcentaje
        }
    )


"""Función para realizar el PDF correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request) y el porcentaje para filtrar en la sentencia SQL.
@return     retorna la vista previa del pdf por medio de una peticion request.
@author     Elmer Huiza
"""
def reporteEstudiantesPorcentajeCarrera(request, porcentaje):
    estudios_universitarios = EstudioUniversitario.objects.filter(porc_carrerar_aprob__gte=porcentaje)

    template = get_template('reportes/ReportePorcentajeCarrera.html')
        
    context = {
            'estudios_universitarios':estudios_universitarios,
        }
        
    html = template.render(context)
        
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="RT-EstudiantesPorPorcentaje.pdf"'
        
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
        
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>'+ html + '</pre>')
        
    return response
"""
Función para realizar el CSV correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request) y el porcentaje a filtrar en la sentencia SQL.
@return     descarga el archivo CSV con el nombre indicado por medio de una peticion request.
@author     Elmer Huiza
"""


def exportarEstudiantesPorcentaje(request, porcentaje):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="RT-EstudiantesPorPorcentaje.csv"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Estudiante por Porcentaje') 

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Porcentaje','Carnet', 'Nombre', 'Apellido', 'Carrera']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    estudios_universitarios = EstudioUniversitario.objects.all()
    estudios_universitarios=estudios_universitarios.filter(porc_carrerar_aprob__gte=porcentaje)

    for estudio in estudios_universitarios:
        row_num += 1
        row = [estudio.porc_carrerar_aprob,estudio.carnet_estudiante_id,estudio.carnet_estudiante.nombre_estudiante,estudio.carnet_estudiante.apellido_estudiante,estudio.codigo_carrera.nombre_carrera]
        
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response
"""
Función para recuperar y mostrar el listado de solictudes
@param      una solicitud de petición (request)
@return     retorna el template EstudiantesPorGenero.html con el diccionario detallado en la descripción.
@author     Elmer Huiza
"""
def listarSolicitudes(request):
    estudiantes = Solicitud.objects.all()
    
    return render(
        request,
        'proyecto/EstudiantesPorGenero.html',
        {'estudiantes':estudiantes}
    )

"""
Función para realizar el filtro correspondiente de los estudiantes por género.
@param      una solicitud de petición (request)
@return     retorna el template EstudiantesPorGenero con los estudiantes filtrados por género.
@author     Elmer Huiza
"""
def  consultaEstudiantesPorGenero(request):
    if request.method=='POST':
        sexo=request.POST['sexo']
        estudiantes=Solicitud.objects.filter(carnet_estudiante__carnet_estudiante__sexo_estudiante=sexo)
    
    return render(
        request,
        'proyecto/EstudiantesPorGenero.html',
        {'estudiantes':estudiantes,'sexo':sexo}
    )

"""Función para realizar el PDF correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request) y el sexo para filtrar en la sentencia SQL.
@return     retorna la vista previa del pdf por medio de una peticion request.
@author     Elmer Huiza
"""
def  reporteEstudiantesPorGenero(request,sexo):
    estudiantes=Solicitud.objects.filter(carnet_estudiante__carnet_estudiante__sexo_estudiante=sexo)

    template = get_template('reportes/ReporteGenero.html')
        
    context = {
        'estudiantes':estudiantes
    }
        
    html = template.render(context)
        
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="RT-EstudiantesPorGenero.pdf"'
        
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
        
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>'+ html + '</pre>')
        
    return response
"""
Función para realizar el CSV correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request) y el género filtrar en la sentencia SQL.
@return     descarga el archivo CSV con el nombre indicado por medio de una peticion request.
@author     Elmer Huiza
"""
def exportarEstudiantesPorGenero(request,sexo):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="RT-EstudiantesPorGenero.csv"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Estudiantes por Género') 

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Genero','Carnet', 'Nombre', 'Apellido', 'Modalidad','Fecha de inicio']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    estudiantes=Solicitud.objects.filter(carnet_estudiante__carnet_estudiante__sexo_estudiante=sexo)
    for estudiante in estudiantes:
        row_num += 1
        fecha_formato_inicio = datetime.strftime(estudiante.fecha_inicio, '%Y-%m-%d')
        row = [estudiante.carnet_estudiante.carnet_estudiante.sexo_estudiante,estudiante.carnet_estudiante_id,estudiante.carnet_estudiante.carnet_estudiante.nombre_estudiante,estudiante.carnet_estudiante.carnet_estudiante.apellido_estudiante,estudiante.modalidad,fecha_formato_inicio]
        
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

"""
Función para recuperar y mostrar el listado de servicios sociales 
@param      una solicitud de petición (request)
@return     retorna el template EstudiantesPorModalidad.html con el diccionario detallado en la descripción.
@author     Elmer Huiza
"""

def listarServicios(request):
    servicios = ServicioSocial.objects.all()
    return render(
        request,
        'proyecto/EstudiantesPorModalidad.html',
        {'servicios':servicios}
    )

"""
Función para realizar el filtro correspondiente de los estudiantes por modalidad.
@param      una solicitud de petición (request)
@return     retorna el template EstudiantesPorModalidad con los estudiantes filtrados por modalidad.
@author     Elmer Huiza
"""
def  consultaEstudiantesPorModalidad(request):
    modalidad = request.POST['modalidad']
    fecha = request.POST['fecha']
        
    # Se usa doble subrayado para que funcione como el "." en el template (osea un join)
    modalidad_filtro = ServicioSocial.objects.filter(carnet_estudiante__modalidad=modalidad)

    context = {
        'modalidad_filtro': modalidad_filtro,
        'fecha': fecha,
        'modalidad': modalidad,
    }

    return render(
        request,
        'proyecto/EstudiantesPorModalidad.html', 
        context,
    )

"""Función para realizar el PDF correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request) y el modalidad para filtrar en la sentencia SQL.
@return     retorna la vista previa del pdf por medio de una peticion request.
@author     Elmer Huiza
"""

def reporteEstudiantesPorModalidad(request, modalidad):

    servicios = ServicioSocial.objects.filter(carnet_estudiante__modalidad=modalidad)
    
    template = get_template('reportes/ReporteModalidad.html')

    context = {
        'servicios': servicios,
    }

    html = template.render(context)
    
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'inline; filename="RG-EstudiantesPorModalidad.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest = response, link_callback=link_callback)
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>'+ html + '</pre>')
    
    return response


"""Función para realizar el PDF correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request)   y los parametros modalidad y fecha  para filtrar en la sentencia SQL.
@return     retorna la vista previa del pdf por medio de una peticion request.
@author     Elmer Huiza
"""

def  reporteEstudiantesPorModalidadFecha(request, modalidad,fecha):
    servicios = ServicioSocial.objects.all()
    servicios = servicios.filter(carnet_estudiante__modalidad=modalidad).filter(carnet_estudiante__fecha_inicio__gte=fecha)

    template = get_template('reportes/ReporteModalidad.html')
        
    context = {
            'servicios':servicios,
        }
        
    html = template.render(context)
        
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="RG-EstudiantesPorModalidad.pdf"'
        
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
        
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>'+ html + '</pre>')
        
    return response

"""
Función para realizar el CSV correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request), la fecha y la modalidad a filtrar en la sentencia SQL.
@return     descarga el archivo CSV con el nombre indicado por medio de una peticion request.
@author     Elmer Huiza
"""
def exportarEstudiantesPorModalidadFecha(request, fecha, modalidad):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="RG-EstudiantesPorModalidad.csv"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Estudiantes por Modalidad') 

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Modalidad','Carnet', 'Nombre', 'Apellido', 'Proyecto','Fecha de inicio']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    estudiantes = ServicioSocial.objects.filter(carnet_estudiante__modalidad=modalidad).filter(carnet_estudiante__fecha_inicio__gte=fecha)

    for estudiante in estudiantes:
        row_num += 1
        fecha_formato_inicio = datetime.strftime(estudiante.carnet_estudiante.fecha_inicio, '%Y-%m-%d') 
        row = [estudiante.carnet_estudiante.modalidad,estudiante.carnet_estudiante_id,estudiante.carnet_estudiante.carnet_estudiante.carnet_estudiante.nombre_estudiante,estudiante.carnet_estudiante.carnet_estudiante.carnet_estudiante.apellido_estudiante,estudiante.codigo_proyecto_id,fecha_formato_inicio]
        
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

"""
Función para realizar el CSV correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request) y la modalidad  a filtrar en la sentencia SQL.
@return     descarga el archivo CSV con el nombre indicado por medio de una peticion request.
@author     Elmer Huiza
"""
def exportarEstudiantesPorModalidad(request,modalidad):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="RG-EstudiantesPorModalidad.csv"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Estudiantes por Modalidad') 

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Modalidad','Carnet', 'Nombre', 'Apellido', 'Proyecto','Fecha de inicio']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    estudiantes = ServicioSocial.objects.filter(carnet_estudiante__modalidad=modalidad)

    for estudiante in estudiantes:
        row_num += 1
        fecha_formato_inicio = datetime.strftime(estudiante.carnet_estudiante.fecha_inicio, '%Y-%m-%d')
        row = [estudiante.carnet_estudiante.modalidad,estudiante.carnet_estudiante_id,estudiante.carnet_estudiante.carnet_estudiante.carnet_estudiante.nombre_estudiante,estudiante.carnet_estudiante.carnet_estudiante.carnet_estudiante.apellido_estudiante,estudiante.codigo_proyecto_id,fecha_formato_inicio]
        
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response


#---------------------------------------------------------------------------------------------------------------

"""
Función para recuperar y mostrar el listado de todas las solicitudes aceptadas o denegadas 
para su selección y realización del filtro correspondiente y de la recuperación de todas las 
solicitudes por estado
@param      una solicitud de petición (request)
@return     retorna el template estudiantesSolicitudesAprobadas con el diccionario detallado en la descripción.
@author     Karla Abrego
"""
def consultaSolicitud(request):

    
    estado_solicitud=EstadoSolicitud.objects.order_by('carnet_estudiante')
    
    context = {
        
        'estado_solicitud':estado_solicitud,
    }

    return render(
        request,
        'proyecto/estudiantesSolicitudesAprobadas.html', context
    )

"""
Función para realizar el filtro correspondiente de las solicitudes por estado.
@param      una solicitud de petición (request)
@return     retorna el template estudiantesSolicitudesAprobadas con los proyectos filtrados por departamento.
@author     Karla Abrego
"""

def consultaEstudiantesSolicitudAprobada(request):
    if request.method == 'POST':
        estado = request.POST['estado']

        # Se usa doble subrayado para que funcione como el "." en el template (osea un join)
        estado_solicitud_filtro = EstadoSolicitud.objects.filter(aceptado = estado)
        context = {
            'estado_solicitud_filtro': estado_solicitud_filtro,
            'estado' : estado,
        }

        return render(
            request,
            'proyecto/estudiantesSolicitudesAprobadas.html', 
            context,
        )


"""
Función para realizar el PDF correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request) y el estado a filtrar en la sentencia SQL.
@return     retorna la vista previa del pdf por medio de una peticion request.
@author     Karla Abrego
"""

def reporteSolicitudAprobada(request, estado):

    estado_solicitud_filtro = EstadoSolicitud.objects.filter(aceptado = estado)

    template = get_template('reportes/ReporteSolicitudAprobada.html')

    context = {
        'estado_solicitud_filtro': estado_solicitud_filtro
    }

    html = template.render(context)
    
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'inline; filename="SolicitudesAprobadas.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest = response, link_callback=link_callback)
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>'+ html + '</pre>')
    
    return response

"""
Función para realizar el CSV correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request) y el departamento a filtrar en la sentencia SQL.
@return     descarga el archivo CSV con el nombre indicado por medio de una peticion request.
@author     Karla Abrego
"""   

def exportarEstudiantesSolicitudAprobada(request, estado):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="RT-SolicitudesAprobadas.csv"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Solicitudes Aprobadas') 

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Carnet', 'Nombre', 'Apellido', 'Estado', 'Observaciones']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    estado_solicitud_filtro = EstadoSolicitud.objects.filter(aceptado = estado)

    for estadoSol in  estado_solicitud_filtro:
        row_num += 1
        row = [estadoSol.carnet_estudiante_id,estadoSol.carnet_estudiante.carnet_estudiante.carnet_estudiante.nombre_estudiante,estadoSol.carnet_estudiante.carnet_estudiante.carnet_estudiante.apellido_estudiante,estadoSol.aceptado,estadoSol.observaciones]
        
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response


#---------------------------------------------------------------------------------------------------- 

"""
Función para recuperar y mostrar el listado de todos los estudiantes en servicio social 
para su selección y realización del filtro correspondiente y de la recuperación de todas los servicios social 
por periodo
@param      una solicitud de petición (request)
@return     retorna el template estudiantesServSocPeriodo con el diccionario detallado en la descripción.
@author     Karla Abrego
"""

def consultaEstudiantesPeriodo(request):


    consulta_periodo=Solicitud.objects.order_by('carnet_estudiante')
    
    context = {
        
        'consulta_periodo':consulta_periodo,
    }

    return render(
        request,
        'proyecto/estudiantesServSocPeriodo.html', context
    )

"""
Función para realizar el filtro correspondiente del servicio social por periodo.
@param      una solicitud de petición (request)
@return     retorna el template estudiantesServSocPeriodo con los proyectos filtrados por departamento.
@author     Karla Abrego
"""

def consultaEstudiantesServSocialPeriodo(request):
    if request.method == 'POST':
        # Se usa doble subrayado para que funcione como el "." en el template (osea un join)
        fecha_inicio = request.POST['fechaInicio']
        fecha_fin = request.POST['fechaFin']
        periodo_servicio_filtro = Solicitud.objects.order_by('fecha_inicio')

        print(periodo_servicio_filtro)
        print(fecha_inicio)
        print(fecha_fin)


        context = {
            'periodo_servicio_filtro': periodo_servicio_filtro,
            'fecha_inicio' : fecha_inicio,
            'fecha_fin' : fecha_fin,

        }

        return render(
            request,
            'proyecto/estudiantesServSocPeriodo.html', 
            context,
        )

"""
Función para realizar el PDF correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request) y el estado a filtrar en la sentencia SQL.
@return     retorna la vista previa del pdf por medio de una peticion request.
@author     Karla Abrego
"""        

def reporteEstudiantesServSocialPeriodo(request, fecha_inicio, fecha_fin):

    periodo_servicio_filtro = Solicitud.objects.order_by('fecha_inicio')
    

    template = get_template('reportes/ReporteServicioSocialPeriodo.html')

    context = {
        'periodo_servicio_filtro': periodo_servicio_filtro,
        'fecha_inicio' : fecha_inicio, 
        'fecha_fin' : fecha_fin,

    }

    html = template.render(context)
    
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'inline; filename="ServicioSocialPorPeriodo.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest = response, link_callback=link_callback)
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>'+ html + '</pre>')
    
    return response

"""
Función para realizar el CSV correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request) y el departamento a filtrar en la sentencia SQL.
@return     descarga el archivo CSV con el nombre indicado por medio de una peticion request.
@author     Karla Abrego
"""   

def exportarEstudiantesServSocialPeriodo(request, fecha_inicio, fecha_fin):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="RT-ServicioSocialPorPeriodo.csv"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Servicio Social Periodo ') 

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Carnet', 'Nombre', 'Apellido', 'Fecha Inicio', 'Fecha Fin']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    periodo_servicio_filtro = Solicitud.objects.order_by('fecha_inicio')
   
    
    for periodo in  periodo_servicio_filtro:


        fecha_formato_inicio = datetime.strftime(periodo.fecha_inicio, '%Y-%m-%d')  # trasformar
        fecha_formato_fin = datetime.strftime(periodo.fecha_fin, '%Y-%m-%d')  # trasformar

        fecha_formato_inicio_i = datetime.strftime(periodo.fecha_inicio, '%d-%m-%Y')  # trasformar
        fecha_formato_fin_i = datetime.strftime(periodo.fecha_fin, '%d-%m-%Y')  # trasformar

        if fecha_inicio <= fecha_formato_inicio and fecha_fin >= fecha_formato_inicio or fecha_inicio <= fecha_formato_fin and fecha_fin >= fecha_formato_fin :
            
            row_num += 1
            row = [periodo.carnet_estudiante_id,periodo.carnet_estudiante.carnet_estudiante.nombre_estudiante,periodo.carnet_estudiante.carnet_estudiante.apellido_estudiante,fecha_formato_inicio_i,fecha_formato_fin_i]
            print(row)
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response   

#---------------------------------------------------------------------------------------------------

"""
Función para recuperar y mostrar el listado de todos los estudiantes en servicio social 
para su selección y realización del filtro correspondiente y de la recuperación de todas los servicios social 
por periodo y carrera
@param      una solicitud de petición (request)
@return     retorna el template estudiantesServSocPeriodo con el diccionario detallado en la descripción.
@author     Karla Abrego
"""

def consultaEstudiantesCarrera(request):

    carreras = Carrera.objects.all()
    consulta_carrera=Solicitud.objects.order_by('carnet_estudiante')
    
    context = {
    
        'carreras': carreras,
        'consulta_carrera': consulta_carrera,
    }

    return render(
        request,
        'proyecto/estudiantesPorPeriodoCarrera.html', 
        context,
    )

"""
Función para realizar el filtro correspondiente del servicio social por periodo.
@param      una solicitud de petición (request)
@return     retorna el template estudiantesServSocPeriodo con los proyectos filtrados por carrera y periodo.
@author     Karla Abrego
"""

def consultaEstudiantesCarreraPeriodo(request):
    if request.method == 'POST':
        fecha = request.POST['fecha']
        carrera = request.POST['carrera']
        # Se usa doble subrayado para que funcione como el "." en el template (osea un join)
        carrera_periodo_filtro = Solicitud.objects.filter(carnet_estudiante__codigo_carrera__nombre_carrera = carrera)
        
        carreras = Carrera.objects.all()

        context = {

            'carrera_periodo_filtro' : carrera_periodo_filtro,
            'carreras': carreras,
            'carrera' : carrera,
            'fecha' : fecha,

        }

        return render(
            request,
            'proyecto/estudiantesPorPeriodoCarrera.html', 
            context,
        )

"""
Función para realizar el PDF correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request) y el estado a filtrar en la sentencia SQL.
@return     retorna la vista previa del pdf por medio de una peticion request.
@author     Karla Abrego
"""        
def reporteEstudianteCarreraPeriodo1(request, carrera):

    carrera_periodo_filtro = Solicitud.objects.filter(carnet_estudiante__codigo_carrera__nombre_carrera = carrera)
    fecha = ""
    carrera = carrera

    template = get_template('reportes/ReporteCarreraPeriodo.html')

    context = {
        
        'carrera_periodo_filtro' : carrera_periodo_filtro,
        'fecha' : fecha,
        'carrera': carrera,

    }

    html = template.render(context)
    
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'inline; filename="ServicioSocialCarreraPeriodo.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest = response, link_callback=link_callback)
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>'+ html + '</pre>')
    
    return response

"""
Función para realizar el PDF correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request) y el estado a filtrar en la sentencia SQL.
@return     retorna la vista previa del pdf por medio de una peticion request.
@author     Karla Abrego
"""  

def reporteEstudianteCarreraPeriodo2(request, fecha, carrera):

    carrera_periodo_filtro = Solicitud.objects.filter()
    fecha = fecha
    carrera = carrera

    template = get_template('reportes/ReporteCarreraPeriodo.html')

    context = {
        
        'carrera_periodo_filtro' : carrera_periodo_filtro,
        'fecha' : fecha,
        'carrera': carrera,

    }

    html = template.render(context)
    
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'inline; filename="ServicioSocialCarreraPeriodo.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest = response, link_callback=link_callback)
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>'+ html + '</pre>')
    
    return response

"""
Función para realizar el CSV correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request) y el departamento a filtrar en la sentencia SQL.
@return     descarga el archivo CSV con el nombre indicado por medio de una peticion request.
@author     Karla Abrego
"""   

def exportarEstudianteCarreraPeriodo1(request,carrera):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="RG-ServicioSocialCarreraPeriodo.csv"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Servicio Social Carrera ') 

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Carnet', 'Nombre', 'Apellido', 'Fecha Inicio', 'Fecha Final']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    carrera_periodo_filtro = Solicitud.objects.filter(carnet_estudiante__codigo_carrera__nombre_carrera = carrera)
    
    for periodo in  carrera_periodo_filtro:
        if periodo.carnet_estudiante.codigo_carrera.nombre_carrera == carrera:
            fecha_formato = datetime.strftime(periodo.fecha_inicio, '%Y-%m-%d')  # trasformar
            fecha_formato_fin = datetime.strftime(periodo.fecha_fin, '%Y-%m-%d')  # trasformar
            row_num += 1
            row = [periodo.carnet_estudiante_id,periodo.carnet_estudiante.carnet_estudiante.nombre_estudiante,periodo.carnet_estudiante.carnet_estudiante.apellido_estudiante,fecha_formato,fecha_formato_fin]
            print(row)

            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response   

"""
Función para realizar el CSV correspondiente con los datos recuperados a partir del filtro.
@param      una solicitud de petición (request) y el departamento a filtrar en la sentencia SQL.
@return     descarga el archivo CSV con el nombre indicado por medio de una peticion request.
@author     Karla Abrego
"""   
def exportarEstudianteCarreraPeriodo2(request,fecha,carrera):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="RG-ServicioSocialCarreraPeriodo.csv"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Servicio Social Carrera ') 

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Carnet', 'Nombre', 'Apellido', 'Fecha Inicio', 'Fecha Final']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    carrera_periodo_filtro = Solicitud.objects.filter(carnet_estudiante__codigo_carrera__nombre_carrera = carrera)
    
    for periodo in  carrera_periodo_filtro:
        if periodo.carnet_estudiante.codigo_carrera.nombre_carrera == carrera:
            fecha_formato = datetime.strftime(periodo.fecha_inicio, '%Y-%m-%d')  # trasformar
            fecha_formato_fin = datetime.strftime(periodo.fecha_fin, '%Y-%m-%d')  # trasformar
            if fecha <= fecha_formato and fecha <= fecha_formato_fin:
                row_num += 1
            row = [periodo.carnet_estudiante_id,periodo.carnet_estudiante.carnet_estudiante.nombre_estudiante,periodo.carnet_estudiante.carnet_estudiante.apellido_estudiante,fecha_formato,fecha_formato_fin]
            

            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response   



#---------------------------------------------------------------------------------------------------------------



def actualizarBD(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        
        if form.is_valid():
            archivo = request.FILES['docfile']

            handle_uploaded_file(archivo)
            
            #newdoc = Document(docfile = archivo)
            #newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse_lazy('sistemaGerencialAgro:actualizarBD'))
    
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'proyecto/actualizarBD.html',
        {
            'documents': documents, 
            'form': form
        }
    )


def handle_uploaded_file(f):
    filename = f.name

    if filename != 'dbRespaldo.sqlite3':
        filename = 'dbRespaldo.sqlite3'

    destination = open('media/respaldoDB/'+filename, 'wb+')

    for chunk in f.chunks(): 
        destination.write(chunk)

    destination.close()

#------------------------------------------------------------------------------

# proy = ServicioSocial.objects.raw('SELECT D.nombreDepartamento, C.nombre_carrera, P.descripcion_proyecto,  S.carnet_estudiante_id, E.nombre_estudiante FROM proyecto_serviciosocial SS'+
    # 'INNER JOIN proyecto_solicitud S ON SS.carnet_estudiante_id = S.carnet_estudiante_id'+
    # 'INNER JOIN proyecto_estudiouniversitario EU ON S.carnet_estudiante_id = EU.carnet_estudiante_id'+
    # 'INNER JOIN proyecto_estudiante E ON EU.carnet_estudiante_id = E.carnet_estudiante'+
    # 'INNER JOIN proyecto_carrera C ON EU.codigo_carrera_id = C.codigo_carrera'+
    # 'INNER JOIN proyecto_departamento D ON C.departamento_id = D.codigoDepartamento'+
    # 'INNER JOIN proyecto_proyecto P ON SS.codigo_proyecto_id = P.codigo_proyecto;')
