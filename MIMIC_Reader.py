import pandas as pd
import numpy as np
from datetime import datetime

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

def addFilteredHeightWeightColumns():
  # Average the height and weight of each BMI patient and add it to the row (NEW VERSION - uses filtered weight and height tables)
  print("NEW VERSION")
  omr_BMI_kg = pd.read_csv(copyTitle + "/omr BMI_kg.csv")
  omr_BMI_ids = omr_BMI_kg['subject_id']

  omr_Weight_lb = pd.read_csv(copyTitle + "/omr Weight_lb_corrected_range.csv")
  omr_Weight_values = omr_Weight_lb['result_value']
  omr_Weight_ids = omr_Weight_lb['subject_id']

  omr_Height_in = pd.read_csv(copyTitle + "/omr Height_in_corrected_range.csv")
  omr_Height_values = omr_Height_in['result_value']
  omr_Height_ids = omr_Height_in['subject_id']
  
  patient_weights = {}
  patient_heights = {}

  for i in range(len(omr_Weight_ids)):
    subject_id = omr_Weight_ids[i]
    weight = float(omr_Weight_values[i])
    if (subject_id in patient_weights):
      patient_weights[subject_id].append(weight)
    else:
      patient_weights[subject_id] = [weight]

  for i in range(len(omr_Height_ids)):
    subject_id = omr_Height_ids[i]
    try:
      height = float(omr_Height_values[i])
    except ValueError:
      continue  # Skip rows where height cannot be converted to float
    if (subject_id in patient_heights):
      patient_heights[subject_id].append(height)
    else:
      patient_heights[subject_id] = [height]

  print(len(patient_weights.keys()))

  # Write into a copy file using pandas
  omr_BMI_kg_copy = omr_BMI_kg.copy()
  maxLen = len(omr_BMI_ids)
  print('TOTAL', maxLen)
  for i in range(len(omr_BMI_ids)):
    if (i % 1000 == 0):
      print((i * 100 / maxLen), "%")
    subject_id = omr_BMI_ids[i]
    if (subject_id in patient_heights.keys()):
      height_avg = np.mean(patient_heights[subject_id])
      height_max = np.max(patient_heights[subject_id])
      height_min = np.min(patient_heights[subject_id])
      height_len = len(patient_heights[subject_id])
      omr_BMI_kg_copy.loc[i, 'avg_height'] = height_avg
      omr_BMI_kg_copy.loc[i, 'max_height'] = height_max
      omr_BMI_kg_copy.loc[i, 'min_height'] = height_min
      omr_BMI_kg_copy.loc[i, 'height_measurements'] = height_len
    if (subject_id in patient_weights):
      # repeat same process for weight
      weight_avg = np.mean(patient_weights[subject_id])
      weight_max = np.max(patient_weights[subject_id])
      weight_min = np.min(patient_weights[subject_id])
      weight_len = len(patient_weights[subject_id])
      omr_BMI_kg_copy.loc[i, 'avg_weight'] = weight_avg
      omr_BMI_kg_copy.loc[i, 'max_weight'] = weight_max
      omr_BMI_kg_copy.loc[i, 'min_weight'] = weight_min
      omr_BMI_kg_copy.loc[i, 'weight_measurements'] = weight_len

  omr_BMI_kg_copy.to_csv(copyTitle + '/omr BMI_height_weight_filtered.csv', index=False)

def calculateFilteredBMI(): # Create a column of the projected BMI using the filtered height and weight values
  omr_BMI_kg_copy = pd.read_csv(copyTitle + "/omr BMI_height_weight_filtered.csv")
  omr_BMI_ids = omr_BMI_kg_copy['subject_id']
  omr_weight_values = omr_BMI_kg_copy['avg_weight']
  omr_height_values = omr_BMI_kg_copy['avg_height']
  actual_BMI_values = omr_BMI_kg_copy['result_value']

  for i in range(len(omr_BMI_ids)):
    weight = float(omr_weight_values[i])
    height = float(omr_height_values[i])
    actual_BMI = float(actual_BMI_values[i])
    if (weight > 0 and height > 0): 
      bmi = (weight * 0.453592) / ((height * 0.0254) ** 2)
      omr_BMI_kg_copy.loc[i, 'projected_bmi'] = bmi
      omr_BMI_kg_copy.loc[i, 'percent_error'] = (abs(bmi - actual_BMI) / (actual_BMI + bmi) * 2) * 100

  # Write to new csv file
  omr_BMI_kg_copy.to_csv(copyTitle + '/omr BMI_height_weight_filtered_with_projected.csv', index=False)


def nearestNeighborsCheckWeight():
  kg_file = pd.read_csv(copyTitle + '/omr Weight_lb_replaced.csv')
  id_list = kg_file['subject_id']
  value_list = kg_file['result_value']
  time_list = kg_file['chartdate']
  time_values = []

  zero_date = datetime.strptime('2000-01-1', '%Y-%m-%d')
  for i in range(len(time_list)):
    obj = datetime.strptime(time_list[i], '%Y-%m-%d')
    days = (obj - zero_date).days
    time_values.append(days)

  patients = {}

  for i in range(len(id_list)):
    patient_id = id_list[i]
    value = value_list[i]
    time = time_values[i]
    if patient_id in patients:
      patients[patient_id].append((value, time, i))
    else:
      patients[patient_id] = [(value, time, i)]
  
  # Create copy of kg file
  kg_file_copy = kg_file.copy()
  resolved = 0
  # Loop through patients obj
  for patient_id, measurements in patients.items():
    sorted_measurements = sorted(measurements, key=lambda x: x[1])

    for i in range(len(sorted_measurements)):
      row_num = sorted_measurements[i][2]
      kg_file_copy.loc[row_num, 'patient_measurments'] = len(sorted_measurements)
      if (len(sorted_measurements) < 3):
        continue # We cannot tell which one is the outlier
      
      a = 0
      b = 0
      if (i > 0 and i < len(sorted_measurements) - 1):
        a = sorted_measurements[i - 1][0]
        b = sorted_measurements[i + 1][0]
      elif (i == 0):
        a = sorted_measurements[i + 1][0]
        b = sorted_measurements[i + 2][0]
      elif (i == len(sorted_measurements) - 1):
        a = sorted_measurements[i - 1][0]
        b = sorted_measurements[i - 2][0]

      if (a == 0 and b == 0):
        print("Error: both measurements are 0")

      # Calculate percent difference
      percent_diff_a = abs((sorted_measurements[i][0] - a)) / ((sorted_measurements[i][0] + a) / 2) * 100
      percent_diff_b = abs((sorted_measurements[i][0] - b)) / ((sorted_measurements[i][0] + b) / 2) * 100
      if (percent_diff_a > 100 and percent_diff_b > 100):
        print(f"Patient ID: {patient_id}, Measurement: {sorted_measurements[i][0]}, Percent Difference: {percent_diff_a} and {percent_diff_b}, Neighbors: {a} and {b}")
        # Set this value to the mean in the copy file
        kg_file_copy.loc[row_num, 'result_value'] = (a + b) / 2
        resolved += 1

  # Write to new csv file
  kg_file_copy.to_csv(copyTitle + '/omr Weight_lb_adjacent2.csv', index=False)
  print(f"Resolved {resolved} measurements")

def nearestNeighborsCheckHeight():
  in_file = pd.read_csv(copyTitle + '/omr Height_in_replaced.csv')
  id_list = in_file['subject_id']
  value_list = in_file['result_value']
  time_list = in_file['chartdate']
  time_values = []

  zero_date = datetime.strptime('2000-01-1', '%Y-%m-%d')
  for i in range(len(time_list)):
    obj = datetime.strptime(time_list[i], '%Y-%m-%d')
    days = (obj - zero_date).days
    time_values.append(days)

  patients = {}

  for i in range(len(id_list)):
    patient_id = id_list[i]
    value = value_list[i]
    time = time_values[i]

    try:
      value = float(value)
    except ValueError:
      print(f"Non-numeric value found for patient ID: {patient_id}, Value: {value}, Time: {time}")
      continue

    if patient_id in patients:
      patients[patient_id].append((value, time, i))
    else:
      patients[patient_id] = [(value, time, i)]

  # Create copy of in file
  in_file_copy = in_file.copy()
  resolved = 0
  # Loop through patients obj
  for patient_id, measurements in patients.items():
    sorted_measurements = sorted(measurements, key=lambda x: x[1])
    for i in range(len(sorted_measurements)):
      # check if current measurement is between adjecent measurements
      row_num = sorted_measurements[i][2]
      in_file_copy.loc[row_num, 'patient_measurments'] = len(sorted_measurements)

      # Check if there are more than two measurements in the list
      if (len(sorted_measurements) < 3):
        continue 

      if (i > 0 and i < len(sorted_measurements) - 1):
        a = sorted_measurements[i - 1][0]
        b = sorted_measurements[i + 1][0]
      elif (i == 0):
        a = sorted_measurements[i + 1][0]
        b = sorted_measurements[i + 2][0]
      elif (i == len(sorted_measurements) - 1):
        a = sorted_measurements[i - 1][0]
        b = sorted_measurements[i - 2][0]

      # Calculate percent difference
      percent_diff_a = abs(sorted_measurements[i][0] - a) / ((sorted_measurements[i][0] + a) / 2) * 100
      percent_diff_b = abs(sorted_measurements[i][0] - b) / ((sorted_measurements[i][0] + b) / 2) * 100

      if (patient_id == 11703425):
        print(percent_diff_a, percent_diff_b, a, b, sorted_measurements[i][0])

      if (percent_diff_a > 20 and percent_diff_b > 20):
        print(f"Patient ID: {patient_id}, Measurement: {sorted_measurements[i][0]}, Percent Difference: {percent_diff_a} and {percent_diff_b}, Neighbors: {a} and {b}")
        # Set this value to the mean in the copy file
        in_file_copy.loc[row_num, 'result_value'] = (a + b) / 2
        resolved += 1
  
  # Write to new csv file
  in_file_copy.to_csv(copyTitle + '/omr Height_in_adjacent2.csv', index=False)
  print(f"Resolved {resolved} height measurements.")

def nearestBMI():
  weight_file = pd.read_csv(copyTitle + '/omr Weight_lb_adjacent2.csv')
  height_file = pd.read_csv(copyTitle + '/omr Height_in_adjacent2.csv')
  bmi_file = pd.read_csv(copyTitle + '/omr BMI_kg.csv')

  weight_ids = weight_file['subject_id']
  weight_values = weight_file['result_value']
  weight_dates = weight_file['chartdate']
  height_ids = height_file['subject_id']
  height_values = height_file['result_value']
  height_dates = height_file['chartdate']
  bmi_ids = bmi_file['subject_id']
  bmi_values = bmi_file['result_value']
  bmi_dates = bmi_file['chartdate']

  patient_heights = {}
  for i in range(len(height_ids)):
    try:
      numVal = float(height_values[i])
    except ValueError:
      print(f"Non-numeric value found for height ID: {height_ids[i]}, Value: {height_values[i]}, Date: {height_dates[i]}")
      continue

    patient_id = height_ids[i]
    patient_date = datetime.strptime(height_dates[i], "%Y-%m-%d")
    if patient_id in patient_heights:
      patient_heights[patient_id].append((height_values[i], patient_date))
    else:
      patient_heights[patient_id] = [(height_values[i], patient_date)]

  # Do the same for BMI 
  patient_bmi = {}
  for i in range(len(bmi_ids)):
    patient_id = bmi_ids[i]
    patient_date = datetime.strptime(bmi_dates[i], "%Y-%m-%d")
    if patient_id in patient_bmi:
      patient_bmi[patient_id].append((bmi_values[i], patient_date))
    else:
      patient_bmi[patient_id] = [(bmi_values[i], patient_date)]

  weight_copy = weight_file.copy()
  total_amount = len(weight_values)
  for i in range(total_amount):
    if (i % 1000 == 0):
      print(i, "of", total_amount)
    patient_id = weight_ids[i]
    patient_date = datetime.strptime(weight_dates[i], "%Y-%m-%d")
    patient_weight = weight_values[i]

    if not (patient_id in patient_heights) or not (patient_id in patient_bmi):
      continue

    # Find the patient height with date closest to patientdate
    closest_height_date = min(patient_heights[patient_id], key=lambda x: abs(x[1] - patient_date))
    closest_height = float(closest_height_date[0])
    closest_height_time = closest_height_date[1]
    height_measurements = len(patient_heights[patient_id])

    # Find the patient's BMI with closest date to patientdate
    closest_bmi_date = min(patient_bmi[patient_id], key=lambda x: abs(x[1] - patient_date))
    closest_bmi = closest_bmi_date[0]
    closest_bmi_time = closest_bmi_date[1]
    bmi_measurements = len(patient_bmi[patient_id])

    # Calculate BMI using the height and weight
    bmi = (patient_weight * 0.453592) / ((closest_height * 0.0254) ** 2)
    weight_copy.at[i, 'closest_height'] = closest_height
    weight_copy.at[i, 'closest_height_time'] = closest_height_time
    weight_copy.at[i, 'height_measurements'] = height_measurements
    weight_copy.at[i, 'projected_BMI'] = bmi
    weight_copy.at[i, 'actual_BMI'] = closest_bmi
    weight_copy.at[i, 'actual_BMI_time'] = closest_bmi_time
    weight_copy.at[i, 'BMI_measurements'] = bmi_measurements

  # Write to new csv file
  weight_copy.to_csv(copyTitle + '/omr Weight_lb_projectedBMI.csv', index=False)
    
def percentDifferent():
  # Calculate percent difference between the proejcted BMI and actual BMI column in the table
  percent_diff_file = pd.read_csv(copyTitle + '/omr Weight_lb_projectedBMI.csv')

  for i in range(len(percent_diff_file)):
    projected_bmi = percent_diff_file.loc[i, 'projected_BMI']
    actual_bmi = percent_diff_file.loc[i, 'actual_BMI']

    if (projected_bmi is None or actual_bmi is None):
      continue

    diff = abs(projected_bmi - actual_bmi) / abs((projected_bmi + actual_bmi) / 2) * 100
    percent_diff_file.at[i, 'percent_difference'] = diff

  percent_diff_file.to_csv(copyTitle + '/omr BMI_weight_based.csv', index=False)



def nearestNeighborsCheckBMI():
  in_file = pd.read_csv(copyTitle + '/omr Height_in_replaced.csv')
  id_list = in_file['subject_id']
  value_list = in_file['result_value']
  time_list = in_file['chartdate']
  time_values = []

  zero_date = datetime.strptime('2000-01-1', '%Y-%m-%d')
  for i in range(len(time_list)):
    obj = datetime.strptime(time_list[i], '%Y-%m-%d')
    days = (obj - zero_date).days
    time_values.append(days)

  patients = {}

  for i in range(len(id_list)):
    patient_id = id_list[i]
    value = value_list[i]
    time = time_values[i]

    try:
      value = float(value)
    except ValueError:
      print(f"Non-numeric value found for patient ID: {patient_id}, Value: {value}, Time: {time}")
      continue

    if patient_id in patients:
      patients[patient_id].append((value, time, i))
    else:
      patients[patient_id] = [(value, time, i)]

  # Create copy of in file
  in_file_copy = in_file.copy()
  resolved = 0
  # Loop through patients obj
  for patient_id, measurements in patients.items():
    sorted_measurements = sorted(measurements, key=lambda x: x[1])
    for i in range(len(sorted_measurements)):
      # check if current measurement is between adjecent measurements
      row_num = sorted_measurements[i][2]
      in_file_copy.loc[row_num, 'patient_measurments'] = len(sorted_measurements)

      # Check if there are more than two measurements in the list
      if (len(sorted_measurements) < 3):
        continue 

      if (i > 0 and i < len(sorted_measurements) - 1):
        a = sorted_measurements[i - 1][0]
        b = sorted_measurements[i + 1][0]
      elif (i == 0):
        a = sorted_measurements[i + 1][0]
        b = sorted_measurements[i + 2][0]
      elif (i == len(sorted_measurements) - 1):
        a = sorted_measurements[i - 1][0]
        b = sorted_measurements[i - 2][0]

      # Calculate percent difference
      percent_diff_a = abs(sorted_measurements[i][0] - a) / ((sorted_measurements[i][0] + a) / 2) * 100
      percent_diff_b = abs(sorted_measurements[i][0] - b) / ((sorted_measurements[i][0] + b) / 2) * 100

      if (patient_id == 11703425):
        print(percent_diff_a, percent_diff_b, a, b, sorted_measurements[i][0])

      if (percent_diff_a > 20 and percent_diff_b > 20):
        print(f"Patient ID: {patient_id}, Measurement: {sorted_measurements[i][0]}, Percent Difference: {percent_diff_a} and {percent_diff_b}, Neighbors: {a} and {b}")
        # Set this value to the mean in the copy file
        in_file_copy.loc[row_num, 'result_value'] = (a + b) / 2
        resolved += 1
  
  # Write to new csv file
  in_file_copy.to_csv(copyTitle + '/omr Height_in_adjacent2.csv', index=False)
  print(f"Resolved {resolved} height measurements.")



def removeBMIOutlier():
  file = pd.read_csv(copyTitle + '/omr BMI_weight_based_3.csv')
  actual_bmis = file['actual_BMI']
  subject_id = file['subject_id']
  bmi_date = file['actual_BMI_time']
  projected_bmis = file['projected_BMI']
  percentDifferent = file['percent_difference']
  heightValues = file['closest_height']

  patient_bmis = {}
  for i in range(len(actual_bmis)):
    # key: subject id, value: list of bmi, date, and percent diff
    # convert bmi_date[i] to date object
    bmi_date_obj = datetime.strptime(bmi_date[i], '%Y-%m-%d')
    if subject_id[i] in patient_bmis:
      patient_bmis[subject_id[i]].append((actual_bmis[i], bmi_date_obj, percentDifferent[i], projected_bmis[i], i))
    else:
      patient_bmis[subject_id[i]] = [(actual_bmis[i], bmi_date_obj, percentDifferent[i], projected_bmis[i], i)]

    if (heightValues[i] < 10):
      inches = heightValues[i] * 12
      # Fix this row using loc
      file.loc[i, 'closest_height'] = inches

  # remove outliers
  # condition for outliers: percent difference is greater than 100
  # how to deal with outliers: find the closest value by time that is not an outlier and replace it
  for subject_id, measurements in patient_bmis.items():
    sorted_measurements = sorted(measurements, key=lambda x: x[1])
    for i in range(len(sorted_measurements)):
      if sorted_measurements[i][2] >= 100:
        row_index = sorted_measurements[i][4]
        # find the closest non-outlier value
        non_outlier_value = None
        non_outlier_date = None
        minimum_diff = 99999999999
        for j in range(len(sorted_measurements)):
          if (j != i) and (sorted_measurements[j][2] < 100):
              if (sorted_measurements[i][1] - sorted_measurements[j][1]).total_seconds() < minimum_diff:
                    non_outlier_value = sorted_measurements[j][0]
                    non_outlier_date = sorted_measurements[j][1]
                    minimum_diff = (sorted_measurements[i][1] - sorted_measurements[j][1]).total_seconds()

        if non_outlier_value is not None:
          # replace the outlier value with the non-outlier value
          file.loc[row_index, 'actual_BMI'] = non_outlier_value
          file.loc[row_index, 'fixed_bmi_time'] = non_outlier_date.strftime('%Y-%m-%d')
          # create a new percent difference
          file.loc[row_index, 'new_percent_difference'] = abs(non_outlier_value - sorted_measurements[i][3]) / ((sorted_measurements[i][3] + non_outlier_value) / 2) * 100
        else:
          print(f"No non-outlier value found for subject ID: {subject_id}")
          file.loc[row_index, 'actual_BMI'] = ''

  # Write to new csv file
  file.to_csv(copyTitle + '/omr BMI_weight_based_3_no_outliers.csv', index=False)

removeBMIOutlier()

# fix percent diff
# fix feet to inch