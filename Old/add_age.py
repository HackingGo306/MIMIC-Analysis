import pandas as pd
import numpy as np
from datetime import datetime

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

def add_age_column():
  file = pd.read_csv(copyTitle + '/patient_data.csv')
  subject_ids = file['subject_id']
  measurement_dates = file['w_time']
  file2 = pd.read_csv(folderTitle + '/patients.csv')
  patient_ids = file2['subject_id']
  anchor_ages = file2['anchor_age']
  anchor_dates = file2['anchor_year']
  subjects = {}
  
  print(len(file2))
  for i in range(len(file2)):
    subject_id = patient_ids[i]
    anchor_date = datetime.strptime(str(anchor_dates[i]), '%Y')

    subjects[subject_id] = (anchor_date, anchor_ages[i])
    
  for i in range(len(file)):
    if (i % 10000 == 0):
      print(100 * (i / len(file)), "percent")
    subject_id = subject_ids[i]
    if subject_id in subjects:
      anchor_date, anchor_age = subjects[subject_id]
      age = (datetime.strptime(measurement_dates[i], '%Y-%m-%d') - anchor_date).days // 365.25
      age += anchor_age
      file.at[i, 'age'] = age
    else:
      print(f'No age data found for subject {subject_id}')
      
  cols = file.columns.tolist()
  cols = cols[:8] + cols[-1:] + cols[8:-1]
  file = file[cols]
  # save to file
  file.to_csv(copyTitle + '/patient_data.csv', index=False)
  
add_age_column()