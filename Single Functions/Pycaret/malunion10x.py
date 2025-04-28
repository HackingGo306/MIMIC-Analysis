# Compare models where the control size (general or fracture population) is 10x the malunion subset
import pandas as pd
import pycaret
from pycaret.datasets import get_data
from pycaret.classification import *

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

df = pd.read_csv(copyTitle + "/Master Patient Data/Malunion Fracture Control Group 1/train_data_2.csv")

# Remove rows that are empty
df.dropna(inplace=True)
df['gender'] = df['gender'].astype(str)
df = df.applymap(lambda x: 1 if x == 'True' else 0 if x == 'False' else x) # Convert "True" to 1 and "False" to 0

pd.set_option('display.max_columns', None)

# Display all rows (if necessary)
pd.set_option('display.max_rows', None)
print(df.dtypes)

clf_setup = setup(
  data=df,
  target='Malunion and nonunion of fracture',
  session_id=42,
  categorical_features=['gender'],
  ignore_features=['subject_id', 'Unknown', 'Other fractures', 'Fracture of radius or ulna', 'batch', 'relaxed', 'matched_with'],
  verbose=True,
)
get_config('X').dtypes

compare_models()

# best_model = compare_models()

# # Make predictions
# predictions = predict_model(best_model) 

# # Save the model
# save_model(best_model, 'best_classification_model')