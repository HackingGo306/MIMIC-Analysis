import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

distribution = pd.read_csv(copyTitle + '/Lab Events/labevents_with_labels_1_distribution_fluids.csv')

lab_units = {
  
}

unit_types = pd.read_csv(copyTitle + '/Lab Events/labevent_units.csv')

for i in range(len(unit_types) - 1):
  # loop through the row's columns
  amount = 0
  itemid = -1
  for col in unit_types.columns:
    if (col == "itemid"):
      itemid = unit_types[col][i]
      continue
    elif (col == "N Rows"):
      continue
      
    unit_rows = unit_types[col][i]
    if (int(unit_rows) > 0):
      amount += 1
      if (amount > 1 and int(itemid) > 0):
        print(f'Duplicate itemid {itemid} found in labevent_units.csv')
      print(itemid, col)
      lab_units[itemid] = col[2:-1]

# Now use the dictionary to modify the distribution table
for i in range(len(distribution)):
  itemid = distribution['itemid'][i]
  unit = lab_units.get(itemid, 'Unknown')
  distribution.at[i, 'unit'] = unit

# Write it to a file inside hosp copy
distribution.to_csv(copyTitle + '/Lab Events/labevents_distribution_fluids_units.csv', index=False)
print("Finished")