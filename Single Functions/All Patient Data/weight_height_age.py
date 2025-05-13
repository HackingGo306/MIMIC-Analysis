# Gets the median weight, height, and age for each patient

import pandas as pd
import numpy as np
import statistics

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

file = pd.read_csv(folderTitle + "/patients.csv")

patient_data = {
  
}

for i in range(len(file)):
  subject_id = file['subject_id'][i]
  gender = file['gender'][i]
  
  if (not (subject_id in patient_data)):
    patient_data[subject_id] = {}
    
    
  patient_data[subject_id]['gender'] = gender

weight_file = pd.read_csv(copyTitle + "/Old Corrected Weight and Height/omr Weight_lb.csv")
height_file = pd.read_csv(copyTitle + "/Old Corrected Weight and Height/omr Height_in.csv")

for i in range(len(weight_file)):
  subject_id = weight_file['subject_id'][i]
  value = weight_file['result_value'][i]
  
  if (type(value) == str): continue
  
  if ('weight' not in patient_data[subject_id]):
    patient_data[subject_id]['weight'] = []
    
  patient_data[subject_id]['weight'].append(value)
  
  
for i in range(len(height_file)):
  subject_id = height_file['subject_id'][i]
  value = height_file['result_value'][i]
  
  if (type(value) == str): continue
  
  if ('height' not in patient_data[subject_id]):
    patient_data[subject_id]['height'] = []
    
  patient_data[subject_id]['height'].append(value)
  
  
data = []
  
for subject_id in patient_data:
  if ('weight' in patient_data[subject_id]):
    weight_val = patient_data[subject_id]['weight']
  else:
    weight_val = [-1]
  if ('height' in patient_data[subject_id]):
    height_val = patient_data[subject_id]['height']
  else:
    height_val = [-1]
  
  gender_val = patient_data[subject_id]['gender']
  row = {'subject_id': subject_id, 'gender': gender_val, 'weight': statistics.median(weight_val), 'height': statistics.median(height_val)}
  data.append(row)
  
output_file = pd.DataFrame(data)

output_file.to_csv(copyTitle + "/all_patient_data.csv", index=False)