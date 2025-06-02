# Compare models where the control size (general or fracture population) is 10x the malunion subset
import pandas as pd
import pycaret
from pycaret.datasets import get_data
from pycaret.classification import *
import numpy as np

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

df = pd.read_csv(copyTitle + "/All Patient Data/training_data_with_labs.csv")
# Try for ALL patients with and without fracture

df = df[(df['batch'] == 0) | (df['batch'] == 1 )]

# control_rows = df[df.batch != 'Mal']
# df = pd.concat([(df[df['batch'] == 'Mal']), control_rows.sample(n = 115)])

df.drop(columns=['batch'], inplace=True)

age_median = df['age'].median()
weight_median = df['weight'].median()
height_median = df['height'].median()

df['age'] = df['age'].replace(-1, age_median)
df['height'] = df['height'].replace(-1, height_median)
df['weight'] = df['weight'].replace(-1, weight_median)

# Keep if using labevents

lab_features = [
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

lab_features = [
  "Calcium, Total",
  "25-OH Vitamin D",
  "Potassium, Whole Blood",
  "Thyroid Stimulating Hormone"
]

for i in range(len(lab_features)):
  feature_name = lab_features[i]
  labmedian = df[feature_name].mean()
  df[feature_name].fillna(labmedian, inplace=True)


# Take mode for missing categorical variables
df['race'] = df['race'].replace('Unknown', 'White')

df['gender'] = df['gender'].astype(str)
df = df.applymap(lambda x: 1 if x == True else 0 if x == False else x) # Convert "True" to 1 and "False" to 0
df = df.applymap(lambda x: 1 if x == 'M' else 0 if x == 'F' else x)

# Remove rows that are empty
df.dropna(inplace=True)
# df.to_csv(copyTitle + "/testing.csv")

clf_setup = setup(
  data=df,
  target='Malunion and nonunion of fracture',
  session_id=42,
  ignore_features=[
    'subject_id',
    # "circulatory system",
    # "congenital anomalies", 
    # "dermatologic", 
    # "digestive",
    # "endocrine/metabolic",
    # "genitourinary", 
    # "hematopoietic", 
    # "infectious diseases",
    "injuries & poisonings",
    # "mental disorders",
    "musculoskeletal",
    # "neoplasms",
    # "neurological",
    # "pregnancy complications",
    # "respiratory",
    # "sense organs",
    "symptoms",
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
    "Fracture of patella",
    "Fracture of upper limb",
    "Pathologic fracture of femur",
    "Stress fracture",
    "Colles' fracture",
    
    "Complications of transplants and reattached limbs",
    "Complication due to other implant and internal device",
  ],
  verbose=True,
)

best = compare_models()
best = create_model('gbc')
plot_model(best, plot='feature')

# df_out = pd.DataFrame()

# df_out['feature'] = get_config('X_train_transformed').columns
# df_out['weight'] = best.feature_importances_

# df_out.to_csv(copyTitle + "/labevents_feature_importance.csv")

# plot_model(best, plot = 'confusion_matrix', plot_kwargs = {'percent' : True})

# # Make predictions
# predictions = predict_model(best_model) 

# # Save the model
# save_model(best_model, 'best_classification_model')