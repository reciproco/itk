from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, nombre, apellidos, provincia,
                    localidad, centro_de_trabajo, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            nombre=nombre,
            apellidos=apellidos,
            provincia=provincia,
            localidad=localidad,
            centro_de_trabajo=centro_de_trabajo,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, apellidos, provincia,
                         localidad, centro_de_trabajo, password):
        user = self.create_user(
            email,
            nombre=nombre,
            apellidos=apellidos,
            provincia=provincia,
            localidad=localidad,
            centro_de_trabajo=centro_de_trabajo,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    nombre = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=40)
    provincia = models.CharField(max_length=20)
    localidad = models.CharField(max_length=20)
    centro_de_trabajo = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellidos', 'provincia', 'localidad']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, primary_key=True)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
