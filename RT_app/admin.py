from django.contrib import admin
from .models import machine, entretien, personnel,infrastructure
# Register your models here.

admin.site.register(machine)
admin.site.register(entretien)
admin.site.register(personnel)
admin.site.register(infrastructure)