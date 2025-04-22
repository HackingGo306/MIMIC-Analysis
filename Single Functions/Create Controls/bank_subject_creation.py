# Compiles the patients in the weight measurement file (with all other columns like fractures)
# Every row is now a unique patient
# If a patient has a history of any condition, it is set to true for this column
# We take the median of age, weight, and other numerical values
# Output: 61,779 unique patients

import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

patient_diagnoses_file = pd.read_csv(copyTitle + '/patient_data_fracture_flags_race 1.2.csv')
# Change to "patient_data_fracture_flags_race 1.2.csv" to include fracture patients

patient_data = {
  
}

patient_demographic = {
  
}

patient_diagnoses_dict = {
  
}


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

'''
circulatory system
congenital anomalies
dermatologic
digestive
endocrine/metabolic
genitourinary
hematopoietic
infectious diseases
injuries & poisonings
mental disorders
musculoskeletal
neoplasms
neurological
pregnancy complications
respiratory
sense organs
symptoms
Unknown
'''

ac = 0
for i in range(len(patient_diagnoses_file)):
  if (i % 100000 == 0):
    print(100 * (i / len(patient_diagnoses_file)), "percent [part 1]")  
  
  patient_id = patient_diagnoses_file['subject_id'][i]
  
  # do the same for the columns above
  for col in ['circulatory system', 'congenital anomalies', 'dermatologic', 'digestive', 'endocrine/metabolic', 'genitourinary', 'hematopoietic', 'infectious diseases', 'injuries & poisonings','mental disorders','musculoskeletal', 'neoplasms', 'neurological', 'pregnancy complications','respiratory','sense organs','symptoms', 'Unknown', 'Pathologic fracture', 'Pathologic fracture of femur', 'Pathologic fracture of vertebrae', 'Malunion and nonunion of fracture', 'Fracture of tibia and fibula', 'Fracture of lower limb', 'Stress fracture', 'Fracture of unspecified part of femur', 'Fracture of neck of femur', 'Fracture of ankle and foot', 'Fracture of radius and ulna', 'Fracture of vertebral column without mention of spinal cord injury', 'Fracture of hand or wrist']:
    if patient_diagnoses_file.at[i, col]:
      if (patient_id not in patient_diagnoses_dict):
        patient_diagnoses_dict[patient_id] = {}
      patient_diagnoses_dict[patient_id][col] = True

  weight = patient_diagnoses_file['weight'][i]
  height = patient_diagnoses_file['height'][i]
  age = patient_diagnoses_file['age'][i]
  gender = patient_diagnoses_file['gender'][i]
  race = patient_diagnoses_file['race'][i]
  
  if patient_id not in patient_data:
    patient_data[patient_id] = ([], [], [])
    
  patient_data[patient_id][0].append(weight)
  patient_data[patient_id][1].append(height)
  patient_data[patient_id][2].append(age)
  
  if patient_id not in patient_demographic:
    patient_demographic[patient_id] = {}
    patient_demographic[patient_id] = (race, gender)
    
# create a new datafram with the same columns as patient_diagnoses_file
patient_data_file = pd.DataFrame(columns=patient_diagnoses_file.columns)

count = 0
missed = 0

print("Total", len(patient_data.keys()))
for key in patient_data.keys():
  
  if (count % 2000 == 0):
    print((count / len(patient_data.keys()) * 100), "percent", missed, "missed")
  
  (race, gender) = patient_demographic[key]

  weight, height, age = patient_data[key]
  weight = np.median(weight)
  height = np.median(height)
  age = np.median(age)
  
  patient_data_file.at[count, 'weight'] = weight
  patient_data_file.at[count, 'height'] = height
  patient_data_file.at[count, 'age'] = age
  patient_data_file.at[count,'subject_id'] = key
  patient_data_file.at[count, 'race'] = race
  patient_data_file.at[count, 'gender'] = gender
  
  # set the other columns
  try: 
    for col in patient_diagnoses_dict[key]:
      patient_data_file.at[count, col] = True
  except KeyError:
    # print(f'No diagnoses for patient {key}')
    missed += 1
  
  count += 1
    
patient_data_file.drop('w_time', axis=1, inplace=True)
patient_data_file.drop('h_time', axis=1, inplace=True)
patient_data_file.drop('bmi', axis=1, inplace=True)
patient_data_file.drop('bmi_time', axis=1, inplace=True)
patient_data_file.drop('projected_bmi', axis=1, inplace=True)

for col in ['circulatory system', 'congenital anomalies', 'dermatologic', 'digestive', 'endocrine/metabolic', 'genitourinary', 'hematopoietic', 'infectious diseases', 'injuries & poisonings','mental disorders','musculoskeletal', 'neoplasms', 'neurological', 'pregnancy complications','respiratory','sense organs','symptoms', 'Unknown']:
  patient_data_file[col] = patient_data_file[col].fillna(False)

for col in ['Pathologic fracture', 'Pathologic fracture of femur', 'Pathologic fracture of vertebrae', 'Malunion and nonunion of fracture', 'Fracture of tibia and fibula', 'Fracture of lower limb', 'Stress fracture', 'Fracture of unspecified part of femur', 'Fracture of neck of femur', 'Fracture of ankle and foot', 'Fracture of radius and ulna', 'Fracture of vertebral column without mention of spinal cord injury', 'Fracture of hand or wrist']:
  patient_data_file[col] = patient_data_file[col].fillna(False)

# write
patient_data_file.to_csv(copyTitle + '/patient_data_with_fracture_group.csv', index=False)

# Patient_data_with_fracture_group: includes fracture patients in the count as well (did not run remove fractured patients)