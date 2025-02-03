# Read the diagnoses file and set a category to True if that patient has been diagnosed with something in that category before the measurment date

import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

diagnosis_file = pd.read_csv(folderTitle + '/diagnoses_icd.csv')
diagnosis_categories = pd.read_csv(copyTitle + '/d_icd_diagnoses_merged.csv')
admission_file = pd.read_csv(folderTitle + '/admissions.csv')
data_file = pd.read_csv(copyTitle + '/patient_data.csv')
patient_diagnoses_file = pd.read_csv(copyTitle + '/patient_diagnoses.csv')

# admit_times = {
  
# }

# categories = {
  
# }

# patient_diagnoses = {
  
# }

# for i in range(len(admission_file)):
#   admit_date = admission_file['admittime'][i]
#   admit_date = datetime.strptime(admit_date, '%Y-%m-%d %H:%M:%S')

#   admit_id = admission_file['hadm_id'][i]
#   admit_times[admit_id] = admit_date
  
# for i in range(len(diagnosis_categories)):
#   icd_code = diagnosis_categories['icd_code'][i]
#   category = diagnosis_categories['category'][i]
#   categories[icd_code] = category
  
# for i in range(len(diagnosis_file)):
#   if (i % 100000 == 0):
#     print(100 * (i / len(diagnosis_file)), "percent [part 1]")
#   admit_id = diagnosis_file['hadm_id'][i]
#   if (admit_id not in admit_times):
#     continue
#   diagnosis_time = admit_times[admit_id]
#   patient_id = diagnosis_file['subject_id'][i]
#   code = diagnosis_file['icd_code'][i]
#   category = categories[code]
  
#   diagnosis_file.at[i, 'category'] = category
#   diagnosis_file.at[i, 'diagnosis_time'] = diagnosis_time
  
#   if patient_id not in patient_diagnoses:
#     patient_diagnoses[patient_id] = [(diagnosis_time, category)]
#   else:
#     patient_diagnoses[patient_id].append((diagnosis_time, category))

patient_diagnoses = {
  
}

for i in range(len(patient_diagnoses_file)):
  if (i % 100000 == 0):
    print(100 * (i / len(patient_diagnoses_file)), "percent [part 1]")  
  
  patient_id = patient_diagnoses_file['subject_id'][i]
  
  if (patient_id == 11960571 or patient_id == 11404231):
    continue
  
  diagnosis_time = patient_diagnoses_file['diagnosis_time'][i]
  diagnosis_time = datetime.strptime(diagnosis_time, '%Y-%m-%d %H:%M:%S')
  diagnosis_category = patient_diagnoses_file['category'][i]
  
  if patient_id not in patient_diagnoses:
    patient_diagnoses[patient_id] = [(diagnosis_time, diagnosis_category)]
  else:
    patient_diagnoses[patient_id].append((diagnosis_time, diagnosis_category))
  
    
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
      

# Save the updated data file
data_file.to_csv(copyTitle + '/patient_data_with_diagnosis_flags2.csv', index=False)
# diagnosis_file.to_csv(copyTitle + '/patient_diagnoses', index=False)