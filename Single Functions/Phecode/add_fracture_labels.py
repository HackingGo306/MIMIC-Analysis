import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

musculoskeletal_diagnoses = pd.read_csv(copyTitle + '/fractures.csv')
data_file = pd.read_csv(copyTitle + '/patient_data.csv')

patient_diagnoses = {
  
}

for i in range(len(musculoskeletal_diagnoses)):
  patient_id = musculoskeletal_diagnoses['subject_id'][i]
  diagnosis_time = musculoskeletal_diagnoses['diagnosis_time'][i]
  timestamp = datetime.strptime(diagnosis_time, '%Y/%m/%d %H:%M:%S %p')
  fracture_type = musculoskeletal_diagnoses['phecode_string'][i]
  
  if patient_id not in patient_diagnoses:
    patient_diagnoses[patient_id] = []
  
  patient_diagnoses[patient_id].append((timestamp, fracture_type))
  
  
for i in range(len(data_file)):
  if (i % 100000 == 0):
    print(100 * (i / len(data_file)), "percent [part 2]")
  patient_id = data_file['subject_id'][i]
  measurement_time = data_file['w_time'][i]
  measurement_time = datetime.strptime(measurement_time, '%Y-%m-%d') + timedelta(hours=24) # Anything till the end of the day should be included
  
  if patient_id not in patient_diagnoses:
    continue
  
  for j in range(len(patient_diagnoses[patient_id])):
    diagnosis_time, diagnosis_category = patient_diagnoses[patient_id][j]
    if diagnosis_time < measurement_time:
      data_file.at[i, diagnosis_category] = True
      

'''
Pathologic fracture
Pathologic fracture of femur
Pathologic fracture of vertebrae
Malunion and nonunion of fracture
Fracture of tibia and fibula
Fracture of lower limb
Stress fracture
Fracture of unspecified part of femur
Fracture of neck of femur
Fracture of ankle and foot
Fracture of radius and ulna
Fracture of vertebral column without mention of spinal cord injury
Fracture of hand or wrist
'''

for i in range(len(data_file)):
  if (i % 100000 == 0):
    print(100 * (i / len(data_file)), "percent [part 3]")
  # set None values to False for each column above
  for col in ['Pathologic fracture', 'Pathologic fracture of femur', 'Pathologic fracture of vertebrae', 'Malunion and nonunion of fracture', 'Fracture of tibia and fibula', 'Fracture of lower limb', 'Stress fracture', 'Fracture of unspecified part of femur', 'Fracture of neck of femur', 'Fracture of ankle and foot', 'Fracture of radius and ulna', 'Fracture of vertebral column without mention of spinal cord injury', 'Fracture of hand or wrist']:
    data_file.at[i, col] = data_file.at[i, col] if not pd.isna(data_file.at[i, col]) else False


# Save the updated data file
data_file.to_csv(copyTitle + '/patient_data_fracture_flags.csv', index=False)
# diagnosis_file.to_csv(copyTitle + '/patient_diagnoses', index=False)