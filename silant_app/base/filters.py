from django_filters import FilterSet
from django_filters.filters import ModelChoiceFilter
from .models import Machine, TO, Reclamation, Spravochnik
from django.contrib.auth.models import User


"""Фильтр для поиска нужных машин"""


class MachineFilter(FilterSet):
    class Meta:
        model = Machine
        fields = ['number']


class MachineAroundFilter(FilterSet):
    class Meta:
        model = Machine
        fields = ['tech_model', 'eng_model', 'tran_model', 'drive_axle', 'steer_axle']


class TOFilter(FilterSet):
    class Meta:
        model = TO
        fields = ['type', 'machine', 'service']


class ReclamationFilter(FilterSet):
    class Meta:
        model = Reclamation
        fields = ['fail_node', 'recovery', 'service']