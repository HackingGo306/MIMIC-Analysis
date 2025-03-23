import pandas as pd
import numpy as np

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

patients_file = pd.read_csv(copyTitle + '/Old Diagnosis Files/patient_diagnoses_phecode_category 1.2.csv')

patient_diagnoses = {
  
}

for i in range(0, 1000000):
  if (i % 100000 == 0):
    print(100 * (i / len(patients_file)), "percent")
    
  category = patients_file.at[i, 'category']
  if (pd.isna(category)):
    category = 'Unknown'
  patient_id = patients_file.at[i, 'subject_id']
  
  if patient_id not in patient_diagnoses:
    patient_diagnoses[patient_id] = {}
  patient_diagnoses[patient_id][category] = True


# Create a new dataframe with the diagnoses as individual columns
patient_diagnoses_df = pd.DataFrame()

row_count = 0
for subject_id in patient_diagnoses:
  for category in patient_diagnoses[subject_id]:
    patient_diagnoses_df.at[row_count, 'subject_id'] = subject_id
    patient_diagnoses_df.at[row_count, category] = True
  row_count += 1
  if (row_count % 10000 == 0):
    print(100 * (row_count / len(patient_diagnoses)), "percent")
    
patient_diagnoses_df = patient_diagnoses_df.fillna(False)

# Write patient_diagnoses_df to a new file
patient_diagnoses_df.to_csv(copyTitle + '/patient_diagnosis_categories.csv', index=False)

print("Done")