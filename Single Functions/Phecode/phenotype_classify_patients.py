import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

diagnosis_categories = pd.read_csv(copyTitle + '/d_icd_diagnoses_phenotype_category 1.2.csv')
diagnosis_file = pd.read_csv(copyTitle + '/patient_diagnoses.csv')

categories = {
  
}

for i in range(len(diagnosis_categories)):
  icd_code = diagnosis_categories['icd_code'][i]
  category = diagnosis_categories['category'][i]
  categories[icd_code] = category

for i in range(len(diagnosis_file)):
  code = diagnosis_file['icd_code'][i]
  if (i % 100000 == 0):
    print(100 * (i / len(diagnosis_file)), "percent [part 1]")
  category = categories[code]
  
  diagnosis_file.at[i, 'category'] = category
  
  
# Write diagnosis_file
header = list(diagnosis_file.columns)
diagnosis_file.to_csv(copyTitle + '/patient_diagnoses_phecode_category 1.2.csv', columns = header)