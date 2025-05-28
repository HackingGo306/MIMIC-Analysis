# randomly pools from the entire population to match with the ~700 malunion patients

import pandas as pd

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

all_patient_data = pd.read_csv(copyTitle + "/All Patient Data/all_patient_data.csv")

malunion_subset = all_patient_data[all_patient_data['Malunion and nonunion of fracture'] == True]
control_subset = all_patient_data[all_patient_data['Malunion and nonunion of fracture'] == False]

sample_size = len(malunion_subset)

pool = control_subset.sample(n = sample_size * 5, replace = False)

data = malunion_subset.to_dict('records')
add = pool.to_dict('records')

batch = 0
for i in range(len(pool)):
  if (i % sample_size == 0):
    batch += 1
    
  add[i]['batch'] = batch
  data.append(add[i])
  
output = pd.DataFrame(data)
output['batch'].fillna(0, inplace = True)

output.to_csv(copyTitle + "/All Patient Data/training_data_other_msk.csv", index=False)