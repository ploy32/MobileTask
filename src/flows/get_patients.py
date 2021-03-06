from typing import List

from dal.patient_repository import PatientRepository
from model.config_model import Patient


class PatientsListFlow:
    def __init__(self):
        self.patient_repository = PatientRepository()

    def get_all_patients(self) -> List[Patient]:
        return self.patient_repository.get_patients_list()

    def get_patient_by_id(self, patient_id: int) -> Patient:
        patient = self.patient_repository.get_patient_by_id(patient_id)
        return patient








