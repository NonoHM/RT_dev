from django.db import models
from datetime import datetime
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Personnel(AbstractUser):

    id = models.AutoField(primary_key=True,editable=False)

    is_staff = models.BooleanField(default=False)

    id_infrastructure = models.ForeignKey('Infrastructure', on_delete=models.CASCADE, null=True, default=None)

    def __str__ (self):
        return f"{self.username} ({self.id_infrastructure})"



class Machine(models.Model):

    TYPE = (
        ('PC', 'PC - OS windows'),
        ('Mac', ('Mac - OS MacOS')),
        ('Serveur', ('Serveur - OS Debian')),
        ('Autre', ('Autre type de machine')),
    )

    id = models.AutoField(primary_key=True,editable=False)

    nom = models.CharField(max_length=30, default="PC")

    ip = models.CharField(max_length=15, default="172.0.0.1", validators=[RegexValidator(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$')])

    etat = models.BooleanField(default=True)

    id_infrastructure = models.ForeignKey('Infrastructure', on_delete=models.CASCADE)

    type_machine = models.CharField(max_length=32, choices=TYPE, default='PC')

    def __str__ (self):
        return f"{self.nom} -> {self.ip} ({self.id_infrastructure})"

    def get_entretien_ids(self):
        return [entretien.id for entretien in self.entretien_set.all()]

class Infrastructure(models.Model):
    id = models.AutoField(primary_key=True,editable=False)

    nom = models.CharField(max_length=40)

    id_personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)

    pays = models.CharField(max_length=30)

    ville = models.CharField(max_length=64)

    coordonnees = models.CharField(null=True, blank=True ,max_length=18, validators=[RegexValidator(r'^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)\s*[-+]?([1-9]?\d(\.\d+)?|1[0-7]\d(\.\d+)?|180(\.0+)?)$')])  
    
    ip_reseau = models.CharField(max_length=15, default="192.168.0.0", validators=[RegexValidator(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$')])

    masque = models.CharField(max_length=15, default="255.255.255.0", validators=[RegexValidator(r'^(?:128|192|224|240|248|252|254|255)\.(?:0|128|192|224|240|248|252|254|255)\.(?:0|128|192|224|240|248|252|254|255)\.(?:0|128|192|224|240|248|252|254|255)$')])

    def __str__ (self):
        return f"{self.nom}"
    
    def get_ip(self):
        return f"{self.ip_reseau} ({self.masque}) "

class Entretien(models.Model):
    TYPE_CHOICES = [
        ('PREVENTIF', 'Préventif'),
        ('CORRECTIF', 'Correctif'),
        ('AMELIORATION', 'Amélioration'),
        ('MISE A JOUR', 'Mise à jour'),
        ('REPARATION', 'Réparation'),
        ('AUTRE', 'Autre')
    ]

    id = models.AutoField(primary_key=True,editable=False)

    nom = models.CharField(max_length=50, default="Mise à jour")

    type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='PREVENTIF')

    description = models.TextField()

    date = models.DateField(default=datetime.now().strftime("%Y-%m-%d"))

    id_personnel = models.ForeignKey('Personnel', on_delete=models.CASCADE)

    id_machine  = models.ForeignKey('Machine', on_delete=models.CASCADE)

    etat = models.BooleanField(default=False)

    def __str__ (self):
        return f"{str(self.id)} -> {self.nom} ({self.type})"
    
    def get_name (self):
        return f"{self.nom} ({self.type})"

class Entretien_detail(models.Model):
    id_machine = models.ForeignKey(Machine, on_delete=models.CASCADE)

    id_entretien = models.ForeignKey(Entretien, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.id_machine) + " -> " + str(self.id_entretien)
