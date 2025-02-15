import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

distribution = pd.read_csv(copyTitle + '/Lab Events/labevents_distribution.csv')

lower = {
  
}

upper = {
  
}

ranges = pd.read_csv(copyTitle + '/Lab Events/labevent_ref_ranges.csv')

for i in range(len(ranges) - 1):
  item_id = ranges['itemid'][i]
  low = ranges['ref_range_lower'][i]
  high = ranges['ref_range_upper'][i]
  if ((pd.notna(low) and pd.notna(high))):
    lower[item_id] = min(float(low), float(lower.get(item_id, 10000000)))
    upper[item_id] = max(float(high), float(upper.get(item_id, -10000000)))

# Now use the dictionary to modify the distribution table
for i in range(len(distribution)):
  itemid = distribution['itemid'][i]
  # add column values
  distribution.at[i, 'lower'] = lower.get(itemid, np.nan)
  distribution.at[i, 'upper'] = upper.get(itemid, np.nan)

# Write it to a file inside hosp copy
distribution.to_csv(copyTitle + '/Lab Events/labevents_distribution_2.csv', index=False)
print("Finished")