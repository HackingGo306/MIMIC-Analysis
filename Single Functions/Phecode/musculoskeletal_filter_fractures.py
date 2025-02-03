import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

musculoskeletal_diagnoses = pd.read_csv(copyTitle + '/patient_diagnoses_musculoskeletal_phecode.csv')

# create a new pd datafram with the same headers
fractures = pd.DataFrame(columns=musculoskeletal_diagnoses.columns)

# only include a row from musculoskeletal_diagnoses if it contains the word "fracture"
fractures = musculoskeletal_diagnoses[musculoskeletal_diagnoses['phecode_string'].str.lower().str.contains('fracture')]

# write
fractures.to_csv(copyTitle + '/fractures.csv', index=False)