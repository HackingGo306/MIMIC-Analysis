import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

file = pd.read_csv(copyTitle + '/Control Group 2/train_data_2.csv')

categories = ['Pathologic fracture', 'Pathologic fracture of femur', 'Pathologic fracture of vertebrae', 'Malunion and nonunion of fracture', 'Stress fracture']

for category in categories:
  patient_ids = []
  new_file = pd.DataFrame(columns=file.columns)
  for i in range(1670):
    row = file.loc[i]
    if (row[category]):
      patient_ids.append(row['subject_id'])
    
  count = 0
  for i in range(len(file)):
    row = file.loc[i]
    if (row['matched_with'] in patient_ids) or (row['subject_id'] in patient_ids):
      new_file.loc[count] = file.loc[i]
      count += 1
    
  # write
  new_file.to_csv(copyTitle + '/' + 'Control Group 2/' + category + ' subset.csv', index = False)
  print(category)