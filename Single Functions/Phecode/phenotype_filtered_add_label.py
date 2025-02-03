import pandas as pd

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

file = pd.read_csv(copyTitle + '/patient_diagnoses_musculoskeletal.csv')
phenocodes = pd.read_csv(folderTitle + '/phecode_definitions1.2.csv', encoding='latin-1')

categorizer = pd.read_csv(folderTitle + '/phecode_map1.2.csv', encoding='latin-1')
codes = categorizer['ICD']
phenocode_strings = {
  
}
phenocode_categories = {
  
}

for i in range(len(codes)):
  icd_code = codes[i].replace('.', '')
  phenocode_string = categorizer['PhecodeString'][i]
  phenocode_category = categorizer['PhecodeCategory'][i]
  
  phenocode_strings[icd_code] = phenocode_string
  phenocode_categories[icd_code] = phenocode_category
  

for i in range(len(file)):
  if (i % 100000 == 0):
    print(100 * (i / len(file)), "percent [part 2]")
  icd_code = file['icd_code'][i]
  if icd_code in phenocode_strings:
    file.at[i, 'phecode_string'] = phenocode_strings[icd_code]
  else:
    file.at[i, 'phecode_string'] = 'Unknown'
    
  if icd_code in phenocode_categories:
    file.at[i, 'phecode_category'] = phenocode_categories[icd_code]
  else:
    file.at[i, 'phecode_category'] = 'Unknown'
    
    
file.to_csv(copyTitle + '/patient_diagnoses_musculoskeletal_phecode.csv', index=False)