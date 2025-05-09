# Edit the batch number column
# Mal, B1, B2, B3, ...

import pandas as pd

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

file = pd.read_csv(copyTitle + '/Master Patient Data/Malunion General Control Group 2/train_data_2.csv')

for i in range(len(file)):
  batch_val = file['batch'][i]
  if (pd.isna(batch_val)):
    file['batch'][i] = "Mal"
  else:
    file['batch'][i] = "B" + str(int(batch_val))
  
# write
file.to_csv(copyTitle + '/Master Patient Data/train_data_2.csv', index=False)