# Find the distribution of all labevents in terms of events and unique patients

import pandas as pd
import numpy as np

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

lab_items = pd.read_csv(folderTitle + '/d_labitems.csv')

labevent_frequency = {
  
}

labevent_count = {
  
}

batch_size = 1500000 * 10
amount = 0
for df in pd.read_csv(folderTitle + '/labevents.csv', chunksize=batch_size):
  
  batch_data = df.to_dict('records')
  
  
  for i in range(len(batch_data)):
    if (i % ((batch_size) / 10) == 0):
      print(100 * (i / len(df)), "percent, ")
    
    index = i + amount * batch_size
    lab_id = batch_data[i]['itemid']
    
    subject_id = batch_data[i]['subject_id']
    
    if (lab_id not in labevent_frequency):
      labevent_frequency[lab_id] = {}
      labevent_count[lab_id] = 0
      
    labevent_frequency[lab_id][subject_id] = True
    labevent_count[lab_id] += 1
  
  amount += 1
  
  print(amount, "read -------------------------------")
  
output_data = []

for key in labevent_frequency.keys():
  unique_patients = len(labevent_frequency[key].keys())
  total_events = labevent_count[key]
  
  row = {'item_id': key, 'patients': unique_patients, 'events': total_events}
  output_data.append(row)
  
output_df = pd.DataFrame(output_data)
output_df.to_csv(copyTitle + '/Lab Events/all_labevent_frequency.csv')