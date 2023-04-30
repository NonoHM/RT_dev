from django.shortcuts import render
from RT_app.models import machine, entretien, personnel,infrastructure

# Create your views here.

infrastructures = infrastructure.objects.all()
entretiens = entretien.objects.all()
personnels = personnel.objects.all()
machines = machine.objects.all()

def index(request) :
    context = {}
    return render(request, 'index.html', context)

def dashboard(request) :
    machine_sum = machines.count()
    context = {
        'infrastructures' : infrastructures,
        'entretiens' : entretiens,
        'personnels' : personnels,
        'machines' : machines,
        'machine_sum' : machine_sum,
    }
    return render(request, 'admin/dashboard.html', context)

def infra(request) :
    context = {}
    return render(request, 'admin/infra.html', context)

