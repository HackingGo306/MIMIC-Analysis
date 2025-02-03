import pandas as pd

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

labitems = pd.read_csv(folderTitle + '/d_labitems.csv')
file = pd.read_csv(copyTitle + '/labevents_with_labels_1_distribution.csv', encoding='latin-1')

item_fluids = {
  
}
item_categories = {
  
}

for i in range(len(labitems)):
  itemid = labitems['itemid'][i]
  fluid = labitems['fluid'][i]
  category = labitems['category'][i]
  
  item_categories[itemid] = category
  item_fluids[itemid] = fluid
  

for i in range(len(file)):
    
  itemid = file['itemid'][i]
  try:
    search_id = int(itemid)
  except ValueError:
    print(itemid)
    continue
  
  if search_id in item_fluids:
    file.at[i, 'fluid'] = item_fluids[search_id]
  else:
    file.at[i, 'fluid'] = 'Unknown'
    
  if search_id in item_categories:
    file.at[i, 'category'] = item_categories[search_id]
  else:
    file.at[i, 'category'] = 'Unknown'
    
    
file.to_csv(copyTitle + '/labevents_with_labels_1_distribution_fluids.csv', index=False)