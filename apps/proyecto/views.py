from django.shortcuts import render
from django.shortcuts import redirect
from django.core import serializers
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import *
import xlwt

#------------------------------------------------------------------------------


"""
Función para mostrar la página de inicio del sistema
@param      una solicitud de petición (request)
@return     retorna el template base del sistema
@author     Noel Renderos
"""

def index(request):
    return render(
        request,
        'base/base.html',
    )


#------------------------------------------------------------------------------


# ESTA VISTA SOLO ES PARA QUE FUNCIONE EL EJEMPLO, LUEGO SE BORRARA

def consultaEstudiante(request):

    estudiante_list=Estudiante.objects.order_by('carnet_estudiante')
    
    context = {
        'estudiante_list': estudiante_list,
    }

    return render(
        request,
        'proyecto/EjemploConsulta.html', context
    )

#------------------------------------------------------------------------------

class reportesEstudiantesPorcentajeCarrera(TemplateView):
    template_name='proyecto/EstudiantesPorcentajeCarrera.html'
    def post(self,request,*args,**kwargs):
        porcentaje=request.POST['porcentaje']
        estudios_universitarios=EstudioUniversitario.objects.filter(porc_carrerar_aprob=porcentaje)
        return render(request,'proyecto/EstudiantesPorcentajeCarrera.html',{'estudios_universitarios':estudios_universitarios})

class reportesEstudiantesPorGenero(TemplateView):
    template_name='proyecto/EstudiantesPorGenero.html'
    def post(self,request,*args,**kwargs):
        sexo=request.POST['sexo']
        estudiantes=Solicitud.objects.filter(carnet_estudiante__carnet_estudiante__sexo_estudiante=sexo)
        return render(request,'proyecto/EstudiantesPorGenero.html',{'estudiantes':estudiantes})

class reportesEstudiantesPorModalidad(TemplateView):
    template_name='proyecto/EstudiantesPorModalidad.html'
    def post(self,request,*args,**kwargs):
        modalidad=request.POST['modalidad']
        solicitudes=Solicitud.objects.filter(modalidad=modalidad)
        return render(request,'proyecto/EstudiantesPorModalidad.html',{'solicitudes':solicitudes})

def export_estudiantes_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Datos de estudiantes') 

    
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Carnet', 'Nombre', 'Apellido']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Estudiante.objects.all().values_list('carnet_estudiante', 'nombre_estudiante', 'apellido_estudiante')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response