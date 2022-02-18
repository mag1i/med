from django.contrib import admin

# Register your models here.
from med.models import Patient, Dctr, Rdv

admin.site.register(Patient)
admin.site.register(Dctr)
admin.site.register(Rdv)