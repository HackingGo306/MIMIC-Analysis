import ollama
import pandas as pd
import random

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

# read a file
file = pd.read_csv(folderTitle + '/d_icd_diagnoses.csv')
# get the list of diagnoses
diagnoses = file['long_title'].tolist()
categories = ['Infectious Diseases', 'Cardiovascular Diseases', 'Respiratory Diseases', 'Neurological Disorders', 'Endocrine and Metabolic Disorders', 'Musculoskeletal Disorders', 'Gastrointestinal Diseases','Hematological Disorders', 'Dermatological Conditions' ,'Psychiatric and Mental Health Disorders' ,'Cancers (Oncology)' ,'Autoimmune Diseases' ,'Genetic and Congenital Disorders' ,'Eye and Vision Disorders' ,'Ear Nose and Throat (ENT) Disorders' ,'Renal and Urological Disorders' ,'Reproductive System Disorders' ,'Rare and Orphan Diseases']
categories_string = ", ".join(categories)

classification = {
  
}

batches = 20
batch_size = 10

for i in range(0, batches * batch_size, batch_size):
  if (i % (batches * batch_size // 100) == 0):
     print(i / batches / batch_size * 100, "percent")
  
  prompt = "Classify the following list of diagnoses into one of the 18 provided categories. Please provide your response as a comma-separated list, with each category corresponding to the respective diagnosis in order. The categories are as follows"
  prompt += "\n['Infectious Diseases', 'Cardiovascular Diseases', 'Respiratory Diseases', 'Neurological Disorders', 'Endocrine and Metabolic Disorders', 'Musculoskeletal Disorders', 'Gastrointestinal Diseases', 'Hematological Disorders', 'Dermatological Conditions', 'Psychiatric and Mental Health Disorders', 'Cancers (Oncology)', 'Autoimmune Diseases', 'Genetic and Congenital Disorders', 'Eye and Vision Disorders', 'Ear Nose and Throat (ENT) Disorders', 'Renal and Urological Disorders', 'Reproductive System Disorders', 'Rare and Orphan Diseases'].\nHere is the list of diagnoses:"
  for j in range(batch_size):
    prompt += "\n" + str(j + 1) + ") " + diagnoses[i + j]
    
  prompt += "\nProvide the classification results as a list of categories corresponding to each diagnosis."
  
  response = ollama.chat(
      model="llama3",
      messages=[
          {
              "role": "system",
              "content": "You are a helpful AI assistant that responds in " + str(batch_size) + " phrases",
          },
          {
              "role": "user",
              "content": prompt,
          }
      ]
  )
  
  response_string = response['message']['content']
  
  if "\n\n" in response_string:
    response_string = response_string.split("\n\n")[1]
  if "\n\n" in response_string:
    response_string = response_string.split("\n\n")[0]
    
  print(response_string)
  results =  response_string.split(',')
  
  for j in range(batch_size):
    diagnosis = diagnoses[i + j]
    classification[diagnosis] = results[j]
  
# save the classification to a csv file
classification_df = pd.DataFrame(classification.items(), columns=['Diagnosis', 'Category'])
classification_df.to_csv(copyTitle + '/d_icd_diagnoses_classification.csv', index=False)