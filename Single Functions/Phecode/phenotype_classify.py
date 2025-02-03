import pandas as pd

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

file = pd.read_csv(folderTitle + '/d_icd_diagnoses.csv')
phenocodes = pd.read_csv(folderTitle + '/phecode_definitions1.2.csv', encoding='latin-1')

categorizer = pd.read_csv(folderTitle + '/phecode_map1.2.csv', encoding='latin-1')
codes = categorizer['ICD']
icd_categories = {
  
}
phenocodes_categories = {
  
}

for i in range(len(phenocodes)):
  phenocode = phenocodes['phecode'][i]
  phenocodes_categories[phenocode] = phenocodes['category'][i]

for i in range(len(codes)):
  icd_code = codes[i].replace('.', '')
  phenocode = categorizer['Phecode'][i]
  
  if (icd_code in icd_categories):
    er = 2
  else:
    try:
      icd_categories[icd_code] = phenocodes_categories[phenocode]
    except KeyError:
      er = 2
    
for i in range(len(file)):
  icd_code = file['icd_code'][i].replace('.', '')
  if icd_code in icd_categories:
    file.at[i, 'category'] = icd_categories[icd_code]
  else:
    file.at[i, 'category'] = 'Unknown'
    
file.to_csv(copyTitle + '/d_icd_diagnoses_phenotype_category.csv', index=False)