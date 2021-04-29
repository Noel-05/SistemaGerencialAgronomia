from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings



class Departamento(models.Model):
    codigoDepartamento = models.CharField(primary_key=True, max_length=10, null=False)
    nombreDepartamento = models.CharField(max_length=100, null=False)
    nombreJefeDepartamento = models.CharField(max_length=50, null=False)
    apellidoJefeDepartamento = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nombreDepartamento



class Carrera(models.Model):
    codigo_carrera = models.CharField(primary_key=True, max_length=10, null=False)
    nombre_carrera = models.CharField(max_length=100, null=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_carrera



class Estudiante(models.Model):
    carnet_estudiante = models.CharField(primary_key=True, max_length=7, null=False)
    nombre_estudiante = models.CharField(max_length=50, null=False)
    apellido_estudiante = models.CharField(max_length=50, null=False)
    sexo_estudiante = models.CharField(max_length=1, null=False)
    telefono_estudiante = models.IntegerField(null=False)
    correo_estudiante = models.CharField(max_length=100, null=False)
    direccion_estudiante = models.CharField(max_length=250, null=False)

    def __str__(self):
        return self.carnet_estudiante



class EstudioUniversitario(models.Model):
    carnet_estudiante = models.OneToOneField(Estudiante, primary_key=True, unique=True, on_delete = models.CASCADE)
    codigo_carrera = models.ForeignKey(Carrera, on_delete = models.CASCADE)
    codigo_ciclo = models.IntegerField(null=False)
    porc_carrerar_aprob = models.IntegerField(null=False)
    unidades_valorativas = models.IntegerField(null=False)
    experiencia_areas_conoc = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.carnet_estudiante.__str__()



class Solicitud(models.Model):
    carnet_estudiante = models.OneToOneField(EstudioUniversitario, unique=True, primary_key=True, on_delete = models.CASCADE)
    codigo_entidad = models.CharField(max_length=10, null=False)
    horas_semana = models.IntegerField(null=False)
    dias_semana = models.IntegerField(null=False)
    modalidad = models.CharField(max_length=30, null=False)
    fecha_inicio = models.DateField(null=False)
    fecha_fin = models.DateField(null=True)

    def __str__(self):
        return self.carnet_estudiante.__str__()   



class EstadoSolicitud(models.Model):
    carnet_estudiante = models.OneToOneField(Solicitud, unique=True, primary_key=True, on_delete = models.CASCADE)
    aceptado = models.CharField(max_length=30, null=False)
    motivo = models.CharField(max_length=200, null=True, blank=True)
    observaciones = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.carnet_estudiante.__str__() 



class Docente(models.Model):
    carnet_docente = models.CharField(primary_key=True, max_length=10, null=False)
    nombre_docente = models.CharField(max_length=50, null=False)
    apellido_docente = models.CharField(max_length=50, null=False)
    nombre_rol = models.CharField(max_length=25, null=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return self.carnet_docente.__str__() +' '+ self.nombre_docente.__str__()
        


class Proyecto(models.Model):
    codigo_proyecto = models.CharField(primary_key=True, max_length=10, null=False)
    descripcion_proyecto = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.codigo_proyecto.__str__() +' '+ self.descripcion_proyecto.__str__()



class ServicioSocial(models.Model):
    carnet_estudiante = models.OneToOneField(Solicitud, primary_key=True, unique=True, on_delete=models.CASCADE)
    carnet_docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    codigo_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

    def __str__(self):
        return self.carnet_estudiante.__str__()