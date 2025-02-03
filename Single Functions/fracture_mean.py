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
  fracture = False
  
  # check if any of the columns above are true
  for col in ['Pathologic fracture', 'Pathologic fracture of femur', 'Pathologic fracture of vertebrae', 'Malunion and nonunion of fracture', 'Fracture of tibia and fibula', 'Fracture of lower limb', 'Stress fracture', 'Fracture of unspecified part of femur', 'Fracture of neck of femur', 'Fracture of ankle and foot', 'Fracture of radius and ulna', 'Fracture of vertebral column without mention of spinal cord injury', 'Fracture of hand or wrist']:
    if patient_diagnoses_file.at[i, col]:
      fracture = True
      if (patient_id not in patient_diagnoses_dict):
        patient_diagnoses_dict[patient_id] = {}
      patient_diagnoses_dict[patient_id][col] = True
  
  # do the same for the columns above
  for col in ['circulatory system', 'congenital anomalies', 'dermatologic', 'digestive', 'endocrine/metabolic', 'genitourinary', 'hematopoietic', 'infectious diseases', 'injuries & poisonings','mental disorders','musculoskeletal', 'neoplasms', 'neurological', 'pregnancy complications','respiratory','sense organs','symptoms', 'Unknown']:
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
    patient_demographic[patient_id] = (race, gender, fracture)
    
  if (fracture):
    patient_demographic[patient_id] = (race, gender, fracture)
  
# create a new datafram with the same columns as patient_diagnoses_file
patient_data_file = pd.DataFrame(columns=patient_diagnoses_file.columns)

count = 0
for key in patient_data.keys():
  
  (race, gender, fracture) = patient_demographic[key]
  
  if (fracture):
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
    
    for col in patient_diagnoses_dict[key]:
      patient_data_file.at[count, col] = True
    
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
patient_data_file.to_csv(copyTitle + '/frature_patients2.csv', index=False)