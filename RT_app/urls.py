from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', views.dashboard, name='dashboard'),
    path('admin/infra', views.infra, name='infra')
]