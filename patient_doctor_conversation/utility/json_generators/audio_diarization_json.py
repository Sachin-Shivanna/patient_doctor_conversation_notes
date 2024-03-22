import json
import os
from datetime import date
import calendar

class audio_diarization_json:
    def __init__(self, clinicName, accountID, patientID, patientName, conversation_directory,doctor_incharge, visit_details = {}):
        self.clinicName = clinicName
        self.accountID = accountID
        self.patientID = patientID
        self.patientName = patientName
        self.conversation_directory = conversation_directory
        self.doctor_incharge = doctor_incharge
        self.visit_details = visit_details

    def construct_json(self):
        
        # Get the current date
        current_date = date.today()

        # Extract year, month, and day
        current_year = current_date.year
        current_month = current_date.month

        # Get the month name
        current_month_name = calendar.month_name[current_month]

        file_loc = 'diarization_files/'+current_year+'/'+current_month_name+'/'+current_date+'/'+self.accountID+'.json'
        if os.path.isfile(file_loc) is False:
            json_object =  json.dumps(
                        {
                "clinicName": self.clinicName,
                "accountID": self.accountID,
                "patients": [
                    {
                    "patientID": self.patientID,
                    "name": self.patientName,
                    "visits": [
                        {
                        "date": self.visit_details["date"],
                        "report_generated" : False,
                        "doctor_incharge" : self.doctor_incharge,
                        "data": {
                            "weight": self.visit_details["weight"],
                            "bloodPressure": self.visit_details["bloodPressure"],
                            "temperature": self.visit_details["temperature"]
                        }
                        }
                    ]
                    }
                ]
                }, indent=2
            )

            with open(file_loc, "w") as outfile:
             outfile.write(json_object)
        else:

            def find_patient_by_id(clinic_data, patient_id):
                for patient in clinic_data['patients']:
                    if patient['patientID'] == patient_id:
                        return patient
                return None  # Return None if no patient found

            # Read the original JSON data
            with open(file_loc, 'r') as file:
                clinic_data = json.load(file)
            
            patient = find_patient_by_id(clinic_data, self.patientID)

            if patient:
                new_visit = {
                    {
                        "date": self.visit_details["date"],
                        "report_generated" : False,
                        "doctor_incharge" : self.doctor_incharge,
                        "data": {
                            "weight": self.visit_details["weight"],
                            "bloodPressure": self.visit_details["bloodPressure"],
                            "temperature": self.visit_details["temperature"]
                            }
                        }
                }
                patient['visits'].append(new_visit)

                # Write the updated JSON back to the file
                with open(file_loc, 'w') as file:
                    json.dump(clinic_data, file, indent=2)

            else:
                new_patient = {
                    "patientID": self.patientID,
                    "name": self.patientName,
                    "visits": [
                        {
                        "date": self.visit_details["date"],
                        "report_generated" : False,
                        "doctor_incharge" : self.doctor_incharge,
                        "data": {
                            "weight": self.visit_details["weight"],
                            "bloodPressure": self.visit_details["bloodPressure"],
                            "temperature": self.visit_details["temperature"]
                        }
                        }
                    ]
                    }
                
                clinic_data['patients'].append(new_patient)
                # Write the updated JSON back to the file
                with open(file_loc, 'w') as file:
                    json.dump(clinic_data, file, indent=2)

            