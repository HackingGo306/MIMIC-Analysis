# Finds all labs with more than 3000 measured patients and calculates the median value for each of the patients

import pandas as pd
import statistics

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

lab_item_frequencies = pd.read_csv(copyTitle + '/Lab Events/all_labevent_frequency.csv')

patients = {
  
}

frequency = {
  
}

df_head = pd.read_csv(folderTitle + '/labevents.csv', nrows=5000)
df_head.to_csv(copyTitle + '/Lab Events/labevents_sample.csv')

for i in range(len(lab_item_frequencies)):
  lab_id = lab_item_frequencies['item_id'][i]
  try:
    frequency[int(lab_id)] = lab_item_frequencies['patients'][i]
  except ValueError:
    print(f"Non-numeric value found for lab ID: {lab_id}")
    continue

print("Start")
  
amount = 0
batch_size = 1500000 * 10
  
for df in pd.read_csv(folderTitle + '/labevents.csv', chunksize=batch_size):
  for i in range(len(df)):
    if (i % (batch_size / 10) == 0):
      print(100 * (i / len(df)), "percent, ")
      
    index = i + amount * batch_size
    lab_id = df.at[index, 'itemid']
    
    try: 
      if (frequency[lab_id] < 3000):
        continue
    except KeyError:
      print(f"Lab ID not found in frequency: {lab_id}")
      continue
    
    patient_id = df['subject_id'][index]
    valuenum = df['valuenum'][index]
    
    if (patient_id in patients):
      if (lab_id in patients[patient_id]):
        patients[patient_id][lab_id].append(valuenum)
      else:
        patients[patient_id][lab_id] = [valuenum]
    else:
      patients[patient_id] = {lab_id: [valuenum]}
      
  amount += 1
  print(amount, "read")
  
  
print(len(patients.items()))

# create dataframe
output_data = []

for patient_id, lab_counts in patients.items():
  row = {'subject_id': patient_id}
  for lab_id, val in lab_counts.items():
    median_value = statistics.median(val)
    row[lab_id] = median_value
  
  output_data.append(row)

output_file = pd.DataFrame(output_data)

# Write it to a file inside hosp copy
output_file.to_csv(copyTitle + '/Lab Events/patient_lab_medians.csv', index=False)
print("Finished")