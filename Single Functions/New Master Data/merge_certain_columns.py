# Merges certain columns of the fractures into a broader category
# True if any one of the child columns are true

import pandas as pd
import numpy as np

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'
data = pd.read_csv(copyTitle + "/unique_patient_data.csv").to_dict('records')

merge_names = [["Fracture of radius and ulna", "Fracture of hand or wrist"],
               ["Pathologic fracture of vertebrae", "Fracture of vertebral column without mention of spinal cord injury"],
               ["Pathologic fracture of femur", "Fracture of neck of femur", "Fracture of unspecified part of femur"],
               ["Fracture of tibia and fibula", "Fracture of lower limb", "Fracture of ankle and foot"]]

merge_titles = ["Fracture of radius or ulna", "Fracture of vertebrae", "Fracture of femur", "Other fractures"]

for i in range(len(data)):
  for j in range(len(merge_names)):
    merge_val = False
    for k in range(len(merge_names[j])):
      merge_val = merge_val or data[i][merge_names[j][k]]
    data[i][merge_titles[j]] = merge_val
  
output = pd.DataFrame(data)
cols = output.columns.tolist()
cols = cols[0:37] + cols[-4:] + cols[37:-4]
output = output[cols]

for i in range(len(merge_names)):
  output.drop(columns=merge_names[i], inplace=True)

output.to_csv(copyTitle + "/unique_patient_data_merged.csv", index = False)