import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

patient_diagnoses_file = pd.read_csv(copyTitle + '/patient_data_fracture_flags_race.csv')

# filter by category column into a new table
# category column should be equal to musculoskeletal

patient_data = {
  
}

patient_demographic = {
  
}

patient_diagnoses_dict = {
  
}

for i in range(len(patient_diagnoses_file) - 1, 0, -1):
  patient_id = patient_diagnoses_file['subject_id'][i]
  # check if any of the columns above are true
  for col in ['Pathologic fracture', 'Pathologic fracture of femur', 'Pathologic fracture of vertebrae', 'Malunion and nonunion of fracture', 'Fracture of tibia and fibula', 'Fracture of lower limb', 'Stress fracture', 'Fracture of unspecified part of femur', 'Fracture of neck of femur', 'Fracture of ankle and foot', 'Fracture of radius and ulna', 'Fracture of vertebral column without mention of spinal cord injury', 'Fracture of hand or wrist']:
    if patient_diagnoses_file.at[i, col]:
      patient_diagnoses_dict[patient_id] = True
      
# remove rows where patient_diagnoses_dict[patient_id] = True
patient_diagnoses_file = patient_diagnoses_file[~patient_diagnoses_file['subject_id'].isin(list(patient_diagnoses_dict.keys()))]

# write
patient_diagnoses_file.to_csv(copyTitle + '/fracture_patients_matching_bank.csv', index=False)