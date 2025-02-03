import pandas as pd

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

file = pd.read_csv(folderTitle + '/d_icd_diagnoses.csv')
icd_version = file['icd_version']
icd_code = file['icd_code']


def categorize_icd_code(icd_code): # Version 10 only
    icd_code = icd_code[:3]
    # Define the categories and their ranges
    if "A00" <= icd_code <= "B99":
        return 'certain infectious and parasitic diseases'
    elif "C00" <= icd_code <= "D49":
        return 'neoplasms'
    elif "D50" <= icd_code <= "D89":
        return 'diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism'
    elif "E00" <= icd_code <= "E89":
        return 'endocrine, nutritional and metabolic diseases'
    elif "F01" <= icd_code <= "F99":
        return 'mental, behavioral and neurodevelopmental disorders'
    elif "G00" <= icd_code <= "G99":
        return 'diseases of the nervous system'
    elif "H00" <= icd_code <= "H59":
        return 'diseases of the eye and adnexa'
    elif "H60" <= icd_code <= "H95":
        return 'diseases of the ear and mastoid process'
    elif "I00" <= icd_code <= "I99":
        return 'diseases of the circulatory system'
    elif "J00" <= icd_code <= "J99":
        return 'diseases of the respiratory system'
    elif "K00" <= icd_code <= "K95":
        return 'diseases of the digestive system'
    elif "L00" <= icd_code <= "L99":
        return 'diseases of the skin and subcutaneous tissue'
    elif "M00" <= icd_code <= "M99":
        return 'diseases of the musculoskeletal system and connective tissue'
    elif "N00" <= icd_code <= "N99":
        return 'diseases of the genitourinary system'
    elif "O00" <= icd_code <= "O9A":
        return 'pregnancy, childbirth and the puerperium'
    elif "P00" <= icd_code <= "P96":
        return 'certain conditions originating in the perinatal period'
    elif "Q00" <= icd_code <= "Q99":
        return 'congenital malformations, deformations and chromosomal abnormalities'
    elif "R00" <= icd_code <= "R99":
        return 'symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified'
    elif "S00" <= icd_code <= "T88":
        return 'injury, poisoning and certain other consequences of external causes'
    elif "U00" <= icd_code <= "U85":
        return 'codes for special purposes'
    elif "V00" <= icd_code <= "Y99":
        return 'external causes of morbidity'
    elif "Z00" <= icd_code <= "Z99":
        return 'factors influencing health status and contact with health services'
    else:
        return 'unknown'

for i in range(len(icd_version)):
  if (icd_version[i] == 9):
    code = icd_code[i][:3]
    try:
      code = int(code)
      if (code >= 0 and code < 140):
        file.at[i, 'category'] = "infectious and parasitic diseases"
      elif (code >= 140 and code < 240):
        file.at[i, 'category'] = "neoplasms"
      elif (code >= 240 and code < 280):
        file.at[i, 'category'] = "endocrine, nutritional and metabolic diseases, and immunity disorders"
      elif (code >= 280 and code < 290):
        file.at[i, 'category'] = "diseases of the blood and blood-forming organs"
      elif (code >= 290 and code < 320):
        file.at[i, 'category'] = "mental disorders"
      elif (code >= 320 and code < 390):
        file.at[i, 'category'] = "diseases of the nervous system and sense organs"
      elif (code >= 390 and code < 460):
        file.at[i, 'category'] = "diseases of the circulatory system"
      elif (code >= 460 and code < 520):
        file.at[i, 'category'] = "diseases of the respiratory system"
      elif (code >= 520 and code < 580):
        file.at[i, 'category'] = "diseases of the digestive system"
      elif (code >= 580 and code < 630):
        file.at[i, 'category'] = "diseases of the genitourinary system"
      elif (code >= 630 and code < 680):
        file.at[i, 'category'] = "complications of pregnancy, childbirth, and the puerperium"
      elif (code >= 680 and code < 710):
        file.at[i, 'category'] = "diseases of the skin and subcutaneous tissue"
      elif (code >= 710 and code < 740):
        file.at[i, 'category'] = "diseases of the musculoskeletal system and connective tissue"
      elif (code >= 740 and code < 760):
        file.at[i, 'category'] = "congenital anomalies"
      elif (code >= 760 and code < 780):
        file.at[i, 'category'] = "certain conditions originating in the perinatal period"
      elif (code >= 780 and code < 800):
        file.at[i, 'category'] = "symptoms, signs, and ill-defined conditions"
      elif (code >= 800 and code < 1000):
        file.at[i, 'category'] = "injury and poisoning"
    except ValueError:
      file.at[i, 'category'] = "external causes of injury and supplemental classification"
  if (icd_version[i] == 10):
    file.at[i, 'category'] = categorize_icd_code(icd_code[i])
      
# write the file
file.to_csv(copyTitle + '/icd_codes_with_categories.csv', index=False)