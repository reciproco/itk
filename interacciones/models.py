from django.db import models


# Create your models here.
class Itk(models.Model):
    nombre = models.CharField(max_length=24)


class Grupo(models.Model):
    descripcion = models.CharField(max_length=256)


class Farmaco(models.Model):
    nombre = models.CharField(max_length=128)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)


class Rel_Itk_Far(models.Model):
    itk = models.ForeignKey(Itk, on_delete=models.CASCADE, related_name='itk')
    farmaco = models.ForeignKey(Farmaco, on_delete=models.CASCADE,
                                related_name='farmacos')
    clasificacion = models.CharField(max_length=128)
    efecto = models.CharField(max_length=128)
    mecanismo = models.CharField(max_length=128)
    recomendacion = models.CharField(max_length=128)


class Bibliografia(models.Model):
    descripcion = models.CharField(max_length=1024)


class Rel_Biblio_Rel(models.Model):
    rel_itk_far = models.ForeignKey(Rel_Itk_Far, on_delete=models.CASCADE)
    bibliografia = models.ForeignKey(Bibliografia, on_delete=models.CASCADE)
