import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

def split_pools(fracture_index = 0, pool_num = 0):

  version = '3.0'
  folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
  copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'


  categories = ['Pathologic fracture', 'Pathologic fracture of femur', 'Pathologic fracture of vertebrae', 'Malunion and nonunion of fracture', 'Stress fracture']
  category_name = categories[fracture_index]

  # write
  file = pd.read_csv(copyTitle + '/Control Unmatched/' + category_name + '/5x/' + str(pool_num) + '.csv')
  
  
  male = file[file['gender'] == 'M']
  female = file[file['gender'] == 'F']
  
  #write both subsets
  male.to_csv(copyTitle + '/Control Unmatched/' + category_name + '/male_' + str(pool_num) + '.csv', index=False)
  female.to_csv(copyTitle + '/Control Unmatched/' + category_name + '/female_' + str(pool_num) + '.csv', index=False)
  
for i in range(0, 5):
  for j in range(1,4):
    split_pools(i, j)