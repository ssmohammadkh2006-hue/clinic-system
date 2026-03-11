from django.shortcuts import render, redirect
from.models import *
from .forms import PatientForm, DoctorForm, NuresForm, DrugForm
from django.utils import timezone
from django.db.models import Q

def index(request): #--------------------------------------------------------
    doctors_count = Doctors.objects.count()

    patients_total = Patients.objects.count()

    today = timezone.now().date()

    appointments_today = Appointments.objects.filter(date=today).count()

    context = {
        'doctors_count': doctors_count,
        'patients_total': patients_total,
        'appointments_today': appointments_today,
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

        doctor.doctor_name = request.POST['doctor_name']
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
    patient = Patients.objects.get(id=id)

    if request.method == "POST":
        patient.patient_name = request.POST['patient_name']
        patient.age = request.POST['age']
        patient.phone = request.POST['phone']
        patient.date = request.POST['date']
        patient.address = request.POST['address']
        patient.cost = request.POST['cost']
        patient.paid = request.POST['paid']
        patient.remaining = request.POST['remaining']
        patient.responsible_doctor = request.POST['responsible_doctor']
        patient.medical_history = request.POST['medical_history']

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