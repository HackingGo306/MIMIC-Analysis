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
categories_string = ",".join(categories)

classification = {
  
}


amount = 100
for i in range(amount):
  if (i % (amount // 100) == 0):
    print(i / amount * 100, "percent")
  diagnosis = diagnoses[i]
  prompt = "Please categorize the following diagnosis in one of these categories: " + categories_string + "\nThe diagnosis is: " + diagnosis

  response = ollama.chat(
      model="llama3",
      messages=[
          {
              "role": "system",
              "content": "You are an AI assistant that can only respond in one phrase without punctuation",
          },
          {
              "role": "user",
              "content": prompt,
          }
      ],
  )
  classification[diagnosis] = response["message"]["content"]
  

# save the classification to a csv file
classification_df = pd.DataFrame(classification.items(), columns=['Diagnosis', 'Category'])
classification_df.to_csv(copyTitle + '/d_icd_diagnoses_classification.csv', index=False)