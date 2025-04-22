import pandas as pd

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

file = pd.read_csv(copyTitle + '/Master Patient Data/unique_patient_data_merged_malunion.csv')

for i in range(15):
  appending = pd.read_csv(copyTitle + '/Master Patient Data/Malunion Control Group 1/' + 'batch' + str(i + 1) + '.csv')
  appending['batch'] = (i + 1)
  # append this file to the end of file
  file = pd.concat([file, appending])
  
# write
file.to_csv(copyTitle + '/malunion_train_data_1.csv', index=False)