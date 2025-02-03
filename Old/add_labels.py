import pandas as pd
import numpy as np
from datetime import datetime

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

def add_labels():
  file = pd.read_csv(copyTitle + '/patient_data copy.csv')
  
  file.drop("Infectious Diseases", axis = 1, inplace = True)
  file.drop("Cardiovascular Diseases", axis = 1, inplace = True)
  file.drop("Respiratory Diseases", axis = 1, inplace = True)
  file.drop("Neurological Disorders", axis = 1, inplace = True)
  file.drop("Endocrine and Metabolic Disorders", axis = 1, inplace = True)
  file.drop("Musculoskeletal Disorders", axis = 1, inplace = True)
  file.drop("Gastrointestinal Diseases", axis = 1, inplace = True)
  file.drop("Hematological Disorders", axis = 1, inplace = True)
  file.drop("Dermatological Conditions", axis = 1, inplace = True)
  file.drop("Psychiatric and Mental Health Disorders", axis = 1, inplace = True)
  file.drop("Cancers (Oncology)", axis = 1, inplace = True)
  file.drop("Autoimmune Diseases", axis = 1, inplace = True)
  file.drop("Genetic and Congenital Disorders", axis = 1, inplace = True)
  file.drop("Eye and Vision Disorders", axis = 1, inplace = True)
  file.drop("Ear, Nose, and Throat (ENT) Disorders", axis = 1, inplace = True)
  file.drop("Renal and Urological Disorders", axis = 1, inplace = True)
  file.drop("Reproductive System Disorders", axis = 1, inplace = True)
  file.drop("Rare and Orphan Diseases", axis = 1, inplace = True)
  
  for i in range(len(file)):
    if (i % 5000 == 0):
      print(i / len(file) * 100, "percent")
    
    file.at[i, 'circulatory system'] = False
    file.at[i, 'congenital anomalies'] = False
    file.at[i, 'dermatologic'] = False
    file.at[i, 'digestive'] = False
    file.at[i, 'endocrine/metabolic'] = False
    file.at[i, 'genitourinary'] = False
    file.at[i, 'hematopoietic'] = False
    file.at[i, 'infectious diseases'] = False
    file.at[i, 'injuries & poisonings'] = False
    file.at[i, 'mental disorders'] = False
    file.at[i, 'musculoskeletal'] = False
    file.at[i, 'neoplasms'] = False
    file.at[i, 'neurological'] = False
    file.at[i, 'pregnancy complications'] = False
    file.at[i, 'respiratory'] = False
    file.at[i, 'sense organs'] = False
    file.at[i, 'symptoms'] = False
    file.at[i, 'Unknown'] = False
    
  file.to_csv(copyTitle + '/patient_data_phecode.csv', index=False)

add_labels()

'''

circulatory system
congenital anomalies
dermatologic
digestive
endocrine/metabolic
genitourinary
hematopoietic
infectious diseases
injuries & poisonings
mental disorders
musculoskeletal
neoplasms
neurological
pregnancy complications
respiratory
sense organs
symptoms
Unknown

'''