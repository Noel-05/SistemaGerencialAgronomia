import json
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.serializers import serialize
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView,TemplateView
from apps.usuario.models import Usuario
from apps.usuario.forms import FormularioLogin, FormularioUsuario, FormularioUsuarioEditar, FormularioUsuarioLogin
from apps.usuario.mixins import LoginPEAMixin, LoginPAMixin, LoginEAMixin, LoginAMixin

from apps.proyecto import *

def index(request):
    return render(
        request,
        'base/base.html',
    )

"""
Clase para el Login del Sistema.
@param      el formulario por defecto de Django
@return     retorna el template login.
@author     Roberto Paz
"""
class Login(FormView):
    template_name = 'usuario/login1.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('usuario:index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)

"""
Funcion para cerrar sesion del Sistema.
@param      una solicitud de petición (request)
@return     retorna al template login.
@author     Roberto Paz
"""

def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('usuario:login'))  

"""
Clase para redirigir a la lista de los usuarios.
@param      el TemplateView por defecto de Django
@return     retorna a la plantilla de listar_usuario.
@author     Roberto Paz
"""
class InicioListadoUsuario(LoginPAMixin, TemplateView):
    template_name='usuario/listar_usuario.html'

"""
Clase para listar los usuarios del sistema.
@param      el ListView por defecto de Django
@return     retorna la lista de los usuarios del sistema.
@author     Roberto Paz
"""
class ListadoUsuario(LoginAMixin, ListView):
    model=Usuario

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)  

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('usuario:inicio_usuarios')

"""
Clase para registrar los usuarios en el sistema.
@param      el CreateView por defecto de Django
@return     retorna a la lista de los usuarios del sistema, con el usuario creado.
@author     Roberto Paz
"""

class RegistrarUsuario(LoginAMixin, CreateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'usuario/crear_usuario_modal.html'

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                nuevo_usuario = Usuario(
                    email=form.cleaned_data.get('email'),
                    username=form.cleaned_data.get('username'),
                    nombres=form.cleaned_data.get('nombres'),
                    apellidos=form.cleaned_data.get('apellidos'),
                    rol=form.cleaned_data.get('rol'),
                )
                nuevo_usuario.set_password(form.cleaned_data.get('password1'))
                nuevo_usuario.save()
                mensaje = f'{self.model.__name__} registrado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('usuario:inicio_usuarios')

class RegistrarUsuarioLogin(CreateView):
    model=Usuario
    form_class=FormularioUsuarioLogin
    template_name='usuario/crear_usuario_login.html'

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            nuevo_usuario=Usuario(
                email=form.cleaned_data.get('email'),
                username=form.cleaned_data.get('username'),
                nombres=form.cleaned_data.get('nombres'),
                apellidos=form.cleaned_data.get('apellidos'),
            )
            nuevo_usuario.set_password(form.cleaned_data.get('password1'))
            nuevo_usuario.save()

            login(request, nuevo_usuario)
            return HttpResponseRedirect(reverse_lazy('usuario:index'))
        else:
            return render(request, self.template_name,{'form':form})

"""
Clase para Editar los usuarios registrados en el sistema.
@param      el UpdateView por defecto de Django
@return     retorna a la lista de los usuarios del sistema, con los cambios realizados al 
usuario seleccionado.
@author     Roberto Paz
"""

class EditarUsuario(LoginAMixin, UpdateView):
    model = Usuario
    form_class = FormularioUsuarioEditar
    template_name = 'usuario/editar_usuario_modal.html'


    def post(self,request,*args,**kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST,instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} actualizado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido actualizar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('usuario:inicio_usuarios')

"""
Clase para Eliminar un usuario del sistema.
@param      el DeleteView por defecto de Django
@return     retorna a la lista de los usuarios del sistema.
@author     Roberto Paz
"""

class EliminarUsuario(LoginAMixin, DeleteView):
    model = Usuario
    template_name = 'usuario/eliminar_usuario_modal.html'

    def delete(self,request,*args,**kwargs):
        if request.is_ajax():
            usuario = self.get_object()
            usuario.delete()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('usuario:inicio_usuarios')