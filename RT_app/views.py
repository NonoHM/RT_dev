from django.shortcuts import render, get_object_or_404, redirect
from RT_app.models import Machine, Entretien, Personnel, Infrastructure
from django.db.models import Count
from .forms import AddInfraForm, DeleteInfraForm, AddEntretienForm
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.

infrastructures = Infrastructure.objects.all()
entretiens = Entretien.objects.all()
personnels = Personnel.objects.all()
machines = Machine.objects.all()

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

def infra(request):
    infrastructures = Infrastructure.objects.all()
    addInfraForm = AddInfraForm()
    deleteInfraForm = DeleteInfraForm()
    submitted_add = False
    submitted_delete = False

    if request.method == 'POST':
        if 'add_infra_form' in request.POST:
            addInfraForm = AddInfraForm(request.POST)
            if addInfraForm.is_valid():
                addInfraForm.save()
                submitted_add = True
                addInfraForm = AddInfraForm()
        elif 'delete_infra_form' in request.POST:
            deleteInfraForm = DeleteInfraForm(request.POST)
            if deleteInfraForm.is_valid():
                infrastructure = deleteInfraForm.cleaned_data['nom']
                infrastructure.delete()
                submitted_delete = True
                deleteInfraForm = DeleteInfraForm()
        

    context = {
        'infrastructures': infrastructures,
        'addInfraForm': addInfraForm,
        'deleteInfraForm': deleteInfraForm,
        'submitted_add': submitted_add,
        'submitted_delete': submitted_delete,
    }
    return render(request, 'admin/infra.html', context)



def machine_detail_view(request, pk):
    machine_seule = get_object_or_404(Machine, id=pk)
    context = { 'machine': machine_seule }
    return render(request, 'admin/machine_detail.html', context)

def delete_machine_view(request, pk):
    machine_seule = get_object_or_404(Machine, id=pk)
    machine_seule.delete()
    return redirect(reverse('infra'))


def taches(request):
    entretien_a_faire = entretiens.filter(etat=True)
    entretien_par_type = entretien_a_faire.values('type').annotate(count=Count('type'))
    machines_entretien = []
    for entretien_type in entretien_par_type:
        machines = Machine.objects.filter(entretien__type=entretien_type['type'])
        machines_entretien.append({'type': entretien_type['type'], 'machines': machines})

    addEntretienForm = AddEntretienForm()
    submitted_add = False
    submitted_delete = False

    if request.method == 'POST':
        if 'add_tache_form' in request.POST:
            addEntretienForm = AddEntretienForm(request.POST)
            if addEntretienForm.is_valid():
                addEntretienForm.save()
                submitted_add = True
                addEntretienForm = AddEntretienForm()
        # elif 'delete_tache_form' in request.POST:
        #     deleteTacheForm = DeleteTacheForm(request.POST)
        #     if deleteTacheForm.is_valid():
        #         tache = deleteTacheForm.cleaned_data['nom']
        #         tache.delete()
        #         submitted_delete = True
        #         deleteTacheForm = DeleteTacheForm()

    context = {
        'infrastructures' : infrastructures,
        'entretiens' : entretiens,
        'personnels' : personnels,
        'entretien_a_faire' : entretien_a_faire,
        'entretien_par_type': entretien_par_type,
        'machines_entretien' : machines_entretien,
    }
    return render(request, 'admin/taches.html', context)
