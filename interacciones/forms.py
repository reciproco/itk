from django import forms
from interacciones.models import Itk


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.nombre


class ItksForm(forms.Form):
    itks = CustomModelMultipleChoiceField(queryset=Itk.objects.all())
