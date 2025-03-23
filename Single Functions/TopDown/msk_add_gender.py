import pandas as pd
import numpy as np
from datetime import datetime

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

def add_gender_column():
  file = pd.read_csv(copyTitle + '/Old Diagnosis Files/patient_diagnoses_musculoskeletal_phecode 1.2.csv')
  subject_ids = file['subject_id']
  file2 = pd.read_csv(folderTitle + '/patients.csv')
  patient_ids = file2['subject_id']
  patient_genders = file2['gender']
  subjects = {}
  
  print(len(file2))
  for i in range(len(file2)):
    subject_id = patient_ids[i]

    subjects[subject_id] = (patient_genders[i])
    
  for i in range(len(file)):
    if (i % 10000 == 0):
      print(100 * (i / len(file)), "percent")
    subject_id = subject_ids[i]
    if subject_id in subjects:
      file.at[i, 'gender'] = subjects[subject_id]
    else:
      print(f'No gender data found for subject {subject_id}')
      
  cols = file.columns.tolist()
  cols = cols[:9] + cols[-1:] + cols[9:-1]
  file = file[cols]
  # save to file
  file.to_csv(copyTitle + '/Old Diagnosis Files/patient_diagnoses_musculoskeletal_phecode 1.2.csv', index=False)
  
add_gender_column()