import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

lab_items = pd.read_csv(folderTitle + '/d_labitems.csv')

lab_names = {
  
}

print("Start")

for i in range(len(lab_items)):
  lab_id = lab_items['itemid'][i]
  lab_name = lab_items['label'][i]
  lab_names[lab_id] = lab_name
  
amount = 0
batch_size = 5000000
  
for df in pd.read_csv(copyTitle + '/labevents_removed_columns.csv', chunksize=batch_size):
  for i in range(len(df)):
    if (i % 500000 == 0):
      print(100 * (i / len(df)), "percent, ", end='')
    index = i + amount * batch_size
    lab_id = df['itemid'][index]
    lab_name = lab_names.get(lab_id, 'Unknown')
    df.at[index, 'item_name'] = lab_name
    
  # Write it to a file inside hosp copy
  header = list(df.columns)
  df.to_csv(copyTitle + '/labevents_with_labels.csv', columns = header, mode = 'a')
  amount += 1
  print(amount, "pushed")