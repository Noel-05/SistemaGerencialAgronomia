from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django import forms
import re

class FormularioContraOlvidada(SetPasswordForm):
	new_password1=forms.CharField(label='Contraseña', widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder':'Ingrese su Nueva Contraseña',
			'id': 'new_password1',
			'required':'required',
		}
	))

	new_password2=forms.CharField(label='Contraseña de Confirmacion', widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder':'Ingrese nuevamente su Contraseña',
			'id': 'new_password2',
			'required':'required',
		}
	))

	def clean_new_password2(self):

		print(self.cleaned_data)
		new_password1=self.cleaned_data.get('new_password1')
		new_password2=self.cleaned_data.get('new_password2')
		if new_password1 != new_password2:
			raise forms.ValidationError('Contraseñas no coinciden')
		if not 8 <= len(new_password2) <= 20:
			raise forms.ValidationError('Su contraseña debe de contener entre 8 y 20 caracteres')						
		if not(re.search('[a-z]', new_password2) and re.search('[A-Z]', new_password2)):
			raise forms.ValidationError('Su contraseña debe de contener al menos una letra mayúscula y una minúscula, un número, un carácter especial, y contener entre 8 y 20 caracteres')
		if not(re.search('[0-9]', new_password2)):
			raise forms.ValidationError('Su contraseña debe de contener al menos una letra mayúscula y una minúscula, un número, un carácter especial, y contener entre 8 y 20 caracteres')
		if not(re.search('[@$%&/=?(¿¡!_.,>)<*]', new_password2)):
			raise forms.ValidationError('Su contraseña debe de contener al menos una letra mayúscula y una minúscula, un número, un carácter especial, y contener entre 8 y 20 caracteres')
		return new_password2

class FormularioCambioContraseña(PasswordChangeForm):
	new_password1=forms.CharField(label='Contraseña', widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder':'Ingrese su Nueva Contraseña',
			'id': 'new_password1',
			'required':'required',
		}
	))

	new_password2=forms.CharField(label='Contraseña de Confirmacion', widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder':'Ingrese nuevamente su Contraseña',
			'id': 'new_password2',
			'required':'required',
		}
	))

	def clean_new_password2(self):

		print(self.cleaned_data)
		new_password1=self.cleaned_data.get('new_password1')
		new_password2=self.cleaned_data.get('new_password2')
		if new_password1 != new_password2:
			raise forms.ValidationError('Contraseñas no coinciden')
		if not 8 <= len(new_password2) <= 20:
			raise forms.ValidationError('Su contraseña debe de contener entre 8 y 20 caracteres')						
		if not(re.search('[a-z]', new_password2) and re.search('[A-Z]', new_password2)):
			raise forms.ValidationError('Su contraseña debe de contener al menos una letra mayúscula y una minúscula, un número, un carácter especial, y contener entre 8 y 20 caracteres')
		if not(re.search('[0-9]', new_password2)):
			raise forms.ValidationError('Su contraseña debe de contener al menos una letra mayúscula y una minúscula, un número, un carácter especial, y contener entre 8 y 20 caracteres')
		if not(re.search('[@$%&/=?(¿¡!_.,>)<*]', new_password2)):
			raise forms.ValidationError('Su contraseña debe de contener al menos una letra mayúscula y una minúscula, un número, un carácter especial, y contener entre 8 y 20 caracteres')
		return new_password2
