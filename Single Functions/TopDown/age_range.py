import pandas as pd
import numpy as np

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

patients_file = pd.read_csv(folderTitle + '/patients.csv')

# Calculate current age range (as of 2025)
for i in range(len(patients_file)):
  if (i % 10000 == 0):
    print(100 * (i / len(patients_file)), "percent")
    
  anchor_age =  patients_file.at[i, 'anchor_age']
  anchor_year = patients_file.at[i, 'anchor_year_group']
  min_year = anchor_year.split(' - ')[0]
  max_year = anchor_year.split(' - ')[1]
  current_year = 2025
  
  current_min = current_year - int(max_year) + anchor_age
  current_max = current_year - int(min_year) + anchor_age
  
  patients_file.at[i, '2025_min_age'] = current_min
  patients_file.at[i, '2025_max_age'] = current_max
  patients_file.at[i, '2025_estimate_age'] = (current_max + current_min) / 2
  
# Save to file
patients_file.to_csv(copyTitle + '/patient_ages.csv', index=False)