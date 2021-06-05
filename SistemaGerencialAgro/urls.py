"""SistemaGerencialAgro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy, path, include
from .forms import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.proyecto.urls')),
    path('',include('apps.usuario.urls')),    
    path('accounts/', include('django.contrib.auth.urls')),
    
    #1 Form para enviar Email
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="reset_password"),

    #2 Mensaje de Envio de Correo Electronico
    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    #3 Enlace al correo de Reseteo de contraseña y formulario de reseteo
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html", form_class=FormularioContraOlvidada), 
        name="password_reset_confirm"),

    #4 Mensaje de Reseteo de contraseña exitosa   
    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),

    #5 Formulario de cambio de contraseña   
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html', form_class=FormularioCambioContraseña), 
        name='password_change'),

    #6 Mensaje de que la contraseña se ha reseteado correctamente    
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), 
        name='password_change_done'),
]

'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Reset form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
5 - Password change                           //PasswordChangeDoneView.as_view()
'''