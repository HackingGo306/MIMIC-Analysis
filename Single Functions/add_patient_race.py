import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

admissions = pd.read_csv(folderTitle + '/admissions.csv')
patient_data = pd.read_csv(copyTitle + '/patient_data_fracture_flags.csv')

patient_races = {
  
}

for i in range(len(admissions)):
  subject_id = admissions['subject_id'][i]
  ethnicity = admissions['race'][i]
  race = 'Other'
  if (ethnicity == 'AMERICAN INDIAN/ALASKA NATIVE'):
    race = 'Native'
  if (ethnicity == 'ASIAN'):
    race = 'Asian'
  if (ethnicity == 'ASIAN - ASIAN INDIAN'):
    race = 'Asian'
  if (ethnicity == 'ASIAN - CHINESE'):
    race = 'Asian'
  if (ethnicity == 'ASIAN - KOREAN'):
    race = 'Asian'
  if (ethnicity == 'ASIAN - SOUTH EAST ASIAN'):
    race = 'Asian'
  if (ethnicity == 'BLACK/AFRICAN'):
    race = 'Black'
  if (ethnicity == 'BLACK/AFRICAN AMERICAN'):
    race = 'Black'
  if (ethnicity == 'BLACK/CAPE VERDEAN'):
    race = 'Black'
  if (ethnicity == 'BLACK/CARIBBEAN ISLAND'):
    race = 'Black'
  if (ethnicity == 'HISPANIC OR LATINO'):
    race = 'Hispanic'
  if (ethnicity == 'HISPANIC/LATINO - CENTRAL AMERICAN'):
    race = 'Hispanic'
  if (ethnicity == 'HISPANIC/LATINO - COLUMBIAN'):
    race = 'Hispanic'
  if (ethnicity == 'HISPANIC/LATINO - CUBAN'):
    race = 'Hispanic'
  if (ethnicity == 'HISPANIC/LATINO - DOMINICAN'):
    race = 'Hispanic'
  if (ethnicity == 'HISPANIC/LATINO - GUATEMALAN'):
    race = 'Hispanic'
  if (ethnicity == 'HISPANIC/LATINO - HONDURAN'):
    race = 'Hispanic'
  if (ethnicity == 'HISPANIC/LATINO - MEXICAN'):
    race = 'Hispanic'
  if (ethnicity == 'HISPANIC/LATINO - PUERTO RICAN'):
    race = 'Hispanic'
  if (ethnicity == 'HISPANIC/LATINO - SALVADORAN'):
    race = 'Hispanic'
  if (ethnicity == 'MULTIPLE RACE/ETHNICITY'):
    race = 'Multiple'
  if (ethnicity == 'NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER'):
    race = 'Native'
  if (ethnicity == 'OTHER'):
    race = 'Other'
  if (ethnicity == 'PATIENT DECLINED TO ANSWER'):
    race = 'Other'
  if (ethnicity == 'PORTUGUESE'):
    race = 'White'
  if (ethnicity == 'SOUTH AMERICAN'):
    race = 'Hispanic'
  if (ethnicity == 'UNABLE TO OBTAIN'):
    race = 'Other'
  if (ethnicity == 'UNKNOWN'):
    race = 'Other'
  if (ethnicity == 'WHITE'):
    race = 'White'
  if (ethnicity == 'WHITE - BRAZILIAN'):
    race = 'White'
  if (ethnicity == 'WHITE - EASTERN EUROPEAN'):
    race = 'White'
  if (ethnicity == 'WHITE - OTHER EUROPEAN'):
    race = 'White'
  if (ethnicity == 'WHITE - RUSSIAN'):
    race = 'White'
    
  patient_races[subject_id] = race
  
# Add this column to patient_data using for loop
for i in range(len(patient_data)):
  subject_id = patient_data['subject_id'][i]
  # print(subject_id, patient_races[subject_id])
  if (subject_id not in patient_races):
    print(f'Warning: Missing race for subject_id {subject_id}')
    continue
  
  patient_data.at[i, 'race'] = patient_races[subject_id]

# re-order the columns
cols = patient_data.columns.tolist()
cols = cols[:10] + cols[-1:] + cols[10:-1]
patient_data = patient_data[cols]

# save to file
patient_data.to_csv(copyTitle + '/patient_data_fracture_flags_race.csv', index=False)