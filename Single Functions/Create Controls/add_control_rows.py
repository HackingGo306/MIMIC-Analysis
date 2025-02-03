import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

file = pd.read_csv(copyTitle + '/fracture_patients.csv')

for i in range(15):
  appending = pd.read_csv(copyTitle + '/Control Group 2/' + 'batch' + str(i + 1) + '.csv')
  appending['batch'] = (i + 1)
  # append this file to the end of file
  file = pd.concat([file, appending])
  
# write
file.to_csv(copyTitle + '/train_data_2.csv', index=False)