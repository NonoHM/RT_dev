from django.shortcuts import render
from RT_app.models import machine, entretien, personnel,infrastructure
from django.db.models import Count

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
    entretien_a_faire = entretiens.filter(etat=True)
    entretien_par_type = entretien_a_faire.values('type').annotate(count=Count('type'))
    context = {
        'infrastructures' : infrastructures,
        'entretiens' : entretiens,
        'personnels' : personnels,
        'machines' : machines,
        'machine_sum' : machine_sum,
        'entretien_a_faire' : entretien_a_faire,
        'entretien_par_type': entretien_par_type,
    }
    return render(request, 'admin/dashboard.html', context)

def infra(request) :
    context = {}
    return render(request, 'admin/infra.html', context)

