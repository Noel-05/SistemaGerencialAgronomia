from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from apps.usuario.models import *

roles=[
    ('ADM', 'Administrador'),
    ('EST', 'Estudiante'),
    ('DOC', 'Profesor')
]

class UsuarioManager(BaseUserManager):
    def create_user(self, email,username,nombres, apellidos, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo electronico')

        user = self.model(
            username = username,
            email = self.normalize_email(email),
            nombres = nombres,    
            apellidos=apellidos,
        )
        
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,username,email,nombres,apellidos, password):
        user=self.create_user(
            email,
            username = username,
            nombres = nombres,
            apellidos=apellidos,
            password=password,
        )

        user.usuario_administrador= True
        user.save()
        return user


class Usuario(AbstractBaseUser):
    username = models.CharField('Nombre de usuario',unique = True, max_length=100)
    email = models.EmailField('Correo Electrónico', max_length=254,unique = True)
    nombres = models.CharField('Nombres', max_length=200, blank = True, null = True)
    apellidos = models.CharField('Apellidos', max_length=200,blank = True, null = True)
    imagen = models.ImageField('Imagen de Perfil', upload_to='perfil/', max_length=200,blank = True,null = True)
    is_active = models.BooleanField(default = True)
    usuario_administrador = models.BooleanField(default = False)
    rol=models.CharField(max_length=3,null=False, blank=False,choices=roles,default='EST')

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','nombres', 'apellidos']

    def __str__(self):
        return f'{self.nombres},{self.apellidos}'

    def save(self, *args, **kwargs):

        if self.usuario_administrador == True:
            self.rol = 'ADM'

        super().save(*args, **kwargs)

    def has_perm(self, perm,obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador