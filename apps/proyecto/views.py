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

from .models import *


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
