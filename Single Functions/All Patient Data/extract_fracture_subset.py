# Extracts patients with fracture
# Can be easily modified to exclude those with fracture

import pandas as pd
import numpy as np

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'
data = pd.read_csv(copyTitle + "/All Patient Data/all_patient_data2.csv").to_dict('records')

fractures = ["Fracture of radius or ulna", "Fracture of vertebrae", "Fracture of femur", "Other fractures", "Pathologic fracture", "Stress fracture", "Malunion and nonunion of fracture"]
fractures = ["Malunion and nonunion of fracture"]

output = []

for i in range(len(data)):
  found = False
  for j in range(len(fractures)):
    if (data[i][fractures[j]]):
      output.append(data[i])
      found = True
      break
  # if (not found):
  #   output.append(data[i])
    
    
output = pd.DataFrame(output)
output.to_csv(copyTitle + "/All Patient Data/malunion_extracted.csv", index=False)