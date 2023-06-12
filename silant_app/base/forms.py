from django import forms
from django.forms import Textarea
from .models import Machine, Reclamation, TO, Spravochnik
from django.forms.widgets import DateInput


class TOForm(forms.ModelForm):
    to_date = forms.DateField(
        label='Дата проведения ТО',
        widget=DateInput(attrs= {'type': 'date'}))
    order_date = forms.DateField(
        label='Дата заказ-наряда',
        widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = TO
        fields = [
            'type',
            'to_date',
            'operating',
            'order_num',
            'order_date',
            'service',
        ]


class ReclamationForm(forms.ModelForm):
    fail_date = forms.DateField(
        label='Дата отказа',
        widget=DateInput(attrs={'type': 'date'}))
    recovery_date = forms.DateField(
        label='Дата восстановления',
        widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Reclamation
        fields = [
            'fail_date',
            'operating',
            'fail_node',
            'fail_descrip',
            'recovery',
            'parts',
            'recovery_date',
        ]
