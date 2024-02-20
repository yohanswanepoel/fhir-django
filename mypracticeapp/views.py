# myapp/views.py
from django.shortcuts import render
from fhirclient import client
import fhirclient.models.patient as p
import requests
from .models import Patient as PatientModel
from django.conf import settings
import json

def index(request):
    # Fetch patient data from the FHIR server
    patients_data = fetch_patients_data()
    return render(request, 'mypracticeapp/index.html', {'patients': patients_data})

def patient_detail(request, patient_id):
    patients_data = fetch_patients_data()
    patient_details = get_patient_detail(patient_id)
    return render(request, 'mypracticeapp/index.html', {'patients': patients_data, 'selected_patient': patient_details})


def fetch_patients_data():
    # Example: Fetch patient data from the FHIR server
    fhir_url = f'{settings.FHIR_SERVER_BASE_URL}/Patient'
    response = requests.get(fhir_url, verify=False)

    if response.status_code == 200:
        # Parse FHIR data
        fhir_data = response.json()
        patients_data = []
        patients = fhir_data.get('entry', [])
        for patient in patients:
            fhir_patient = p.Patient(patient["resource"]) 
            patients_data.append({'id': fhir_patient.id, 'name': f'{fhir_patient.name[0].family}, {fhir_patient.name[0].given[0]}'})
    
        # Extract relevant patient information
        #patients_data = [{'fhir_id': patient.get('resource', {}).get('id'), 'name': patient.get('resource', {}).get('name', [{}])[0].get('text')} for patient in patients]
        print(patients_data)
        # patients_data = [{'fhir_id': patient.id, 'name': patient.name[0].text} for patient in patients]
        return patients_data
    else:
        print(f'Error fetching data from FHIR server. Status code: {response.status_code}')
        return []
    
def get_patient_detail(patient_id):
    fhir_url = f'{settings.FHIR_SERVER_BASE_URL}/Patient/{patient_id}'
    response = requests.get(fhir_url, verify=False)  # Disable SSL certificate verification

    if response.status_code == 200:
        # Parse FHIR data
        fhir_data = response.json()
        patient = p.Patient(fhir_data)
        # Extract relevant patient details
        # This should deploy
        patient_details = {
            'id': patient.id,
            'name': f'{patient.name[0].family}, {patient.name[0].given[0]}',
            'active': patient.active,
            'gender': patient.gender,
            'birth_date': patient.birthDate.as_json,
            # 'marital_status': patient.maritalStatus, # Comment out this line as it is a purposed bug
            'marital_status': patient.maritalStatus.text, # Uncomment this line to have the right value
            # Add other patient details as needed Dhi
        }
        return patient_details
    else:
        print(f'Error fetching patient details from FHIR server. Status code: {response.status_code}')
        return {}


