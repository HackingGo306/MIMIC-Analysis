import pandas as pd
import numpy as nps
from datetime import datetime
from datetime import timedelta

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

def addBMICol():
  file = pd.read_csv(copyTitle + '/Control Group 4/Pathologic fracture unmatched.csv')
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
  file.to_csv(copyTitle + '/Control Group 4/Pathologic fracture unmatched.csv', index=False)
  
addBMICol()