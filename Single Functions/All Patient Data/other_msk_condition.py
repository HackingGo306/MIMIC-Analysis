# Like add_diagnosis_category.py, this file categorizes all diagnoses except Malunion is not included as Msk.
# This makes the model predictions more practical/realistic

# Using the output from phecodes.py, add into 17 or 18 true/false diagnosis columns

import pandas as pd

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

patient_demographics = pd.read_csv(copyTitle + "/All Patient Data/all_patient_data2.csv")
patient_phecodes = pd.read_csv(copyTitle + "/All Patient Data/all_patient_phecodes.csv")

phecode_categories = pd.read_csv(folderTitle + "/phecode_definitions1.2.csv")
categorizer = {
  
}

for i in range(len(phecode_categories)):
  phecode = str(phecode_categories['phecode'][i])
  category = phecode_categories['category'][i]
  if (phecode == "733.8"):
    print("Mal\n\n\n\n\n")
    continue
  categorizer[phecode] = category
  
selected_categories = [
  "circulatory system",
  "congenital anomalies", 
  "dermatologic", 
  "digestive",
  "endocrine/metabolic",
  "genitourinary", 
  "hematopoietic", 
  "infectious diseases",
  "injuries & poisonings",
  "mental disorders",
  "musculoskeletal",
  "neoplasms",
  "neurological",
  "pregnancy complications",
  "respiratory",
  "sense organs",
  "symptoms"
]
include = {}
for cat in selected_categories:
  include[cat] = True
  patient_demographics[cat] = False

patient_data = {
  
}

for i in range(len(patient_phecodes)):
  if (i % 10000 == 0):
    print("Part 1:",(i/len(patient_phecodes) * 100),"% percent")
  subject_id = str(patient_phecodes['subject_id'][i])
  if (pd.isna(patient_phecodes['phecodes'][i])): continue
  patient_data[subject_id] = {}
  try:
    phecodes = str(patient_phecodes['phecodes'][i]).split(", ")
    for phecode in phecodes: 
      category = categorizer[phecode]
      if (category in include):
        patient_data[subject_id][category] = True
  except KeyError:
    pass
    # Some phecodes aren't in the category despite being in the phecode map
      
for i in range(len(patient_demographics)):
  if (i % 10000 == 0):
    print("Part 2:",(i/len(patient_demographics) * 100),"% percent")
  subject_id = str(patient_demographics['subject_id'][i])
  try:
    for category in patient_data[subject_id].keys():
      patient_demographics.at[i, category] = True
  except KeyError:
    pass # Not all patients have phecode diagnoses
    
patient_demographics.to_csv(copyTitle + "/All Patient Data/all_patient_data3.csv", index=False)