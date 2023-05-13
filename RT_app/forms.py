from django import forms 
from django.core.exceptions import ValidationError
from .models import Personnel, Infrastructure, Entretien, Entretien_detail
from django.core.validators import RegexValidator


class AddInfraForm(forms.ModelForm):
    add_infra_form = forms.CharField(widget=forms.HiddenInput(), initial='add_infra_form')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_personnel'].queryset = Personnel.objects.all()

    class Meta:
        model = Infrastructure
        fields = ['nom', 'id_personnel', 'pays', 'ville', 'coordonnees']
        labels = {
            'id_personnel': 'Personnel responsable de l\'infra',
            'coordonnees': 'Coordonnées'
        }
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'infra'}),
            'id_personnel': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Personnel responsable de l\'infra'}),
            'pays': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pays de l\'infra'}),
            'ville': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville de l\'infra'}),
            'coordonnees': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Coordoonnées décimales, ex: 46.816487 0.548146'}),
        }


class DeleteInfraForm(forms.ModelForm):
    confirm = forms.BooleanField(required=True, initial=False)
    nom = forms.ModelChoiceField(queryset=Infrastructure.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'infra'}), required=True)
    delete_infra_form = forms.CharField(widget=forms.HiddenInput(), initial='delete_infra_form')

    class Meta:
        model = Infrastructure
        fields = ['nom']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirm'].label = 'Confirmez la suppression de cette infrastructure'

    def clean(self):
        cleaned_data = super().clean()
        confirm = cleaned_data.get('confirm')

        if not confirm:
            raise forms.ValidationError('Vous devez confirmer la suppression de cette infrastructure.')


class AddEntretienForm(forms.ModelForm):
    add_entretien_form = forms.CharField(widget=forms.HiddenInput(), initial='add_entretien_form')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Entretien
        fields = [ 'type', 'description', 'date', 'id_personnel','id_machine']
        labels = {
            'id_personnel': 'Personnel attitré',
            'id_machine': 'Machine atitrée'
        }
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Type de l\'entretien'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Que faire ?'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date limite de l\'entretien'}),
            'id_personnel': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Personnel responsable de l\'entretien'}),
            'id_machine': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Machine sur laquelle faire la tâche'})
        }

# class DeleteEntretienForm(forms.ModelForm):
#     delete_entretien_form = forms.CharField(widget=forms.HiddenInput(), initial='delete_entretien_form')

#     entretien_choices = [(entretien.nom, entretien.nom) for entretien in Entretien.objects.all()]
#     nom = forms.ChoiceField(choices=entretien_choices, widget=forms.Select(attrs={'class': 'form-control'}))

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#     class Meta:
#         model = Entretien 
#         fields = ['nom']  
#         labels = {
#             'nom': 'Nom de l\'entretien'
#         }
#         widgets = {
#             'nom': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'entretien'}),
#         }

class DeleteEntretienForm(forms.ModelForm):
    confirm = forms.BooleanField(required=True, initial=False, label='Confirmer')
    delete_entretien_form = forms.CharField(widget=forms.HiddenInput(), initial='delete_entretien_form')
    entretien_choices = [(entretien.id, entretien.get_name()) for entretien in Entretien.objects.all().filter(etat=True)]
    nom = forms.ChoiceField(choices=entretien_choices, widget=forms.Select(attrs={'class': 'form-control'}), label='Nom de l\'entretien')

    class Meta:
        model = Entretien 
        fields = ['nom']
        widgets = {
             'nom': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'entretien'}),
        }

        def clean(self):
            cleaned_data = super().clean()
            clean_name = cleaned_data.get('name')
            confirm = cleaned_data.get('confirm')

            if not Entretien.objects.filter(name=clean_name).exists():
                raise forms.ValidationError("Cet entretien n'existe pas")
            
            if not confirm:
                raise forms.ValidationError('Vous devez confirmer la suppression de cet entretien.')

