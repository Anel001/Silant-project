from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from .models import Machine, Reclamation, TO, Spravochnik
from .forms import TOForm, ReclamationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .filters import MachineFilter, MachineAroundFilter, TOFilter, ReclamationFilter
from django.contrib import messages


class InfoListView(ListView):
    model = Machine
    template_name = 'default.html'
    context_object_name = 'machines'
    queryset = Machine.objects.order_by('shipping_date')

    """В зависимости от группы пользователя создается queryset с определенными машинами"""
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name='Клиент').exists():
                self.filterset = MachineAroundFilter(self.request.GET, Machine.objects.filter(client=self.request.user.profile))
            elif self.request.user.groups.filter(name='Сервисная организация').exists():
                self.filterset = MachineAroundFilter(self.request.GET, Machine.objects.filter(service__name=self.request.user.profile.name))
            else:
                self.filterset = MachineAroundFilter(self.request.GET, queryset)
                print(queryset )
        else:
            self.filterset = MachineFilter(self.request.GET, queryset)

        return self.filterset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        machines = self.get_queryset()
        if machines.qs.count() == 1:
            context['is_set'] = True
        elif machines.qs.count() < 1:
            context['is_set'] = True
        else:
            context['is_set'] = False
        if self.request.user.groups.filter(name='Клиент').exists():
            context['is_client'] = True
            context['users_machines'] = self.get_queryset()
        else:
            context['is_client'] = False
            if self.request.user.groups.filter(name='Сервисная организация').exists():
                context['is_service'] = True
                context['users_machines'] = self.get_queryset()
            else:
                context['is_service'] = False
                context['users_machines'] = self.get_queryset()
        return context


class MachineDetailView(LoginRequiredMixin, DetailView):
    model = Machine
    template_name = 'machine.html'
    context_object_name = 'machine'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['to_list'] = TO.objects.filter(machine=self.get_object())
        context['reclam_list'] = Reclamation.objects.filter(machine=self.get_object())
        if self.request.user.groups.filter(name='Клиент').exists():
            context['is_client'] = True
        else:
            context['is_client'] = False
        return context


class TOListView(LoginRequiredMixin, ListView):
    model = TO
    template_name = 'to_list.html'
    context_object_name = 'maintenances'
    queryset = TO.objects.order_by('to_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        to_list = TOFilter(self.request.GET, queryset=self.get_queryset())
        context['filterset'] = to_list
        if self.request.user.groups.filter(name='Клиент').exists():
            context['is_client'] = True
            context['users_machines'] = users_machines = Machine.objects.filter(client=self.request.user.profile)

        else:
            context['is_client'] = False
            if self.request.user.groups.filter(name='Сервисная организация').exists():
                context['is_service'] = True
                context['users_machines'] = users_machines = Machine.objects.filter(service__name=self.request.user.profile.name)
            else:
                context['is_service'] = False
                context['users_machines'] = users_machines = Machine.objects.all()

        for to in to_list.qs:
            if to.machine in users_machines:
                context['is_exist'] = True
                break
            else:
                context['is_exist'] = False
        return context


class TOCreateView(LoginRequiredMixin, CreateView):
    model = TO
    template_name = 'to_create.html'
    form_class = TOForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('machine', kwargs={'pk': self.get_object().id})

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Machine.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machine'] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.machine = self.get_object()
        self.object.save()
        messages.success(self.request, "Запись о ТО успешно добавлена")
        return super().form_valid(form)


class TOUpdateView(LoginRequiredMixin, UpdateView):
    model = TO
    template_name = 'to_create.html'
    form_class = TOForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('machine', kwargs={'pk': self.get_object().machine.id})

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return TO.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machine'] = self.get_object().machine
        return context

    def form_valid(self, form):
        messages.success(self.request, "Запись о ТО успешно обновлена")
        return super().form_valid(form)


class TODeleteView(LoginRequiredMixin, DeleteView):
    model = TO
    context_object_name = 'to'
    template_name = 'to_delete.html'

    def get_success_url(self, **kwargs):
        messages.info(self.request, "Запись о ТО успешно удалена")
        return reverse_lazy('machine', kwargs={'pk': self.get_object().machine.id})

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return TO.objects.get(pk=id)


class ReclamationCreateView(PermissionRequiredMixin, CreateView):
    model = Reclamation
    template_name = 'reclam_create.html'
    form_class = ReclamationForm
    permission_required = ('base.add_reclamation',)

    def get_success_url(self, **kwargs):
        return reverse_lazy('machine', kwargs={'pk': self.get_object().id})

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Machine.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machine'] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.machine = self.get_object()
        self.object.service = Spravochnik.objects.get(name=self.request.user.profile.name)
        self.object.save()
        messages.success(self.request, "Запись о рекламации успешно добавлена")
        return super().form_valid(form)


class ReclamationUpdateView(PermissionRequiredMixin, UpdateView):
    model = Reclamation
    template_name = 'reclam_create.html'
    form_class = ReclamationForm
    permission_required = ('base.change_reclamation',)

    def get_success_url(self, **kwargs):
        return reverse_lazy('machine', kwargs={'pk': self.get_object().machine.id})

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Reclamation.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machine'] = self.get_object().machine
        return context

    def form_valid(self, form):
        messages.success(self.request, "Запись о рекламации успешно обновлена")
        return super().form_valid(form)


class ReclamationDeleteView(PermissionRequiredMixin, DeleteView):
    model = Reclamation
    context_object_name = 'reclam'
    template_name = 'rec_delete.html'
    permission_required = ('base.delete_reclamation',)

    def get_success_url(self, **kwargs):
        messages.info(self.request, "Запись о рекламации успешно удалена")
        return reverse_lazy('machine', kwargs={'pk': self.get_object().machine.id})

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Reclamation.objects.get(pk=id)


class ReclamationListView(LoginRequiredMixin, ListView):
    model = Reclamation
    template_name = 'reclams.html'
    context_object_name = 'reclamations'
    queryset = Reclamation.objects.order_by('fail_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reclam_list = ReclamationFilter(self.request.GET, queryset=self.get_queryset())
        context['filterset'] = reclam_list
        if self.request.user.groups.filter(name='Клиент').exists():
            context['is_client'] = True
            context['users_machines'] = users_machines = Machine.objects.filter(client=self.request.user.profile)
        else:
            context['is_client'] = False
            if self.request.user.groups.filter(name='Сервисная организация').exists():
                context['is_service'] = True
                context['users_machines'] = users_machines = Machine.objects.filter(service__name=self.request.user.profile.name)
            else:
                context['is_service'] = False
                context['users_machines'] = users_machines = Machine.objects.all()

        for reclam in reclam_list.qs:
            if reclam.machine in users_machines:
                context['is_exist'] = True
                break
            else:
                context['is_exist'] = False
        return context


class SpravochnikDetailView(LoginRequiredMixin, DetailView):
    model = Spravochnik
    template_name = 'sprav_detail.html'
    context_object_name = 'sprav'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sprav = self.get_object()
        context['type_name'] = sprav.get_type_name_display()
        return context


# Create your views here.
