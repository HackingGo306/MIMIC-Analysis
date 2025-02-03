import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

patient_diagnoses_file = pd.read_csv(copyTitle + '/patient_diagnoses_phecode_category.csv')

# filter by category column into a new table
# category column should be equal to musculoskeletal
musculoskeletal_diagnoses = patient_diagnoses_file[patient_diagnoses_file['category'] == 'musculoskeletal']

# write
musculoskeletal_diagnoses.to_csv(copyTitle + '/patient_diagnoses_musculoskeletal.csv', index=False)