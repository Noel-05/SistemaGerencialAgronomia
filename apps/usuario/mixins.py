from django.shortcuts import redirect
from django.contrib import messages

# Mixin Estudiante, Profesor y Administrador
class LoginPEAMixin(object):

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.rol == 'DOC' or request.user.rol == 'EST' or request.user.rol == 'ADM':
				return super().dispatch(request, *args, **kwargs)
			messages.error(request, 'No tienes permisos para realizar esta acción.')
		return redirect('usuario:index')

# Mixin Profesor y Administrador
class LoginPAMixin(object):

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.rol == 'DOC' or request.user.rol == 'ADM':
				return super().dispatch(request, *args, **kwargs)
			messages.error(request, 'No tienes permisos para realizar esta acción.')
		return redirect('usuario:index')

# Mixin Estudiante y Administrador
class LoginEAMixin(object):

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.rol == 'EST' or request.user.rol == 'ADM':
				return super().dispatch(request, *args, **kwargs)
			messages.error(request, 'No tienes permisos para realizar esta acción.')
		return redirect('usuario:index')

# Mixin Administrador
class LoginAMixin(object):

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.rol == 'ADM':
				return super().dispatch(request, *args, **kwargs)
			messages.error(request, 'No tienes permisos para realizar esta acción.')
		return redirect('usuario:index')