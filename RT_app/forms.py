from django import forms 
from django.core.exceptions import ValidationError
from .models import Personnel,Infrastructure, Entretien
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
    add_tache_form = forms.CharField(widget=forms.HiddenInput(), initial='add_tache_form')

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
            'date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date limite de l\'entretien'}),
            'id_personnel': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Personnel responsable de l\'entretien'}),
            'id_machine': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Machine sur laquelle faire la tâche'})
        }



