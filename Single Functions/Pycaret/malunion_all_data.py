# Compare models where the control size (general or fracture population) is 10x the malunion subset
import pandas as pd
import pycaret
from pycaret.datasets import get_data
from pycaret.classification import *
import numpy as np

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

df = pd.read_csv(copyTitle + "/All Patient Data/training_data.csv")
# Try for ALL patients with and without fracture

df = df[(df['batch'] == 0) | (df['batch'] == 1 )]

# control_rows = df[df.batch != 'Mal']
# df = pd.concat([(df[df['batch'] == 'Mal']), control_rows.sample(n = 115)])

df.drop(columns=['batch'], inplace=True)

# Remove rows that are empty
df.dropna(inplace=True)

age_median = df['age'].median()
weight_median = df['weight'].median()
height_median = df['height'].median()

df['age'] = df['age'].replace(-1, age_median)
df['height'] = df['height'].replace(-1, height_median)
df['weight'] = df['weight'].replace(-1, weight_median)


df['gender'] = df['gender'].astype(str)
df = df.applymap(lambda x: 1 if x == True else 0 if x == False else x) # Convert "True" to 1 and "False" to 0
df = df.applymap(lambda x: 1 if x == 'M' else 0 if x == 'F' else x)

# Display all rows

clf_setup = setup(
  data=df,
  target='Malunion and nonunion of fracture',
  session_id=42,
  ignore_features=['subject_id'],
  # verbose=True,
  numeric_imputation='mean',
  preprocess=True
)

best = compare_models()
plot_model(best, plot = 'feature')

# plot_model(best, plot = 'confusion_matrix', plot_kwargs = {'percent' : True})

# # Make predictions
# predictions = predict_model(best_model) 

# # Save the model
# save_model(best_model, 'best_classification_model')