# Use the diagnosis_icd file and phecode mapping to map all phecode numbers (up to 4 for each diagnosis) to the patinents
# For each patient create a list of the phecodes they have

import pandas as pd

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

file = pd.read_csv(folderTitle + '/d_icd_diagnoses.csv')
phenocodes = pd.read_csv(folderTitle + '/phecode_definitions1.2.csv', encoding='latin-1')

categorizer = pd.read_csv(folderTitle + '/phecode_map1.2.csv', encoding='latin-1')
codes = categorizer['ICD']

diagnosis = pd.read_csv(folderTitle + "/diagnoses_icd.csv")

icd_categories = {
  
}

for i in range(len(codes)):
  if (i % 10000 == 0):
    print("Part 1:",(i/len(codes) * 100),"percent")
    
  icd_code = codes[i].replace('.', '')
  phecode = categorizer['Phecode'][i]
  
  if (icd_code in icd_categories):
    icd_categories[icd_code].append(phecode)
  else:
    try:
      icd_categories[icd_code] = [phecode]
    except KeyError:
      pass

patient_phecodes = {
  
}

for i in range(len(diagnosis)):
  if (i % 100000 == 0):
    print("Part 2:",(i/len(diagnosis) * 100),"percent")
    
  subject_id = diagnosis['subject_id'][i]
  icd_code = diagnosis['icd_code'][i]
  
  try:
    phecode = icd_categories[icd_code]
    if (subject_id not in patient_phecodes):
      patient_phecodes[subject_id] = {}
    for ele in phecode:
      patient_phecodes[subject_id][ele] = True
  except KeyError:
    pass
  

patient_data = pd.read_csv(copyTitle + "/All Patient Data/all_patient_data.csv")
for i in range(len(patient_data)):
  if (i % 10000 == 0):
    print("Part 3:",(i/len(patient_data) * 100),"percent")
  subject_id = patient_data['subject_id'][i]
  try: 
    string = ', '.join(str(x) for x in patient_phecodes[subject_id])
    patient_data.at[i, 'phecodes'] = string
  except KeyError:
    pass

patient_data.to_csv(copyTitle + "/All Patient Data/all_patient_phecodes.csv", index=False)