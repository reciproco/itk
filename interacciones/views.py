from django.shortcuts import render
from interacciones.models import Itk


# Create your views here.
def prueba(request):

    itk = Itk.objects.get(nombre='Imatinib')

    for i in itk.itks.all():
        print(i.recomendacion)
    return render(request, 'interacciones/prueba.html', locals())
