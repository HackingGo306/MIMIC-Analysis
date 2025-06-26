# Add fluid, lab category, and label to the labevent distribution file

import pandas as pd
import numpy as np

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

lab_items = pd.read_csv(folderTitle + '/d_labitems.csv')

lab_info = {
  
}

for i in range(len(lab_items)):
  item_id = lab_items['itemid'][i]
  label = lab_items['label'][i]
  fluid = lab_items['fluid'][i]
  category = lab_items['category'][i]
  
  lab_info[item_id] = {
    'label': label,
    'fluid': fluid,
    'category': category,
  }
  
read_file = pd.read_csv(copyTitle + "/Lab Events/labevent_ref_ranges.csv")

for i in range(len(read_file) - 1):
  item_id = str(read_file['itemid'][i])
  if not (item_id in lab_info):
    continue
  label = lab_info[item_id]['label']
  fluid = lab_info[item_id]['fluid']
  category = lab_info[item_id]['category']
  
  read_file.at[i, 'label'] = label
  read_file.at[i, 'fluid'] = fluid
  read_file.at[i, 'category'] = category
  
read_file.to_csv(copyTitle + '/Lab Events/all_labevent_ref_range_details.csv', index=False)