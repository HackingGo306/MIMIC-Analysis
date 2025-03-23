import pandas as pd
import numpy as np

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

patients_file = pd.read_csv(copyTitle + '/Old Diagnosis Files/patient_diagnoses_phecode_category 1.2.csv')

patient_categories = {
  
}

data = []

for i in range(len(patients_file)):
  if ((i + 0) % 100000 == 0):
    print(100 * (i / len(patients_file)), "percent")
    
  category = patients_file.at[i, 'category']
  if (pd.isna(category)):
    category = 'Unknown'
  patient_id = patients_file.at[i, 'subject_id']
  
  if patient_id not in patient_categories:
    patient_categories[patient_id] = {}
    patient_categories[patient_id][category] = True
    data.append({'subject_id': patient_id, 'category': category})
  else:
    if (category in patient_categories[patient_id]):
      continue
    else:
      patient_categories[patient_id][category] = True
      # Add the current row of this dataframe to the new dataframe
      data.append({'subject_id': patient_id, 'category': category})
    

# Convert the list of dictionaries to a dataframe
patient_categories_df = pd.DataFrame(data)
      
# Write patient_categories_df to a new file
patient_categories_df.to_csv(copyTitle + '/patient_diagnosis_distribution2.csv', index=False)