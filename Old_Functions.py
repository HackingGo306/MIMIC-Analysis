import pandas as pd
import numpy as np
from datetime import datetime

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

def add_long_title():
  diagnosis_codes = pd.read_csv(folderTitle + "/d_icd_diagnoses.csv")
  lookup = {}
  codes = diagnosis_codes[['long_title', 'icd_code']].values

  for i in range(len(codes)):
    parsed_code = codes[i][0]
    parsed_code = parsed_code.split(",")[0]
    lookup[codes[i][1]] = parsed_code

  diagnosis_patients = pd.read_csv(folderTitle + "/diagnoses_icd.csv")
  diagnosis_patients['diagnosis_description'] = diagnosis_patients['icd_code'].map(lookup)
  header = list(diagnosis_patients.columns)
  diagnosis_patients.to_csv(copyTitle + '/diagnoses_icd_no_unspecified.csv', columns = header)

def omr_events_mean():
  omr_measurments = pd.read_csv(folderTitle + "/hosp/omr.csv")
  measurment_names = omr_measurments['result_name'].values
  result_values = omr_measurments['result_value'].values

  weight_lbs = []
  weight = []

  height_inches = []
  height = []

  for i in range(0, len(result_values)):
    if (measurment_names[i] == 'Weight (Lbs)'):
      weight_lbs.append(float(result_values[i]))
    elif (measurment_names[i] == 'Weight'):
      weight.append(float(result_values[i]))
    elif (measurment_names[i] == 'Height (Inches)'):
      height_inches.append(float(result_values[i]))
    elif (measurment_names[i] == "Height"):
      height.append(float(result_values[i]))

  print("Mean for Weight (Lbs):", np.mean(weight_lbs), "\nMedian for Weight (Lbs):", np.median(weight_lbs), "\nStandard deviation", np.std(weight_lbs, ddof=1))
  print("Mean for Weight:", np.mean(weight), "\nMedian for Weight:", np.median(weight), "\nStandard deviation:", np.std(weight, ddof=1))

  print("Mean for Height (Inches):", np.mean(height_inches), "\nMedian for Weight (Inches):", np.median(height_inches), "\nStandard deviation", np.std(height_inches, ddof=1))
  print("Mean for Height:", np.mean(height), "\nMedian for Height:", np.median(height), "\nStandard deviation:", np.std(height, ddof=1))


def seperateOmrRows_measurement():
  omr_measurments = pd.read_csv(folderTitle + "/omr.csv")
  measurement_types = ['BMI', 'BMI (kg/m2)', 'eGFR', 'Height', 'Height (Inches)', 'Weight', 'Weight (Lbs)']
  measurement_filenames = ['BMI', 'BMI_kg', 'eGFR', 'Height', 'Height_in', 'Weight', 'Weight_lb']
  for i in range(len(measurement_types)):
    measurement = measurement_types[i]
    copy_filename = measurement_filenames[i]
    new_df = omr_measurments[omr_measurments['result_name'] == measurement]
    new_df.to_csv(copyTitle + '/omr ' + copy_filename + '.csv', index=False)


def seperateOmrRows_blood():
  omr_measurments = pd.read_csv(folderTitle + "/omr.csv")
  blood_pressures = ['Blood Pressure', 'Blood Pressure Lying', "Blood Pressure Sitting", 'Blood Pressure Standing', 'Blood Pressure Standing (1 min)', 'Blood Pressure Standing (3 mins)']
  blood_filenames = ['BP', 'BP_Lying', 'BP_Sitting', 'BP_Standing', 'BP_Standing_1', 'BP_Standing_3']
  for i in range(len(blood_pressures)):
    blood_pressure = blood_pressures[i]
    copy_filename = blood_filenames[i]
    new_df = omr_measurments[omr_measurments['result_name'] == blood_pressure]
    # Split systolic blood pressure and diastolic blood pressure
    new_df['systolic'] = new_df['result_value'].apply(lambda x: x.split('/')[0])
    new_df['diastolic'] = new_df['result_value'].apply(lambda x: x.split('/')[1])
    new_df = new_df[['subject_id', 'chartdate','seq_num','result_name','systolic', 'diastolic']]
    new_df.to_csv(copyTitle + '/omr ' + copy_filename + '.csv', index=False)


def visualizeOutlierTrends():
  omr_BMI_kg = pd.read_csv(copyTitle + "/omr BMI_kg.csv")
  omr_BMI_ids = omr_BMI_kg['subject_id']
  omr_BMI_values = omr_BMI_kg['result_value']

  omr_Weight_lb = pd.read_csv(copyTitle + "/omr Weight_lb.csv")
  omr_Weight_values = omr_Weight_lb['result_value']
  omr_Weight_ids = omr_Weight_lb['subject_id']

  omr_Height_in = pd.read_csv(copyTitle + "/omr Height_in.csv")
  omr_Height_values = omr_Height_in['result_value']
  omr_Height_ids = omr_Height_in['subject_id']

  median = np.median(omr_BMI_values)
  std = np.std(omr_BMI_values)
  print("Median BMI is", median, "and standard deviation is", std)
  three_sigma = []
  for i in range(len(omr_BMI_values)):
    value = omr_BMI_values[i]
    sub_id = omr_BMI_ids[i]
    if abs(value - median) > 3 * std:
      three_sigma.append({"value": value, "subject_id": sub_id})

  print(len(three_sigma), "values lie outside 3 standard deviation")
  outlier_data = {}
  outlier_values = {}
  for i in range(len(three_sigma)):
    subject_id = three_sigma[i]['subject_id']
    outlier_data[subject_id] = {"weight": omr_Weight_values[omr_Weight_ids == subject_id].values, "height": omr_Height_values[omr_Height_ids == subject_id].values}
    if (subject_id in outlier_values):
      outlier_values[subject_id].append(three_sigma[i]['value'])
    else:
      outlier_values[subject_id] = [three_sigma[i]['value']]

    print("----- Patient Id:", subject_id, "-----")
    print("BMI Values:", outlier_values[subject_id])
    print("Height:", outlier_data[subject_id]['height'].tolist())
    print("Weight:", outlier_data[subject_id]['weight'].tolist(), "\n")

def addHeightWeightColumns(): # Average the height and weight of each BMI patient and add it to the row
  omr_BMI_kg = pd.read_csv(copyTitle + "/omr BMI_kg.csv")
  omr_BMI_ids = omr_BMI_kg['subject_id']
  omr_BMI_values = omr_BMI_kg['result_value']

  omr_Weight_lb = pd.read_csv(copyTitle + "/omr Weight_lb.csv")
  omr_Weight_values = omr_Weight_lb['result_value']
  omr_Weight_ids = omr_Weight_lb['subject_id']

  omr_Height_in = pd.read_csv(copyTitle + "/omr Height_in.csv")
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
  for i in range(len(omr_BMI_ids)):
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

  omr_BMI_kg_copy.to_csv(copyTitle + '/omr BMI_height_weight_details.csv', index=False)

def calculateBMI():
  omr_BMI_kg_copy = pd.read_csv(copyTitle + "/omr BMI_height_weight_details.csv")
  omr_BMI_ids = omr_BMI_kg_copy['subject_id']
  omr_weight_values = omr_BMI_kg_copy['avg_weight']
  omr_height_values = omr_BMI_kg_copy['avg_height']

  for i in range(len(omr_BMI_ids)):
    weight = float(omr_weight_values[i])
    height = float(omr_height_values[i])
    if (weight > 0 and height > 0): 
      bmi = (weight * 0.453592) / ((height * 0.0254) ** 2)
      omr_BMI_kg_copy.loc[i, 'projected_bmi'] = bmi

  # Write to new csv file
  omr_BMI_kg_copy.to_csv(copyTitle + '/omr BMI_height_weight_details_with_BMI.csv', index=False)

def replaceOutlierWeightHeight():
  # If it's outside the acceptable range and outside 2 median and standard deviation replace it with the most recent acceptable value
  omr_BMI_kg = pd.read_csv(copyTitle + "/omr BMI_kg.csv")
  omr_BMI_ids = omr_BMI_kg['subject_id']
  omr_BMI_values = omr_BMI_kg['result_value']

  omr_Weight_lb = pd.read_csv(copyTitle + "/omr Weight_lb.csv")
  omr_Weight_values = omr_Weight_lb['result_value']
  omr_Weight_ids = omr_Weight_lb['subject_id']
  omr_Weight_times = omr_Weight_lb['chartdate']

  omr_Height_in = pd.read_csv(copyTitle + "/omr Height_in.csv")
  omr_Height_values = omr_Height_in['result_value']
  omr_Height_ids = omr_Height_in['subject_id']
  omr_Height_times = omr_Height_in['chartdate']
  
  patient_weights = {}
  patient_heights = {}

  for i in range(len(omr_Weight_ids)):
    subject_id = omr_Weight_ids[i]
    weight = float(omr_Weight_values[i])
    date = datetime.strptime(omr_Weight_times[i], "%Y-%m-%d")

    if (subject_id in patient_weights):
      patient_weights[subject_id].append({'weight': weight, 'date': date})
    else:
      patient_weights[subject_id] = [{'weight': weight, 'date': date}]

  for i in range(len(omr_Height_ids)):
    subject_id = omr_Height_ids[i]
    try:
      height = float(omr_Height_values[i])
    except ValueError:
      continue
    date = datetime.strptime(omr_Height_times[i], "%Y-%m-%d")

    if (subject_id in patient_heights):
      patient_heights[subject_id].append({'height': height, 'date': date})
    else:
      patient_heights[subject_id] = [{'height': height, 'date': date}]


  height_table = omr_Height_in.copy()
  print("HEIGHT", height_table.shape[0])

  for i in range(height_table.shape[0]):
    if (i % 1000) == 0:
      print(i)
    row = height_table.loc[i]
    subject_id = row['subject_id']
    if (subject_id in patient_heights.keys()):
      # print(patient_heights[subject_id])
      try:
        original_height = float(row['result_value'])
        original_date = datetime.strptime(row['chartdate'], "%Y-%m-%d")
        height_table.loc[i, 'initial'] = original_height
        if (original_height > 107 or original_height < 1):
            # Taller than tallest man in the world or shorter than newborn height
            most_recent_acceptable = -1
            minimum_diff = 9999999999999
            # get the height value with the closest date value by comparing the two time objects
            for p in patient_heights[subject_id]:
              if (p['date'] - original_date).total_seconds() < minimum_diff:
                if (p['height'] > 1 and p['height'] < 107):
                  minimum_diff = abs(p['date'] - original_date).total_seconds()
                  most_recent_acceptable = p['height']

            height_table.loc[i, 'result_value'] = most_recent_acceptable
      except ValueError:
        continue

  weight_table = omr_Weight_lb.copy()
  print("WEIGHT:", weight_table.shape[0])
  for i in range(weight_table.shape[0]):
    if (i % 1000) == 0:
      print(i)  
    row = weight_table.loc[i]
    subject_id = row['subject_id']
    if (subject_id in patient_weights.keys()):
      weight_values = [p['weight'] for p in patient_weights[subject_id]]
      weight_median = np.median(weight_values)
      original_weight = float(row['result_value'])
      original_date = datetime.strptime(row['chartdate'], "%Y-%m-%d")
      weight_table.loc[i, 'initial'] = original_weight

      if (original_weight > 1500 or original_weight < 5): # Not a real weight
        most_recent_acceptable = -1
        minimum_diff = 99999999999
        for p in patient_weights[subject_id]:
          if (p['date'] - original_date).total_seconds() < minimum_diff:
            if (p['weight'] > 5 and p['weight'] < 1500):
              minimum_diff = abs(p['date'] - original_date).total_seconds()
              most_recent_acceptable = p['weight']

        weight_table.loc[i, 'result_value'] = most_recent_acceptable
  
  weight_table.to_csv(copyTitle + '/omr Weight_lb_replaced.csv', index=False)
  height_table.to_csv(copyTitle + '/omr Height_in_replaced.csv', index=False)

def addReplacedHeightWeightColumns():
  print("Using Median")
  # Used the replaced table and add those columns to the new BMI table
  omr_BMI_kg = pd.read_csv(copyTitle + "/omr BMI_kg.csv")
  omr_BMI_ids = omr_BMI_kg['subject_id']

  omr_Weight_lb = pd.read_csv(copyTitle + "/omr Weight_lb_replaced.csv")
  omr_Weight_values = omr_Weight_lb['result_value']
  omr_Weight_ids = omr_Weight_lb['subject_id']

  omr_Height_in = pd.read_csv(copyTitle + "/omr Height_in_replaced.csv")
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
      height_avg = np.median(patient_heights[subject_id])
      height_max = np.max(patient_heights[subject_id])
      height_min = np.min(patient_heights[subject_id])
      height_len = len(patient_heights[subject_id])
      omr_BMI_kg_copy.loc[i, 'median_height'] = height_avg
      omr_BMI_kg_copy.loc[i, 'max_h'] = height_max
      omr_BMI_kg_copy.loc[i, 'min_h'] = height_min
      omr_BMI_kg_copy.loc[i, 'n_h'] = height_len
    if (subject_id in patient_weights):
      # repeat same process for weight
      weight_avg = np.median(patient_weights[subject_id])
      weight_max = np.max(patient_weights[subject_id])
      weight_min = np.min(patient_weights[subject_id])
      weight_len = len(patient_weights[subject_id])
      omr_BMI_kg_copy.loc[i, 'median_weight'] = weight_avg
      omr_BMI_kg_copy.loc[i, 'max_w'] = weight_max
      omr_BMI_kg_copy.loc[i, 'min_w'] = weight_min
      omr_BMI_kg_copy.loc[i, 'n_w'] = weight_len

  omr_BMI_kg_copy.to_csv(copyTitle + '/omr BMI_height_weight_replaced.csv', index=False)

def calculateFilteredBMI(): # Create a column of the projected BMI using the filtered height and weight values
  omr_BMI_kg_copy = pd.read_csv(copyTitle + "/omr BMI_height_weight_replaced.csv")
  omr_BMI_ids = omr_BMI_kg_copy['subject_id']
  omr_weight_values = omr_BMI_kg_copy['median_weight']
  omr_height_values = omr_BMI_kg_copy['median_height']
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
  omr_BMI_kg_copy.to_csv(copyTitle + '/omr BMI_height_weight_replaced_projected.csv', index=False)


def removeOutlierBMI(): # Filter outlier weight and height using standard deviation and median (only if it lies outside the acceptable range)
  omr_BMI_kg = pd.read_csv(copyTitle + "/omr BMI_kg.csv")
  omr_BMI_ids = omr_BMI_kg['subject_id']
  omr_BMI_values = omr_BMI_kg['result_value']

  omr_Weight_lb = pd.read_csv(copyTitle + "/omr Weight_lb.csv")
  omr_Weight_values = omr_Weight_lb['result_value']
  omr_Weight_ids = omr_Weight_lb['subject_id']

  omr_Height_in = pd.read_csv(copyTitle + "/omr Height_in.csv")
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

  height_table = omr_Height_in.copy()
  print("HEIGHT", height_table.shape[0])
  for i in range(height_table.shape[0]):
    if (i % 1000) == 0:
      print(i)
    row = height_table.loc[i]
    subject_id = row['subject_id']
    if (subject_id in patient_heights.keys()):
      height_median = np.median(patient_heights[subject_id])
      height_mean = np.mean(patient_heights[subject_id])
      height_std = np.std(patient_heights[subject_id])
      # get range within 2 standard deviations
      low_range = height_mean + 2 * height_std
      high_range = height_mean - 2 * height_std
      if type(row['result_value']) == float:
        original_height = row['result_value']
        height_table.loc[i, 'initial'] = original_height
        # if (original_height < height_median / 1.5 or original_height > height_median * 1.5):
        if (original_height < low_range or original_height > high_range):
          if (original_height > 107 or original_height < 1): # Taller than tallest man in the world or shorter than newborn height
            height_table.loc[i, 'result_value'] = height_median

  weight_table = omr_Weight_lb.copy()
  print("WEIGHT:", weight_table.shape[0])
  for i in range(weight_table.shape[0]):
    if (i % 1000) == 0:
      print(i)  
    row = weight_table.loc[i]
    subject_id = row['subject_id']
    if (subject_id in patient_weights.keys()):
      weight_median = np.median(patient_weights[subject_id])
      original_weight = float(row['result_value'])
      weight_table.loc[i, 'initial'] = original_weight
      if (original_weight < weight_median / 2 or original_weight > weight_median * 2):
        if (original_weight > 1500 or original_weight < 5): # Not a real weight
          weight_table.loc[i, 'result_value'] = weight_median
  
  weight_table.to_csv(copyTitle + '/omr Weight_lb_corrected_range.csv', index=False)
  height_table.to_csv(copyTitle + '/omr Height_in_corrected_range.csv', index=False)