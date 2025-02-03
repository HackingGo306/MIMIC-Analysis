import pandas as pd
import numpy as np
from datetime import datetime

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

def import_bmi():
  file = pd.read_csv(copyTitle + '/omr_corrected.csv')
  subject_ids = file['subject_id']
  weights = file['weight']
  weight_times = file['chartdate']
  heights = file['closest_height']
  height_times = file['closest_height_time']
  bmis = file['actual_BMI']
  bmi_times = file['actual_BMI_time']
  fixed_bmi_times = file['fixed_bmi_time']
  projected_bmis = file['projected_BMI']

  total_lines = len(file)
  data = []
  print(fixed_bmi_times[100000])
  print(total_lines)
  for i in range(0, len(file)):
    if (i % 10000 == 0):
      print(100 * (i / total_lines), "percent")
    newRow = {'subject_id': subject_ids[i], 'weight': weights[i], 'w_time': weight_times[i], 'height': heights[i], 'h_time': height_times[i], 'bmi': bmis[i], 'bmi_time': bmi_times[i], 'projected_bmi': projected_bmis[i]}
    try:
      datetime.strptime(fixed_bmi_times[i], '%Y-%m-%d')
      newRow['bmi_time'] = fixed_bmi_times[i]
    except TypeError:
      er = 2

    if (newRow['bmi'] > 200):
      print("skip", newRow['bmi'])
      continue

    data.append(newRow)

  empty = pd.DataFrame(data, columns = ['subject_id', 'weight', 'w_time', 'height', 'h_time', 'bmi', 'bmi_time', 'projected_bmi'])
  empty.to_csv(copyTitle + '/patient_data.csv', index=False)
  

import_bmi()