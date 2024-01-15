# mypracticeapp/models.py
from django.db import models

class Contact(models.Model):
    """A generic model for various contact types (Identifier, HumanName, ContactPoint, Address, etc.)"""
    system = models.CharField(max_length=50)
    value = models.CharField(max_length=255)
    use = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"{self.system}: {self.value}"

class Patient(models.Model):
    fhir_id = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=100, blank=True)
    telecoms = models.ManyToManyField(Contact, related_name='patient_telecoms', blank=True)
    addresses = models.ManyToManyField(Contact, related_name='patient_addresses', blank=True)

    active = models.BooleanField(default=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('unknown', 'Unknown')])
    birth_date = models.DateField(blank=True)
    marital_status = models.CharField(max_length=20, blank=True, null=True)
    multiple_birth = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name.first().given} {self.name.first().family}"
