# Compare models where the control size (general or fracture population) is 10x the malunion subset
import pandas as pd
import pycaret
from pycaret.datasets import get_data
from pycaret.classification import *

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

df = pd.read_csv(copyTitle + "/Master Patient Data/Malunion General Control Group 2/train_data_2.csv")
# Try for ALL patients with and without fracture

df = df[(df['batch'] == 'Mal') | (df['batch'] == "B1" )]

# control_rows = df[df.batch != 'Mal']
# df = pd.concat([(df[df['batch'] == 'Mal']), control_rows.sample(n = 115)])

df.drop(columns=['batch', 'relaxed', 'matched_with'], inplace=True)

# Remove rows that are empty
df.dropna(inplace=True)

df['gender'] = df['gender'].astype(str)
df = df.applymap(lambda x: 1 if x == True else 0 if x == False else x) # Convert "True" to 1 and "False" to 0
df = df.applymap(lambda x: 1 if x == 'M' else 0 if x == 'F' else x)

# Display all rows

clf_setup = setup(
  data=df,
  target='Malunion and nonunion of fracture',
  session_id=42,
  ignore_features=['subject_id', 'Unknown'],
  # , 'Pathologic fracture', 'Stress fracture', 'Fracture of vertebrae', 'Fracture of femur'
  verbose=True,
)
get_config('X').dtypes

best = compare_models()
plot_model(best, plot = 'feature')
# plot_model(best, plot = 'confusion_matrix', plot_kwargs = {'percent' : True})

# # Make predictions
# predictions = predict_model(best_model) 

# # Save the model
# save_model(best_model, 'best_classification_model')