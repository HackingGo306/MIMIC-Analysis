# Adds the phecode_string to the frequency table

import pandas as pd

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

phecode_map = pd.read_csv(folderTitle + "/phecode_map1.2.csv")
phecode_freq = pd.read_csv(copyTitle + "/All Patient Data/patient_phecode_frequency.csv")
categorizer = {
  
}

for i in range(len(phecode_map)):
  phecode = str(phecode_map['Phecode'][i])
  phecode_string = phecode_map['PhecodeString'][i]
  categorizer[phecode] = phecode_string
  
for i in range(len(phecode_freq)):
  phecode = str(phecode_freq['phecode'][i])
  phecode_string = categorizer[phecode]
  phecode_freq.at[i, 'phecode_string'] = phecode_string
  
phecode_freq.to_csv(copyTitle + "/All Patient Data/patient_phecode_frequency.csv", index = False)