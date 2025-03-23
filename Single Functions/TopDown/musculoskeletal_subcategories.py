import pandas as pd
import numpy as np

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

patients_file = pd.read_csv(copyTitle + '/Old Diagnosis Files/patient_diagnoses_musculoskeletal_phecode 1.2.csv')

patient_subcategories = {
  
}

# Create a new dataframe with the same columns
patient_subcategories_df = pd.DataFrame(columns=patients_file.columns)


for i in range(len(patients_file)):
  if (i % 100000 == 0):
    print(100 * (i / len(patients_file)), "percent")
    
  patient_id = patients_file.at[i, 'subject_id']
  subcategory = patients_file.at[i, 'phecode_string']
  
  if patient_id not in patient_subcategories:
    patient_subcategories[patient_id] = {}
    patient_subcategories[patient_id][subcategory] = True
    patient_subcategories_df = patient_subcategories_df._append(patients_file.iloc[i], ignore_index=True)
  else:
    if (subcategory in patient_subcategories[patient_id]):
      continue
    else:
      patient_subcategories[patient_id][subcategory] = True
      # Add the current row of this dataframe to the new dataframe
      patient_subcategories_df = patient_subcategories_df._append(patients_file.iloc[i], ignore_index=True)
      
      
# Write patient_subcategories_df to a new file
patient_subcategories_df.to_csv(copyTitle + '/patient_msk_subcategories.csv', index=False)
    