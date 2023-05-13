from django.shortcuts import render, get_object_or_404, redirect
from RT_app.models import Machine, Entretien, Personnel, Infrastructure
from django.db.models import Count
from .forms import AddInfraForm, DeleteInfraForm, AddEntretienForm, DeleteEntretienForm
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.

infrastructures = Infrastructure.objects.all()
entretiens = Entretien.objects.all()
personnels = Personnel.objects.all()
machines = Machine.objects.all()

# La vue index renvoie une réponse HTTP avec un contexte vide
def index(request):
    context = {}
    return render(request, 'index.html', context)


# La vue dashboard affiche un tableau de bord avec des statistiques sur les machines et les entretiens
def dashboard(request):
    machine_sum = machines.count()
    entretien_a_faire = entretiens.filter(etat=True)
    entretien_par_type = entretien_a_faire.values('type').annotate(count=Count('type'))

    context = {
        'infrastructures': infrastructures,
        'entretiens': entretiens,
        'personnels': personnels,
        'machines': machines,
        'machine_sum': machine_sum,
        'entretien_a_faire': entretien_a_faire,
        'entretien_par_type': entretien_par_type,
    }
    return render(request, 'admin/dashboard.html', context)


# La vue infra affiche la liste des infrastructures avec des formulaires pour ajouter et supprimer des éléments
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


# La vue machine_detail_view affiche les détails d'une machine spécifique
def machine_detail_view(request, pk):
    machine_seule = get_object_or_404(Machine, id=pk)
    context = {'machine': machine_seule}
    return render(request, 'admin/machine_detail.html', context)


# La vue delete_machine_view supprime une machine spécifique et redirige l'utilisateur vers la page d'infrastructures
def delete_machine_view(request, pk):
    machine_seule = get_object_or_404(Machine, id=pk)
    machine_seule.delete()
    return redirect(reverse('infra'))



def taches(request):
    # Récupérer les entretiens à faire qui sont actuellement en cours
    entretien_a_faire = entretiens.filter(etat=True)

    # Grouper les entretiens à faire par type et compter leur nombre
    entretien_par_type = entretien_a_faire.values('type').annotate(count=Count('type'))

    # Récupérer les machines qui nécessitent un entretien par type d'entretien
    machines_entretien = []
    for entretien_type in entretien_par_type:
        machines = Machine.objects.filter(entretien__type=entretien_type['type'])
        machines_entretien.append({'type': entretien_type['type'], 'machines': machines})

    # Initialiser les formulaires pour ajouter et supprimer des entretiens
    addEntretienForm = AddEntretienForm()
    deleteEntretienForm = DeleteEntretienForm()
    submitted_add = False
    submitted_delete = False

    # Traiter les soumissions de formulaires
    if request.method == 'POST':
        print(request.POST)
        if 'add_entretien_form' in request.POST:
            # Traiter la soumission du formulaire d'ajout d'un entretien
            addEntretienForm = AddEntretienForm(request.POST)
            if addEntretienForm.is_valid():
                addEntretienForm.save()
                submitted_add = True
                addEntretienForm = AddEntretienForm()
        elif 'delete_entretien_form' in request.POST:
            # Traiter la soumission du formulaire de suppression d'un entretien
            deleteEntretienForm = DeleteEntretienForm(request.POST)
            if deleteEntretienForm.is_valid():
                nom_entretien_id = deleteEntretienForm.cleaned_data['nom']
                nom_entretien = Entretien.objects.get(pk=nom_entretien_id)
                nom_entretien.etat = False 
                nom_entretien.save() 
                submitted_delete = True
                deleteEntretienForm = DeleteEntretienForm()

    context = {
        'infrastructures' : infrastructures,
        'entretiens' : entretiens,
        'personnels' : personnels,
        'entretien_a_faire' : entretien_a_faire,
        'entretien_par_type': entretien_par_type,
        'machines_entretien' : machines_entretien,
        'addEntretienForm': addEntretienForm,
        'deleteEntretienForm': deleteEntretienForm,
        'submitted_add': submitted_add,
        'submitted_delete': submitted_delete,
    }

    return render(request, 'admin/taches.html', context)

