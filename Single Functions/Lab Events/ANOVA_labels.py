# After storing ANOVA (Screening --> Response Screening) for the lab events, add labels to the item_id

import pandas as pd
import statistics

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

file = pd.read_csv(copyTitle + '/Lab Events/lab_by_malunion.csv')

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
  
for i in range(len(file)):
  item_id = file['Y'][i]
  
  file.at[i, 'label'] = lab_info[item_id]['label']
  file.at[i, 'fluid'] = lab_info[item_id]['fluid']
  file.at[i, 'category'] = lab_info[item_id]['category']
  
  
cols = file.columns.tolist()
cols = cols[0:1] + cols[-3:] + cols[2:-3]
file = file[cols]
  
file.to_csv(copyTitle + "/Lab Events/lab_by_malunion_details.csv", index=False)