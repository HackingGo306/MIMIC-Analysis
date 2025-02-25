import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

musculoskeletal_diagnoses = pd.read_csv(copyTitle + '/Old Diagnosis Files/patient_diagnoses_musculoskeletal_phecode 1.2.csv')
categories = ['Pathologic fracture', 'Pathologic fracture of femur', 'Pathologic fracture of vertebrae', 'Malunion and nonunion of fracture', 'Stress fracture']
category = categories[3]

for z in range(1, 4):
  data_file_M = pd.read_csv(copyTitle + '/Control Semi-Matched/Gender Separated/' + category + '/1x/M' + str(z) + ".csv")
  data_file_F = pd.read_csv(copyTitle + '/Control Semi-Matched/Gender Separated/' + category + '/1x/F' + str(z) + ".csv")
  
  subject_other_msk = {
    
  }

  for i in range(0, len(musculoskeletal_diagnoses)):
    subject_id = musculoskeletal_diagnoses['subject_id'][i]
    condition = musculoskeletal_diagnoses['phecode_string'][i]
    if (condition != category):
      subject_other_msk[subject_id] = True
      
  for i in range(0, len(data_file_M)):
    subject_id = data_file_M['subject_id'][i]
    if (subject_id in subject_other_msk):
      data_file_M.at[i, 'msk not ' + category] = True
    else:
      data_file_M.at[i, 'msk not ' + category] = False
      
  cols = data_file_M.columns.tolist()
  cols = cols[:17] + cols[-1:] + cols[18:-1] + cols[17:18]
  data_file_M = data_file_M[cols]
      
  for i in range(0, len(data_file_F)):
    subject_id = data_file_F['subject_id'][i]
    if (subject_id in subject_other_msk):
      data_file_F.at[i, 'msk not ' + category] = True
    else:
      data_file_F.at[i, 'msk not ' + category] = False
      
  cols = data_file_F.columns.tolist()
  cols = cols[:17] + cols[-1:] + cols[18:-1] + cols[17:18]
  data_file_F = data_file_F[cols]
      
  data_file_M.to_csv(copyTitle + '/Control Semi-Matched/Gender Separated/' + category + '/1x/M' + str(z) + "_other.csv", index=False)
  data_file_F.to_csv(copyTitle + '/Control Semi-Matched/Gender Separated/' + category + '/1x/F' + str(z) + "_other.csv", index=False)