import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

file = pd.read_csv(copyTitle + '/Control Group 4/train_data_2.csv')

def addFractureCol():
  for i in range(len(file)):
    if (pd.isna(file['batch'][i])):
      file.at[i, 'any_fracture'] = True
    else:
      file.at[i, 'any_fracture'] = False
    
  # write
  file.to_csv(copyTitle + '/Control Group 4/train_data_2.csv', index=False)
  
def addBMICol():
  file = pd.read_csv(copyTitle + '/Control Group 4/train_data_2.csv')
  for i in range(len(file)):
    weight = file.at[i, 'weight']
    height = file.at[i, 'height']
    # calculate bmi when weight is in pounds and height is in inches
    bmi = weight * 703 / (height ** 2)
    file.at[i, 'bmi'] = round(bmi, 2)
    
  cols = file.columns.tolist()
  cols = cols[:3] + cols[-1:] + cols[3:-1]
  file = file[cols]
    
  # write
  file.to_csv(copyTitle + '/Control Group 4/train_data_2.csv', index=False)
  
addBMICol()
