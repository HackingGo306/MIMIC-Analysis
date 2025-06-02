# Add specific labevent columns to the patient data that are related to or affecting msk

import pandas as pd
import numpy as np

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

lab_mapping = pd.read_csv(folderTitle + "/d_labitems.csv")

lab_map = {
  
}
for i in range(len(lab_mapping)):
  lab_id = lab_mapping['itemid'][i]
  lab_type = lab_mapping['label'][i]
  category = lab_mapping['category'][i]
  fluid = lab_mapping['fluid'][i]
  lab_map[lab_id] = {'name': lab_type, 'category': category, 'fluid': fluid}
  
selected_categories = [
  "Hematocrit",
  "Creatinine",
  "Platelet Count",
  "Urea Nitrogen",
  "Hemoglobin",
  "White Blood Cells",
  "Potassium",
  "MCHC",
  "MCV",
  "MCH",
  "Red Blood Cells",
  "RDW",
  "Sodium",
  "Chloride",
  "Bicarbonate",
  "Anion Gap",
  "Glucose",
  "Calcium, Total",
  "Magnesium",
  "Phosphate",
  "H",
  "L",
  "I",
  "RDW-SD",
  "Alanine Aminotransferase (ALT)",
  "INR(PT)",
  "PT",
  "Asparate Aminotransferase (AST)",
  "Estimated GFR (MDRD equation)",
  "PTT",
  "Lymphocytes",
  "Neutrophils",
  "Monocytes",
  "Eosinophils",
  "Basophils",
  "Bilirubin, Total",
  "Alkaline Phosphatase",
  "Albumin",
  "Absolute Neutrophil Count",
  "Absolute Eosinophil Count",
  "Absolute Monocyte Count",
  "Absolute Lymphocyte Count",
  "Absolute Basophil Count"
]

selected_fluids = [
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
  'Blood',
]

patient_data = {
  
}

amount = 0
batch_size = 15000000
for df in pd.read_csv(folderTitle + '/labevents.csv', chunksize=batch_size):
  for i in range(len(df)):
    if (i % 1500000 == 0):
      print(100 * (i / len(df)), "percent, ")
      
    index = i + amount * batch_size
    lab_id = df.at[index, 'itemid']
    subject_id = df.at[index, 'subject_id']
    
    lab_name = lab_map[lab_id]['name']
    lab_fluid = lab_map[lab_id]['fluid']
    
    matched = False
    for j in range(len(selected_categories)):
      if (lab_name == selected_categories[j]) and (lab_fluid == selected_fluids[j]):
        matched = True
        break
    
    if (matched):
      lab_value = df['valuenum'][index]
      
      if (type(lab_value) == str) or (pd.isna(lab_value)):
        continue
      
      if not (subject_id in patient_data):
        patient_data[subject_id] = {}
        
      if not (lab_name in patient_data[subject_id]):
        patient_data[subject_id][lab_name] = []
        
      patient_data[subject_id][lab_name].append(lab_value)
    
      
  amount += 1
  print(amount, "read")
  
data = []
for subject_id, info in patient_data.items():
  row = {}
  row['subject_id'] = subject_id
  
  category_values = []
  for i in range(len(selected_categories)):
    category_values.append(-1)
    if (selected_categories[i] in info):
      category_values[i] = np.median(info[selected_categories[i]])
    
    row[selected_categories[i]] = category_values[i]
    
  data.append(row)
    
output_data = pd.DataFrame(data)

output_data.to_csv(copyTitle + '/patient_msk_labs_all.csv', index=False)