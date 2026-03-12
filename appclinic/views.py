from django.shortcuts import render, redirect, get_object_or_404
from.models import *

from .forms import PatientForm, DoctorForm, NuresForm, DrugForm
from django.utils import timezone

from django.db.models import Q

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import pandas as pd
from django.http import HttpResponse


def export_patients_excel(request):

    patients = Patients.objects.all().values(
        'patient_name',
        'age',
        'phone',
        'address',
        'date',
        'cost',
        'paid',
        'remaining',
        'responsible_doctor',
        'medical_history'
    )

    df = pd.DataFrame(list(patients))

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = 'attachment; filename="patients_report.xlsx"'


    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Patients')

        worksheet = writer.sheets['Patients']

        worksheet.column_dimensions['A'].width = 25
        worksheet.column_dimensions['B'].width = 5
        worksheet.column_dimensions['C'].width = 18
        worksheet.column_dimensions['D'].width = 15
        worksheet.column_dimensions['E'].width = 15
        worksheet.column_dimensions['F'].width = 10
        worksheet.column_dimensions['G'].width = 10
        worksheet.column_dimensions['H'].width = 10
        worksheet.column_dimensions['I'].width = 25
        worksheet.column_dimensions['J'].width = 40


    return response
 
def login_view(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'pages/login.html', {'error': 'Invalid username or password'})

    return render(request, 'pages/login.html')

@login_required
def index(request):

    doctors_count = Doctors.objects.count()
    patients_total = Patients.objects.count()
    nurses_count = Nures.objects.count()

    context = {
        'doctors_count': doctors_count,
        'patients_total': patients_total,
        'nurses_count': nurses_count,
    }

    return render(request, 'pages/index.html', context)

def patients(request):

    search = request.GET.get('search')

    if search:
        all_patients = Patients.objects.filter(
            Q(patient_name__icontains=search) |
            Q(responsible_doctor__icontains=search)
        )
    else:
        all_patients = Patients.objects.all()

    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patients')
    else:
        form = PatientForm()

    context = {
        'form': form,
        'all_patients': all_patients
    }

    return render(request, 'pages/patients.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')

def doctors(request): #--------------------------------------------------------
    if request.method == "POST":
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctors')
    else:
        form = DoctorForm()
    all_doctors = Doctors.objects.all()
    context = {
        'form': form,
        'all_doctors': all_doctors
    }   
    return render(request, 'pages/doctors.html',context)


def nures(request): #--------------------------------------------------------
    if request.method == "POST":
        form = NuresForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nures')
    else:
        form = NuresForm()
    all_Nures = Nures.objects.all()
    context = {
        'form': form,
        'all_Nures': all_Nures
        
    }  
    
    return render(request, 'pages/nures.html',context)

def drugs(request): #--------------------------------------------------------
    if request.method == "POST":
        form = DrugForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('drugs')
    else:
        form = DrugForm()
    all_Drugs= Drugs.objects.all()
    context = {
        'form': form,
        'all_Drugs': all_Drugs
        
    }  
    
    
    return render(request, 'pages/drugs.html',context)


def update_drug(request, id):

    drug = Drugs.objects.get(id=id)

    if request.method == "POST":

        drug.drug_name = request.POST['drug_name']
        drug.quantity = request.POST['quantity']
        drug.date = request.POST['date']

        drug.save()

        return redirect('drugs')

    context = {
        'drug': drug
    }

    return render(request, 'pages/update_drug.html', context)


def update_doctor(request, id):

    doctor = Doctors.objects.get(id=id)

    if request.method == "POST":

        doctor.doctors_name = request.POST['doctors_name']
        doctor.specialisation = request.POST['specialisation']
        doctor.phone = request.POST['phone']

        doctor.save()

        return redirect('doctors')

    context = {
        'doctor': doctor
    }

    return render(request, 'pages/update_doctor.html', context)


def update_nures(request, id):
    nurse = Nures.objects.get(id=id)

    if request.method == "POST":
        nurse.nures_name = request.POST['nures_name']
        nurse.responsible_doctor = request.POST['responsible_doctor']
        nurse.phone = request.POST['phone']

        nurse.save()

        return redirect('nures')

    context = {
        'nurse': nurse
    }

    return render(request, 'pages/update_nures.html', context)


def update_patient(request, id):

    patient = get_object_or_404(Patients, id=id)
    if request.method == "POST":
        patient.patient_name = request.POST.get('patient_name')
        patient.age = request.POST.get('age') or 0
        patient.phone = request.POST.get('phone')
        
        date_value = request.POST.get('date')
        if date_value:
            patient.date = date_value
        else:
            patient.date = None
        
        patient.address = request.POST.get('address')
        patient.cost = request.POST.get('cost') or 0
        patient.paid = request.POST.get('paid') or 0
        patient.remaining = request.POST.get('remaining') or 0
        patient.responsible_doctor = request.POST.get('responsible_doctor')
        patient.medical_history = request.POST.get('medical_history')

        patient.save()
        return redirect('patients')
    context = {
        'patient': patient
    }
    return render(request, 'pages/update_patient.html', context)



def delete_item(request, model, id):

    if model == "patient":
        item = Patients.objects.get(id=id)
        redirect_page = "patients"

    elif model == "doctor":
        item = Doctors.objects.get(id=id)
        redirect_page = "doctors"

    elif model == "nurse":
        item = Nures.objects.get(id=id)
        redirect_page = "nures"

    elif model == "drug":
        item = Drugs.objects.get(id=id)
        redirect_page = "drugs"

    if request.method == "POST":
        item.delete()
        return redirect(redirect_page)

    context = {
        "item": item
    }

    return render(request, "pages/delete_confirm.html", context)

 
