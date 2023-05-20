from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout'),
    path('admin/', views.dashboard, name='dashboard'),
    path('admin/infra', views.infra, name='infra'),
    path('admin/entretiens', views.taches, name='taches'),
    path('admin/entretiens-historique', views.taches_historique, name='taches_historique'),
    path('admin/machine-<pk>',views.machine_detail_view ,name='machine-detail'),
    path('admin/machine/<int:pk>/delete/', views.delete_machine_view, name='machine-delete'),
    path('admin/entretien-<pk>',views.entretien_detail_view ,name='entretien-detail'),
    path('admin/create-user',views.create_user,name='create-user'),
]