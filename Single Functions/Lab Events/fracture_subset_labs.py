import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

lab_items = pd.read_csv(folderTitle + '/d_labitems.csv')
lab_item_frequencies = pd.read_csv(copyTitle + '/Lab Events/patient_labs.csv')

categories = ['Pathologic fracture', 'Pathologic fracture of femur', 'Pathologic fracture of vertebrae', 'Malunion and nonunion of fracture', 'Stress fracture']
for category in categories:
  fracture_patients = pd.read_csv(copyTitle + '/Control Unmatched/' + category + ' subset.csv')
  fracture_patients = fracture_patients[fracture_patients['batch'].isna()]
  fracture_patient_ids = fracture_patients['subject_id'].unique()
  # make it into a dictionary of true/false
  fracture_patient_dict = {id: True for id in fracture_patient_ids}

  lab_item_frequencies_subset = lab_item_frequencies[lab_item_frequencies['subject_id'].isin(fracture_patient_ids)]
  lab_item_frequencies_subset = lab_item_frequencies_subset.reset_index(drop=True)
  
  freq = {
    
  }
  
  # loop through rows
  for i in range(len(lab_item_frequencies)):
    if (lab_item_frequencies['subject_id'][i] in fracture_patient_dict):
        # loop through columns
        for col in lab_item_frequencies.columns:
            if (col == 'subject_id'):
                continue
            else:
              if (pd.isna(lab_item_frequencies.at[i, col])):
                continue
              if (col not in freq):
                freq[col] = 0
              freq[col] += lab_item_frequencies[col][i]
              
  # turn freq into file
  file = pd.DataFrame(columns = ['itemid', 'count'])
  for itemid, count in freq.items():
    file.loc[len(file)] = [itemid, count]
  file.to_csv(copyTitle + '/Lab Events/Subset Distributions/' + category + '_lab_item_frequency.csv', index=False)
  

freq = {}
# Do one for everything
for i in range(len(lab_item_frequencies)):
  if ((i + 1) % (len(lab_item_frequencies) // 10) == 0):
    print(f"Progress: {i}/{len(lab_item_frequencies)}")
  for col in lab_item_frequencies.columns:
      if (col == 'subject_id'):
          continue
      else:
        if (pd.isna(lab_item_frequencies.at[i, col])):
          continue
        if (col not in freq):
          freq[col] = 0
        freq[col] += lab_item_frequencies[col][i]
            
# turn freq into file
file = pd.DataFrame(columns = ['itemid', 'count'])
for itemid, count in freq.items():
  print(itemid, count)
  file.loc[len(file)] = [itemid, count]
file.to_csv(copyTitle + '/Lab Events/Subset Distributions/' +  'all_lab_item_frequency.csv', index=False)