from django.urls import path
from .views import InfoListView, TOListView, ReclamationListView, MachineDetailView, TOCreateView, ReclamationCreateView, \
    TOUpdateView, ReclamationUpdateView, TODeleteView, ReclamationDeleteView, SpravochnikDetailView

urlpatterns = [
    path('', InfoListView.as_view(), name='base'),
    path('<int:pk>/', MachineDetailView.as_view(), name='machine'),
    path('<int:pk>/add/to', TOCreateView.as_view(), name='to_create'),
    path('update/to/<int:pk>', TOUpdateView.as_view(), name='to_update'),
    path('delete/to/<int:pk>', TODeleteView.as_view(), name='to_delete'),
    path('<int:pk>/add/reclamation', ReclamationCreateView.as_view(), name='reclam_create'),
    path('update/reclamation/<int:pk>', ReclamationUpdateView.as_view(), name='reclam_update'),
    path('delete/reclamation/<int:pk>', ReclamationDeleteView.as_view(), name='reclam_delete'),
    path('maintenance/', TOListView.as_view(), name='main'),
    path('reclamations/', ReclamationListView.as_view(), name='reclamation'),
    path('spravochnik/<int:pk>', SpravochnikDetailView.as_view(), name='sprav'),
]
