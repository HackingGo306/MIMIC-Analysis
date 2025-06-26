# Inside the file with all the patient lab median values, add another column to specify if that patient has a malunion

import pandas as pd

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

read_file = pd.read_csv(copyTitle + '/Lab Events/patient_lab_medians.csv')
malunion_file = pd.read_csv(copyTitle + '/All Patient Data/malunion_extracted.csv')

malunion_patients = {
  
}

for i in range(len(malunion_file)):
  subject_id = malunion_file['subject_id'][i]
  malunion_patients[subject_id] = True
  
for i in range(len(read_file)):
  subject_id = read_file['subject_id'][i]
  if (subject_id in malunion_patients):
    read_file.at[i, 'malunion'] = True
  else:
    read_file.at[i, 'malunion'] = False
    
read_file.to_csv(copyTitle + '/Lab Events/patient_lab_medians_with_malunion.csv', index=False)