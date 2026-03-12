from django.db import models

# Create your models here.
class Patients(models.Model):
    patient_name = models.CharField(max_length=200)
    age = models.IntegerField(null=True,blank=True)
    phone = models.CharField(max_length=20,null=True,blank=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    paid = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    remaining = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    responsible_doctor = models.CharField(max_length=100,null=True,blank=True)
    medical_history = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.patient_name
    
class Doctors(models.Model):
    doctors_name = models.CharField(max_length=200)
    specialisation=models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    def __str__(self):
        return self.doctors_name
    
class Nures(models.Model):
    nures_name = models.CharField(max_length=200)
    responsible_doctor = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=20)
    def __str__(self):
        return self.nures_name
    
class Drugs(models.Model):
    drug_name = models.CharField(max_length=100)
    quantity=models.IntegerField(null=True,blank=True) 
    date = models.DateField(null=True,blank=True)
    def __str__(self):
        return self.drug_name
    
  