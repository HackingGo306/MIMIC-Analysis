# Matching function for the new patient data master sheet

import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

bank = pd.read_csv(copyTitle + "/Master Patient Data/unique_patient_data_merged_fracture.csv")
bank = bank[bank["Malunion and nonunion of fracture"] == False]
fractures = pd.read_csv(copyTitle + "/Master Patient Data/unique_patient_data_merged_malunion.csv")

# for each row in fractures, check if the patient's data is in the bank_data dictionary  
patient_data_file = pd.DataFrame(columns=bank.columns)

def match_patients(columns, datatypes, relax_intervals, relaxation_threshold = 15, filename = 'fracture_patients_matched'):
  global patient_data_file
  global bank
  max_tolerance = 0
  for i, row in fractures.iterrows():
    if (i % 100 == 0): 
      print(f'Progress: {100 * (i / len(fractures))} percent')
      
    patient_id = row['subject_id']
    relaxation = 0
    relaxed = False
    found = False
    while (not found):
      subset = bank
      for j, col in enumerate(columns):
        new_subset = subset
        if (datatypes[j] == "boolean" or datatypes[j] == "string"):
          new_subset = subset[subset[col] == row[col]]
        elif (datatypes[j] == "integer"):
          if (relaxation == 0):
            new_subset = subset[(subset[col].round(1) == round(row[col]))]
          else:
            new_subset = subset[(subset[col] >= row[col] - (relaxation * relax_intervals[j])) & (subset[col] <= row[col] + (relaxation * relax_intervals[j]))]
        
        subset = new_subset
        
        if (len(new_subset) == 0):
          if (datatypes[j] == "integer"):
            if (relaxation > relaxation_threshold):
              found = True
              break
            # relax the number parameters
            relaxation += 1
            relaxed = True
            break
          else:
            found = True
            break
      

      if (len(subset) > 0):
        patient_data_file.loc[i] = subset.iloc[0]
        remove_id = subset.iloc[0]['subject_id']
        bank = bank[bank['subject_id'] != remove_id]
        # add current patient_id to new column
        patient_data_file.loc[i, 'relaxed'] = relaxation
        max_tolerance = max(relaxation, max_tolerance)
        patient_data_file.loc[i, 'matched_with'] = patient_id
        found = True
      elif (not relaxed):
        print(patient_id, "not found")
        patient_data_file.loc[i] = pd.Series(dtype="float64")
        patient_data_file.loc[i, 'matched_with'] = patient_id
        found = True
        
      relaxed = False
    
    
  patient_data_file.to_csv(copyTitle + '/' + filename, index=False)
  return max_tolerance
  
tolerance = 150
for z in range(10):
  print("\n--------------------------------", (z + 1), "--------------------------------\n")
  max_tol = match_patients(['race', 'gender', 'age', 'weight', 'height'], ['string', 'string', 'integer', 'integer', 'integer'], [0, 0, 0.3, 1, 0.6], tolerance, 'Master Patient Data/Control Group 3/batch' + str(z + 1) + '.csv')
  # tolerance = max_tol + min(15, round(0.5 * tolerance)) 