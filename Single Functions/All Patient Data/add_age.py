# Adds age
# Extracts median age for each patient
# uses patient file and difference from the weight (and height) measurement dates
# adds to a list and then takes the median for each patient

import pandas as pd
import numpy as np
from datetime import datetime
import statistics

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

patient_ages = {}

def get_age_data(measurement_file):
  file = pd.read_csv(copyTitle + '/Old Corrected Weight and Height/' + measurement_file)
  subject_ids = file['subject_id']
  measurement_dates = file['chartdate']
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
      
      if (subject_id not in patient_ages):
        patient_ages[subject_id] = []
      patient_ages[subject_id].append(age)
      
    else:
      print(f'No age data found for subject {subject_id}')
  
get_age_data('omr Weight_lb.csv')
get_age_data('omr Height_in.csv')

data_file = pd.read_csv(copyTitle + '/All Patient Data/all_patient_data2.csv')
for i in range(len(data_file)):
  patient_id = data_file['subject_id'][i]
  try: 
    median_age = statistics.median(patient_ages[patient_id])
    data_file.at[i, 'age'] = median_age
  except KeyError:
    data_file.at[i, 'age'] = -1
    
cols = data_file.columns.tolist()
cols = cols[:1] + cols[-1:] + cols[1:-1]
data_file = data_file[cols]
    
data_file.to_csv(copyTitle + '/All Patient Data/tesing.csv', index=False)