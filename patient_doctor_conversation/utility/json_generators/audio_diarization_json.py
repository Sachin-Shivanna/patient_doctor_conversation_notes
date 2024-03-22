import json
import os
from datetime import datetime

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
        if os.path.isfile('diarization_files/'+datetime.today().year+'/'+self.accountID) is False:
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

            with open('diarization_files/'+datetime.today().year+'/'+self.accountID, "w") as outfile:
             outfile.write(json_object)
        else:
            new_visit = {
                {
                        "date": self.visit_details["date"],
                        "report_generated" : False,
                        "data": {
                            "weight": self.visit_details["weight"],
                            "bloodPressure": self.visit_details["bloodPressure"],
                            "temperature": self.visit_details["temperature"]
                        }
                        }
            }