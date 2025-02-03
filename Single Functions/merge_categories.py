import pandas as pd

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

file = pd.read_csv(copyTitle + '/icd_codes_with_categories.csv')
icd_version = file['icd_version']
icd_category = file['category']

for i in range(len(icd_version)):
  category = icd_category[i]
  if (category == "certain infectious and parasitic diseases"):
    file.at[i, 'category'] = "infectious and parasitic diseases"
  if (category == "symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified"):
    file.at[i, 'category'] = "symptoms, signs, and ill-defined conditions"
  if (category == "congenital malformations, deformations and chromosomal abnormalities"):
    file.at[i, 'category'] = "congenital anomalies"
  if (category == "complications of pregnancy, childbirth, and the puerperium"):
    file.at[i, 'category'] = 'pregnancy, childbirth and the puerperium'
  if (category == "mental, behavioral and neurodevelopmental disorders"):
    file.at[i, 'category'] = 'mental disorders'
  if (category == "diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism"):
    file.at[i, 'category'] = 'diseases of the blood and blood-forming organs'
  if (category == "diseases of the nervous system and sense organs"):
    file.at[i, 'category'] = 'diseases of the nervous system'
  if (category == "endocrine, nutritional and metabolic diseases, and immunity disorders"):
    file.at[i, 'category'] = 'endocrine, nutritional and metabolic diseases'
  if (category == "injury and poisoning" or category == "injury, poisoning and certain other consequences of external causes" or category == "external causes of morbidity" or category == "external causes of injury and supplemental classification"):
    file.at[i, 'category'] = 'external causes such as injury, morbidity, and poisoning'
  

file.to_csv(copyTitle + '/d_icd_diagnoses_merged.csv', index=False)