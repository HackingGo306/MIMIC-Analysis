# Add 40 columns (True/False) to the patient master sheet (patient_matching_bank)
# The following columns are msk conditions found using PheWas
# Output: unique patient data

import pandas as pd
import numpy as np

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

conditions = [
  "Bursitis",
  "Other derangement of joint",
  "Other symptoms referable to back",
  "Kyphosis (acquired)",
  "Peripheral enthesopathies and allied syndromes",
  "Osteitis deformans and osteopathies associated with other disorders classified elsewhere",
  "Aseptic necrosis of bone",
  "Synovitis and tenosynovitis",
  "Intervertebral disc disorder with myelopathy",
  "Infective connective tissue disorders",
  "Other and unspecified disc disorder",
  "Enthesopathy",
  "Joint effusions",
  "Acquired spondylolisthesis",
  "Other disorders of soft tissues",
  "Spondylosis with myelopathy",
  "Pyogenic arthritis",
  "Difficulty in walking",
  "Acquired foot deformities",
  "Polymyalgia Rheumatica",
  "Acute osteomyelitis",
  "Kyphoscoliosis and scoliosis",
  "Chronic osteomyelitis",
  "Degeneration of intervertebral disc",
  "Pathologic fracture of vertebrae",
  "Unspecified osteomyelitis",
  "Pathologic fracture",
  "Arthropathy NOS",
  "Displacement of intervertebral disc",
  "Other disorders of bone and cartilage",
  "Osteopenia or other disorder of bone and cartilage",
  "Osteoarthritis; localized",
  "Rheumatoid arthritis",
  "Spinal stenosis of lumbar region",
  "Spinal stenosis",
  "Osteoarthrosis, localized, primary",
  "Spondylosis without myelopathy",
  "Pain in joint",
  "Osteoporosis NOS",
  "Osteoarthrosis NOS"
]

conditions_file = pd.read_csv(copyTitle + "/patient_diagnoses_musculoskeletal_conditions.csv")

patient_conditions = {
  
}

for i in range(len(conditions_file)):
  subject_id = conditions_file['subject_id'][i]
  condition = conditions_file['phecode_string'][i]
  
  if (condition in conditions):
    if (subject_id not in patient_conditions):
      patient_conditions[subject_id] = []
      
    patient_conditions[subject_id].append(condition)
    
patient_data = pd.read_csv(copyTitle + "/patient_data_with_fracture_group.csv")
# Includes fracture patients
data_list = patient_data.to_dict('records')

for i in range(len(data_list)):
  
  for cond in reversed(conditions):
    data_list[i][cond] = False
  
  subject_id = data_list[i]['subject_id']
  if (subject_id in patient_conditions):
    patient_conditions_list = patient_conditions[subject_id]
    for j in range(len(patient_conditions_list)):
      data_list[i][patient_conditions_list[j]] = True
      
      
output_data = pd.DataFrame(data_list)
output_data.to_csv(copyTitle + "/unique_patient_data.csv", index=False)