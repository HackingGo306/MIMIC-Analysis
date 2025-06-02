import pandas as pd

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

labevent_file = pd.read_csv(copyTitle + '/patient_msk_labs_all.csv')
adding_file = pd.read_csv(copyTitle + '/All Patient Data/training_data_with_labs.csv')

patient_data = {
  
}

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

adding_file_data = adding_file.to_dict('records')

print(len(labevent_file))
for i in range(len(labevent_file)):
    
  subject_id = labevent_file['subject_id'][i]
  patient_data[subject_id] = {}
  for j in range(len(selected_categories)):
    current_category = selected_categories[j]
    patient_data[subject_id][current_category] = labevent_file[current_category][i]
  
  
for i in range(len(adding_file)):
  subject_id = adding_file['subject_id'][i]
  if (subject_id in patient_data):
    for j in range(len(selected_categories)):
      current_category = selected_categories[j]
      if (patient_data[subject_id][current_category] > 0):
        adding_file_data[i][current_category] = patient_data[subject_id][current_category]
  
adding_file = pd.DataFrame(adding_file_data)
adding_file.to_csv(copyTitle + "/All Patient Data/training_data_with_labs222.csv", index=False)