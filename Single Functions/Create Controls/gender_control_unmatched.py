import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

def create_pool(fracture_index = 0, pool_num = 0, gender = 'M'):

  version = '3.0'
  folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
  copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'


  categories = ['Pathologic fracture', 'Pathologic fracture of femur', 'Pathologic fracture of vertebrae', 'Malunion and nonunion of fracture', 'Stress fracture']
  category_name = categories[fracture_index]

  fracture_patients = pd.read_csv(copyTitle + '/Control Unmatched/' + category_name + ' subset.csv')
  # keep all the rows where the column is NA
  fracture_patients = fracture_patients[fracture_patients['matched_with'].isna()]
  fracture_patients = fracture_patients[fracture_patients['gender'] == gender]

  # count rows in fracture_patients
  fracture_patient_count = len(fracture_patients)

  bank = pd.read_csv(copyTitle + '/patient_matching_bank.csv')
  
  bank = bank[bank['gender'] == gender]
  bank = bank.reset_index(drop=True)

  subset_size = fracture_patient_count * 1

  # create a new dataframe with the same columns as the bank
  bank_subset = pd.DataFrame(columns=bank.columns)

  added = 0
  used_ids = {}
  # choose subset_size number of unique patients from the bank
  while (added < subset_size):
    if (added % 100 == 0):
      print(added, "of", subset_size, len(bank))
    # choose a random row
    random_index = np.random.randint(0, len(bank))
    
    try:
      random_patient_id = bank.loc[int(random_index), 'subject_id']
      if (random_patient_id in used_ids):
        continue
      used_ids[random_patient_id] = True
      added += 1
    except KeyError:
      print("Key Error:", random_index, len(bank))
      continue
    
    # append one row to the subset
    bank_subset.loc[len(bank_subset)] = bank.loc[random_index]

  for i in range(len(bank_subset)):
    weight = bank_subset.loc[i, 'weight']
    height = bank_subset.loc[i, 'height']
    # calculate bmi when weight is in pounds and height is in inches
    bmi = weight * 703 / (height ** 2)
    bank_subset.loc[i, 'bmi'] = round(bmi, 2)
      
  # append the bank_subset to the bottom of the table
  fracture_patients = pd.concat([fracture_patients, bank_subset])
      
  # fill any_fracture column na with False
  fracture_patients['any_fracture'].fillna(False, inplace=True)

  # fillna column race with "Other"
  fracture_patients['race'].fillna('Other', inplace=True)

  # drop columns
  fracture_patients.drop(columns=['batch', 'matched_with', 'relaxed'], inplace=True)
  
  cols = fracture_patients.columns.tolist()
  cols = cols[:3] + cols[4:] + cols[3:4]
  fracture_patients = fracture_patients[cols]

  # write
  fracture_patients.to_csv(copyTitle + '/Control Semi-Matched/Gender Separated/' + category_name + '/Compare Group/' + gender + str(pool_num) + '.csv', index=False)

for i in range(3, 4):
  for j in range(1,4):
    create_pool(i, j, 'F')
    create_pool(i, j, 'M')