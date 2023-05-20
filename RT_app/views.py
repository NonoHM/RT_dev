from django.shortcuts import render, get_object_or_404, redirect
from RT_app.models import Machine, Entretien, Personnel, Infrastructure
from django.db.models import Count
from .forms import AddInfraForm, DeleteInfraForm, AddEntretienForm, DeleteEntretienForm, AddMachineForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.

infrastructures = Infrastructure.objects.all()
entretiens = Entretien.objects.all()
personnels = Personnel.objects.all()
machines = Machine.objects.all()

# La vue index renvoie une réponse HTTP avec un contexte vide
def index(request):
    context = {}
    return render(request, 'index.html', context)

def login_user(request):

    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))

    if request.method == 'POST':

        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect(reverse("dashboard"))
        else:
            # Return an 'invalid login' error message.
            messages.error(request, "Il y'a eu une erreur d'authentification.")
            return redirect(reverse("login"))
    else:
        context = {}
        return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, "Vous avez bien été déconnecté")
    context = {}
    return redirect(reverse("login"))

# La vue dashboard affiche un tableau de bord avec des statistiques sur les machines et les entretiens
@login_required
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
@login_required
def infra(request):
    infrastructures = Infrastructure.objects.all()
    addInfraForm = AddInfraForm()
    deleteInfraForm = DeleteInfraForm()
    addMachineForm = AddMachineForm()
    submitted_add = False
    submitted_delete = False
    submitted_add_machine = False

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
        elif 'add_machine_form' in request.POST:
            addMachineForm = AddMachineForm(request.POST)
            if addMachineForm.is_valid():
                addMachineForm.save()
                submitted_add_machine = True
                addMachineForm = AddMachineForm()

    context = {
        'infrastructures': infrastructures,
        'addInfraForm': addInfraForm,
        'deleteInfraForm': deleteInfraForm,
        'addMachineForm': addMachineForm,
        'submitted_add': submitted_add,
        'submitted_delete': submitted_delete,
        'submitted_add_machine': submitted_add_machine
    }
    return render(request, 'admin/infra.html', context)


# La vue machine_detail_view affiche les détails d'une machine spécifique
@login_required
def machine_detail_view(request, pk):
    machine_seule = get_object_or_404(Machine, id=pk)
    context = {'machine': machine_seule}
    return render(request, 'admin/machine_detail.html', context)


# La vue delete_machine_view supprime une machine spécifique et redirige l'utilisateur vers la page d'infrastructures
@login_required
def delete_machine_view(request, pk):
    machine_seule = get_object_or_404(Machine, id=pk)
    machine_seule.delete()
    return redirect(reverse('infra'))


@login_required
def taches(request):
    # Récupérer les entretiens à faire qui sont actuellement en cours
    entretien_a_faire = entretiens.filter(etat=True)

    # Grouper les entretiens à faire par type et compter leur nombre
    entretien_par_type = entretien_a_faire.values('type').annotate(count=Count('type'))

    # Récupérer les machines qui nécessitent un entretien par type d'entretien
    machines_entretien = []
    # for entretien_type in entretien_par_type:
    #     machines = Machine.objects.filter(entretien__type=entretien_type['type'])
    #     machines_entretien.append({'type': entretien_type['type'], 'machines': machines})



    for entretien_type in entretien_par_type:
        machines = Machine.objects.filter(entretien__type=entretien_type['type'])
        machines_entretien.append({
            'type': entretien_type['type'],
            'machines': machines,
            'entretien_id': [machine.get_entretien_ids() for machine in machines][0][0]
        })



    # # Grouper les entretiens à faire par type et compter leur nombre
    # entretien_par_type = entretien_a_faire.values('type', 'nom', 'description').annotate(count=Count('type'))

    # Récupérer les machines qui nécessitent un entretien par type d'entretien
    # machines_entretien = []
    # for entretien_type in entretien_par_type:
    #     machines = Machine.objects.filter(entretien__type=entretien_type['nom'])
    #     machines_entretien.append({'type': entretien_type['type'],'nom': entretien_type['nom'], 'description': entretien_type['description'],'machines': machines})

    # print(machines_entretien)
    # for entretien in machines_entretien:
    #     print(entretien['machines'])

    # machines_entretien = []
    # for entretien_type in entretien_par_type:
    #     machines = Machine.objects.filter(entretien__type=entretien_type['nom'])
    #     machines_entretien.append({'type': entretien_type['type'],'nom': entretien_type['nom'], 'description': entretien_type['description'],'machines': machines})

    # print(machines_entretien)
    # for entretien in machines_entretien:
    #     print(entretien['machines'])

    # Initialiser les formulaires pour ajouter et supprimer des entretiens
    addEntretienForm = AddEntretienForm()
    deleteEntretienForm = DeleteEntretienForm()
    submitted_add = False
    submitted_delete = False

    print(machines_entretien)

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

# La vue entretien_detail_view affiche les détails d'un entretien spécifique
@login_required
def entretien_detail_view(request, pk):
    entretien_seul = get_object_or_404(Entretien, id=pk)
    context = {'entretien': entretien_seul}
    return render(request, 'admin/entretien_detail.html', context)

@login_required
def taches_historique(request):
 
    context = {
        'entretiens' : entretiens,
    }

    return render(request, 'admin/taches_histo.html', context)

def is_superadmin(function):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url='dashboard',
        redirect_field_name='redirect_field_name'
    )
    return actual_decorator(function)

@is_superadmin
def create_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        try:
            User = get_user_model()

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different username.')
                return redirect('create-user')

            # Create the user and personnel instances
            user = User.objects.create_user(username=username, password=password)

            messages.success(request, 'User created successfully.')
            return redirect('create-user')
        except Exception as e:
            messages.error(request, f'Failed to create user. Error: {str(e)}')
            return redirect('create-user')



    return render(request, 'create_user.html')
