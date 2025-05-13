# Adds the phecode_category to the frequency table

import pandas as pd

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

phecode_map = pd.read_csv(folderTitle + "/phecode_definitions1.2.csv")
phecode_freq = pd.read_csv(copyTitle + "/All Patient Data/patient_phecode_frequency.csv")
categorizer = {
  
}

for i in range(len(phecode_map)):
  phecode = str(phecode_map['phecode'][i])
  phecode_category = phecode_map['category'][i]
  categorizer[phecode] = phecode_category
  
for i in range(len(phecode_freq)):
  phecode = str(phecode_freq['phecode'][i])
  try:
    phecode_string = categorizer[phecode]
    if (phecode_string == "nan"):
      pass
    phecode_freq.at[i, 'phecode_category'] = phecode_string
  except KeyError:
    pass
  
phecode_freq.to_csv(copyTitle + "/All Patient Data/patient_phecode_frequency.csv", index = False)