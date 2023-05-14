from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', views.dashboard, name='dashboard'),
    path('admin/infra', views.infra, name='infra'),
    path('admin/taches', views.taches, name='taches'),
    path('admin/taches_historique', views.taches_historique, name='taches_historique'),
    path('admin/machine-<pk>',views.machine_detail_view ,name='machine-detail'),
    path('machine/<int:pk>/delete/', views.delete_machine_view, name='machine-delete'),
    
]