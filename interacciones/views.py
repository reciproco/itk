from django.shortcuts import render
from interacciones.models import Itk, Rel_Itk_Far, Farmaco
from django.db.models import Q
from interacciones.forms import ItksForm


# Create your views here.
def prueba(request):

    # itk = Itk.objects.get(nombre='Imatinib')
    rel = Rel_Itk_Far.objects.all().filter(Q(itk__nombre='Dasatinib') |
                                           Q(itk__nombre='Imatinib'))
    for i in rel:
        print(i.efecto)
    return render(request, 'interacciones/prueba.html', locals())


def home(request):
    form = ItksForm()
    if request.method == 'POST':
        form = ItksForm(request.POST)
        if form.is_valid():
            selected_itks = form.cleaned_data['itks']
            farmacos = Farmaco.objects.all()
            return render(request, 'interacciones/farmacos.html', locals())

    return render(request, 'interacciones/index.html', locals())
