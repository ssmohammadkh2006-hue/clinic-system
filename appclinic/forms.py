from django import forms
from .models import *

class PatientForm(forms.ModelForm):

    class Meta:
        model = Patients
        fields = '__all__'
        
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctors
        fields = '__all__'


class NuresForm(forms.ModelForm):
    class Meta:
        model=Nures
        fields='__all__'
        
class DrugForm(forms.ModelForm):
    class Meta:
        model=Drugs
        fields='__all__'