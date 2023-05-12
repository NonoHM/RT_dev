from django.db import models
from datetime import datetime
from django.core.validators import RegexValidator

# Create your models here.

class Personnel(models.Model):

    id = models.AutoField(primary_key=True,editable=False)

    login = models.CharField(max_length=20)

    password = models.CharField(max_length=64, validators=[RegexValidator(r'^[a-z0-9]{64}$')], default='9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08')

    def __str__ (self):
        return str(self.id) + " -> " + self.login

class Machine(models.Model):

    TYPE = (
        ('PC', 'PC - OS windows'),
        ('Mac', ('Mac - OS MacOS')),
        ('Serveur', ('Serveur - OS Debian')),
        ('Autre', ('Autre type de machine')),
    )

    id = models.AutoField(primary_key=True,editable=False)

    nom = models.CharField(max_length=15, default="PC")

    ip = models.CharField(max_length=15, default="172.0.0.1", validators=[RegexValidator(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$')])

    etat = models.BooleanField(default=True)

    id_infrastructure = models.ForeignKey('Infrastructure', on_delete=models.CASCADE)

    type_machine = models.CharField(max_length=32, choices=TYPE, default='PC')

    def __str__ (self):
        return str(self.id) + " -> " + self.ip


class Infrastructure(models.Model):
    id = models.AutoField(primary_key=True,editable=False)

    nom = models.CharField(max_length=20)

    id_personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)

    pays = models.CharField(max_length=30)

    ville = models.CharField(max_length=64)

    coordonnees = models.CharField(null=True, blank=True ,max_length=18, validators=[RegexValidator(r'^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)\s*[-+]?([1-9]?\d(\.\d+)?|1[0-7]\d(\.\d+)?|180(\.0+)?)$')])  
    
    def __str__ (self):
        return str(self.id) + " -> " + self.nom

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

    type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='PREVENTIF')

    description = models.TextField()

    date = models.DateField(default=datetime.now())

    id_personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)

    id_machine  = models.ForeignKey(Machine, on_delete=models.CASCADE)

    etat = models.BooleanField(default=False)

    def __str__ (self):
        return str(self.id) + " -> " + self.type

class Entretien_detail(models.Model):
    id_machine = models.ForeignKey(Machine, on_delete=models.CASCADE)

    id_entretien = models.ForeignKey(Entretien, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.id_machine) + " -> " + str(self.id_entretien)
