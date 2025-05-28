# Add specific phecode_string columns (true/false) to the output of the add_diagnosis_categories.py file

import pandas as pd

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

patient_demographics = pd.read_csv(copyTitle + "/All Patient Data/all_patient_data.csv")
patient_phecodes = pd.read_csv(copyTitle + "/All Patient Data/all_patient_phecodes.csv")

phecode_map = pd.read_csv(folderTitle + "/phecode_map1.2.csv")
categorizer = {
  
}

for i in range(len(phecode_map)):
  phecode = str(phecode_map['Phecode'][i])
  phecode_string = phecode_map['PhecodeString'][i]
  categorizer[phecode] = phecode_string

patient_data = {
  
}

# selected_categories = ['Pathologic fracture', 'Pathologic fracture of femur', 'Pathologic fracture of vertebrae', 'Malunion and nonunion of fracture', 'Fracture of tibia and fibula', 'Fracture of lower limb', 'Stress fracture', 'Fracture of unspecified part of femur', 'Fracture of neck of femur', 'Fracture of ankle and foot', 'Fracture of radius and ulna', 'Fracture of vertebral column without mention of spinal cord injury', 'Fracture of hand or wrist']
selected_categories = [
"Skull and face fracture and other intercranial injury",
"Fracture of vertebral column without mention of spinal cord injury",
"Fracture of ribs",
"Fracture of unspecified part of femur",
"Fracture of neck of femur",
"Pathologic fracture",
"Fracture of tibia and fibula",
"Fracture of radius and ulna",
"Pathologic fracture of vertebrae",
"Fracture of pelvis",
"Fracture of humerus",
"Fracture of clavicle or scapula",
"Fracture of ankle and foot",
"Fracture of lower limb",
"Fracture of foot",
"Fracture of hand or wrist",
"Fracture of unspecified bones",
"Malunion and nonunion of fracture",
"Fracture of patella",
"Fracture of upper limb",
"Pathologic fracture of femur",
"Stress fracture",
"Colles' fracture"
]


selected_categories = [
  # 20 most frequent diagnosis categories (removed those like "other" or unrelated)
  "Essential hypertension",
  "Hyperlipidemia",
  "Tobacco use disorder",
  "GERD",
  "Acute renal failure",
  "Coronary atherosclerosis",
  "Type 2 diabetes",
  "Anxiety disorder",
  "Atrial fibrillation",
  "Other anemias",
  "Urinary tract infection",
  "Major depressive disorder",
  "Acute posthemorrhagic anemia",
  "Hypothyroidism NOS",
  "Hypovolemia",
  "Obesity",
  "Myocardial infarction",
  "Respiratory failure",
  "Hypertensive chronic kidney disease",
  "Hyposmolality and/or hyponatremia",
  
  # 20 most freqeuent msk-related categories (with some repeats removed)
  "Osteoarthrosis NOS",
  "Osteoporosis NOS",
  "Pain in joint",
  "Spondylosis without myelopathy",
  "Osteoarthrosis, localized, primary",
  "Spinal stenosis",
  "Spinal stenosis of lumbar region",
  "Rheumatoid arthritis",
  "Osteoarthritis; localized",
  "Osteopenia or other disorder of bone and cartilage",
  "Other disorders of bone and cartilage",
  "Displacement of intervertebral disc",
  "Arthropathy NOS",
  "Unspecified osteomyelitis",
  "Other disorders of soft tissues",
  "Degeneration of intervertebral disc",
  "Chronic osteomyelitis",
  "Kyphoscoliosis and scoliosis",
  "Acute osteomyelitis",
  "Polymyalgia Rheumatica",
]



include = {}
for cat in selected_categories:
  include[cat] = True
  patient_demographics[cat] = False

for i in range(len(patient_phecodes)):
  if (i % 10000 == 0):
    print("Part 1:",(i/len(patient_phecodes) * 100),"% percent")
  subject_id = str(patient_phecodes['subject_id'][i])
  if (pd.isna(patient_phecodes['phecodes'][i])): continue
  patient_data[subject_id] = {}
  try:
    phecode_strings = str(patient_phecodes['phecodes'][i]).split(", ")
    for string in phecode_strings: 
      phecode_string = categorizer[string]
      if (phecode_string in include):
        patient_data[subject_id][phecode_string] = True
  except KeyError:
    pass
  
for i in range(len(patient_demographics)):
  if (i % 10000 == 0):
    print("Part 2:",(i/len(patient_demographics) * 100),"% percent")
  subject_id = str(patient_demographics['subject_id'][i])
  try:
    for category in patient_data[subject_id].keys():
      patient_demographics.at[i, category] = True 
  except KeyError:
    pass # Not all patients have phecode diagnoses
    
# Remove first column (column 1)
# patient_demographics.drop("Unnamed: 0", axis=1, inplace=True)

patient_demographics.to_csv(copyTitle + "/All Patient Data/all_patient_data2.csv", index=False)