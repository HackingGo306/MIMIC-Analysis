# Add specific phecode_string columns (true/false) to the output of the add_diagnosis_categories.py file

import pandas as pd

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

patient_demographics = pd.read_csv(copyTitle + "/All Patient Data/all_patient_data.csv")
patient_phecodes = pd.read_csv(copyTitle + "/All Patient Data/all_patient_phecodes.csv")

phecode_map = pd.read_csv(folderTitle + "/phecode_map1.2.csv")
categorizer = {
  
}

for i in range(len(phecode_map)):
  phecode = str(phecode_map['Phecode'][i])
  phecode_string = phecode_map['PhecodeString'][i]
  categorizer[phecode] = phecode_string

patient_data = {
  
}

selected_categories = ['Pathologic fracture', 'Pathologic fracture of femur', 'Pathologic fracture of vertebrae', 'Malunion and nonunion of fracture', 'Fracture of tibia and fibula', 'Fracture of lower limb', 'Stress fracture', 'Fracture of unspecified part of femur', 'Fracture of neck of femur', 'Fracture of ankle and foot', 'Fracture of radius and ulna', 'Fracture of vertebral column without mention of spinal cord injury', 'Fracture of hand or wrist']
include = {}
for cat in selected_categories:
  include[cat] = True
  patient_demographics[cat] = False

for i in range(len(patient_phecodes)):
  if (i % 10000 == 0):
    print("Part 1:",(i/len(patient_phecodes) * 100),"% percent")
  subject_id = str(patient_phecodes['subject_id'][i])
  if (pd.isna(patient_phecodes['phecodes'][i])): continue
  patient_data[subject_id] = {}
  try:
    phecode_strings = str(patient_phecodes['phecodes'][i]).split(", ")
    for string in phecode_strings: 
      phecode_string = categorizer[string]
      if (phecode_string in include):
        patient_data[subject_id][phecode_string] = True
  except KeyError:
    pass
  
for i in range(len(patient_demographics)):
  if (i % 10000 == 0):
    print("Part 2:",(i/len(patient_demographics) * 100),"% percent")
  subject_id = str(patient_demographics['subject_id'][i])
  try:
    for category in patient_data[subject_id].keys():
      patient_demographics.at[i, category] = True 
  except KeyError:
    pass # Not all patients have phecode diagnoses
    
# Remove first column (column 1)
patient_demographics.drop("Unnamed: 0", axis=1, inplace=True)
patient_demographics.to_csv(copyTitle + "/All Patient Data/all_patient_data2s.csv", index=False)