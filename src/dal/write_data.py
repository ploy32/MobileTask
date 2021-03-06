from dal.inmemory_database import In_Memory_Database
from dal.json_reader import JsonReader
from flows.get_doctors import DoctorsListFlow
from flows.get_patients import PatientsListFlow
from model.config_model import Doctor, Patient, Appointment


class WriteData:
    def __init__(self, path: str):
        self.path = path
        self.db = In_Memory_Database
        self.json_reader = JsonReader(self.path)

    def init_doctors_data(self) -> str:
        doctors_list_data = self.json_reader.read_from_json()
        for doctor in doctors_list_data:
            doctor_id = doctor.get('Doctor-ID')
            doctor_name = doctor.get('Doctor-Name')
            doctor_phone = doctor.get('Doctor-Phone')
            doctor_available_status = doctor.get('Available-Status')
            doctor_available_start_time = doctor.get('Available-Start-Time')
            doctor_end_time = doctor.get('End-Time')
            doctor_specialty = doctor.get('Doctor-Specialty')
            Doctor_waiting_patients_id = doctor.get('Doctor-waiting-patients-id')

            doctor_obj = Doctor(doctor_id, doctor_name, doctor_phone,doctor_available_status, doctor_available_start_time,doctor_end_time,
                                doctor_specialty, Doctor_waiting_patients_id)
            self.db.add_doctor(doctor_obj)
        return self.db.doctors_list

    def init_patients_data(self) -> str:
        patients_list_data = self.json_reader.read_from_json()
        for patient in patients_list_data:
            patient_id = patient.get('Patient-ID')
            patient_name = patient.get('Patient-Name')
            doctor_name = patient.get('Doctor-Name')
            patient_phone = patient.get('Patient-Phone')
            patient_message = patient.get('Patient-Message')
            patient_arrival_time = patient.get('Patient-Arrival-Time')

            patient_obj = Patient(patient_id, patient_name, doctor_name, patient_phone, patient_message,
                                  patient_arrival_time)
            self.db.add_patient(patient_obj)

        return self.db.patients_list

    def init_appointments_data(self) -> str:
        appointments_list_data = self.json_reader.read_from_json()
        for appointment in appointments_list_data:
            # Appointment
            appointment_index = appointment.get('Appointment-Index')
            appointment_date_time = appointment.get('Appointment-Date')
            appointment_type = appointment.get('Type')
            appointment_time_slot = appointment.get('Time-Slot(Min)')
            # Patient
            appointment_patient_id = appointment.get('Patient-ID')
            # Doctor
            appointment_doctor_id = appointment.get('Doctor-ID')
            # Flow
            patient_id_flow = PatientsListFlow(appointment_patient_id)
            doctor_id_flow = DoctorsListFlow(appointment_doctor_id)
            # Parsed Patient Object
            filtered_patient_by_id = patient_id_flow.get_patient_by_id()
            # Parsed Doctor Object
            filtered_doctor_by_id = doctor_id_flow.get_doctor_by_id()  # get doctor by id
            # Parsed Appointment Object
            appointment_obj = Appointment(appointment_index, appointment_date_time, appointment_type,
                                          appointment_doctor_id, filtered_patient_by_id,
                                          filtered_doctor_by_id, appointment_time_slot)
            self.db.add_appointment(appointment_obj)

        return self.db.appointments_list
