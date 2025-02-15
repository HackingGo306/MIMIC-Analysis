import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

lab_items = pd.read_csv(folderTitle + '/d_labitems.csv')
lab_item_frequencies = pd.read_csv(copyTitle + '/Lab Events/labevents_distribution.csv')

patients = {
  
}

frequency = {
  
}

for i in range(len(lab_item_frequencies)):
  lab_id = lab_item_frequencies['itemid'][i]
  try:
    frequency[int(lab_id)] = lab_item_frequencies['N Rows'][i]
  except ValueError:
    print(f"Non-numeric value found for lab ID: {lab_id}")
    continue

print("Start")
  
amount = 0
batch_size = 15000000
  
for df in pd.read_csv(copyTitle + '/Lab Events/labevents_with_labels_1.csv', chunksize=batch_size):
  for i in range(len(df)):
    if (i % 1500000 == 0):
      print(100 * (i / len(df)), "percent, ", end='')
      
    index = i + amount * batch_size
    lab_id = df.at[index, 'itemid']
    
    try: 
      if (frequency[lab_id] < 500000):
        continue
    except KeyError:
      print(f"Lab ID not found in frequency: {lab_id}")
      continue
    
    patient_id = df['subject_id'][index]
    
    if (patient_id in patients):
      if (lab_id in patients[patient_id]):
        patients[patient_id][lab_id] += 1
      else:
        patients[patient_id][lab_id] = 1
    else:
      patients[patient_id] = {lab_id: 1}
      
  amount += 1
  print(amount, "read")
  
  
print(len(patients.items()))

# create dataframe
patient_labs = pd.DataFrame(columns=['subject_id'])

count = 0
for patient_id, lab_counts in patients.items():
  patient_labs.at[count, 'subject_id'] = patient_id
  for lab_id, val in lab_counts.items():
    patient_labs.at[count, lab_id] = val
    
  count += 1
  

# Write it to a file inside hosp copy
patient_labs.to_csv(copyTitle + '/Lab Events/patient_labs_subset1.csv', index=False)
print("Finished")