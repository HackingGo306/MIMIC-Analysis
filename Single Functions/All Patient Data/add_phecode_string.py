# Add specific phecode_string columns (true/false) to the output of the add_diagnosis_categories.py file

import pandas as pd

version = '3.0'
folderTitle = f'/Users/cameron/mimic-iv-{version}/hosp'
copyTitle = f'/Users/cameron/mimic-iv-{version}/hosp copy'

patient_demographics = pd.read_csv(copyTitle + "/All Patient Data/training_data_base.csv")
patient_phecodes = pd.read_csv(copyTitle + "/All Patient Data/all_patient_phecodes.csv")

phecode_map = pd.read_csv(folderTitle + "/phecode_map1.2.csv")
categorizer = {
  
}

for i in range(len(phecode_map)):
  phecode = str(phecode_map['Phecode'][i])
  phecode_string = phecode_map['PhecodeString'][i]
  categorizer[phecode] = phecode_string

patient_data = {
  
}

# selected_categories = ['Pathologic fracture', 'Pathologic fracture of femur', 'Pathologic fracture of vertebrae', 'Malunion and nonunion of fracture', 'Fracture of tibia and fibula', 'Fracture of lower limb', 'Stress fracture', 'Fracture of unspecified part of femur', 'Fracture of neck of femur', 'Fracture of ankle and foot', 'Fracture of radius and ulna', 'Fracture of vertebral column without mention of spinal cord injury', 'Fracture of hand or wrist']
selected_categories = [
  "Skull and face fracture and other intercranial injury",
  "Fracture of vertebral column without mention of spinal cord injury",
  "Fracture of ribs",
  "Fracture of unspecified part of femur",
  "Fracture of neck of femur",
  "Pathologic fracture",
  "Fracture of tibia and fibula",
  "Fracture of radius and ulna",
  "Pathologic fracture of vertebrae",
  "Fracture of pelvis",
  "Fracture of humerus",
  "Fracture of clavicle or scapula",
  "Fracture of ankle and foot",
  "Fracture of lower limb",
  "Fracture of foot",
  "Fracture of hand or wrist",
  "Fracture of unspecified bones",
  "Malunion and nonunion of fracture",
  "Fracture of patella",
  "Fracture of upper limb",
  "Pathologic fracture of femur",
  "Stress fracture",
  "Colles' fracture"
]


selected_categories = [
  # 20 most frequent diagnosis categories (removed those like "other" or unrelated)
  "Essential hypertension",
  "Hyperlipidemia",
  "Tobacco use disorder",
  "GERD",
  "Acute renal failure",
  "Coronary atherosclerosis",
  "Type 2 diabetes",
  "Anxiety disorder",
  "Atrial fibrillation",
  "Other anemias",
  "Urinary tract infection",
  "Major depressive disorder",
  "Acute posthemorrhagic anemia",
  "Hypothyroidism NOS",
  "Hypovolemia",
  "Obesity",
  "Myocardial infarction",
  "Respiratory failure",
  "Hypertensive chronic kidney disease",
  "Hyposmolality and/or hyponatremia",
  
  # 20 most freqeuent msk-related categories (with some repeats removed)
  "Osteoarthrosis NOS",
  "Osteoporosis NOS",
  "Pain in joint",
  "Spondylosis without myelopathy",
  "Osteoarthrosis, localized, primary",
  "Spinal stenosis",
  "Spinal stenosis of lumbar region",
  "Rheumatoid arthritis",
  "Osteoarthritis; localized",
  "Osteopenia or other disorder of bone and cartilage",
  "Other disorders of bone and cartilage",
  "Displacement of intervertebral disc",
  "Arthropathy NOS",
  "Unspecified osteomyelitis",
  "Other disorders of soft tissues",
  "Degeneration of intervertebral disc",
  "Chronic osteomyelitis",
  "Kyphoscoliosis and scoliosis",
  "Acute osteomyelitis",
  "Polymyalgia Rheumatica",
]

selected_categories = [
  "Cerebral laceration and contusion",
  "Concussion",
  "Intracranial hemorrhage (injury)",
  "Subdural hemorrhage (injury)",
  "Subarachnoid hemorrhage (injury)",
  "Skull and face fracture and other intercranial injury",
  "Torus fracture",
  "Dislocation",
  "Internal derangement of knee",
  "Traumatic arthropathy",
  "Sprains and strains",
  "Muscle/tendon sprain",
  "Rotator cuff (capsule) sprain",
  "Joint/ligament sprain",
  "Sprains and strains of back and neck",
  "Other sprains and strains",
  "Hemorrhage or hematoma complicating a procedure",
  "Complications of transplants and reattached limbs",
  "Complication of colostomy or enterostomy",
  "Complications of cardiac/vascular device, implant, and graft",
  "Complication of nervous system device, implant, and graft",
  "Vascular complications of surgery and medical procedures",
  "Mechanical complication of unspecified genitourinary device, implant, and graft",
  "Complication due to other implant and internal device",
  "Open wounds of head; neck; and trunk",
  "Open wound or laceration of eye or eyelid",
  "Open wound of ear",
  "Other open wound of head and face",
  "Open wound of nose and sinus",
  "Open wound of lip and mouth",
  "Open wound of neck",
  "Open wound of genital organs",
  "Open wounds of extremities",
  "Open wound of hand except finger(s)",
  "Open wound of finger(s)",
  "Open wound of foot except toe(s) alone",
  "Open wound of toe(s)",
  "Traumatic amputation",
  "Broken tooth",
  "Complication of amputation stump",
  "Non-healing surgical wound",
  "Posttraumatic wound infection not elsewhere classified",
  "Late effects of musculoskeletal and connective tissue injuries",
  "Late effects of injuries to skin and subcutaneous tissues",
  "Injuries to the nervous system",
  "Late effects of other injuries",
  "Late effects of external causes",
  "Superficial injury, infected",
  "Blister",
  "Insect bite",
  "Toxic effect of venom",
  "Superficial injury without mention of infection",
  "Contusion",
  "Allergic reaction to food",
  "Adverse reaction to serum or vaccine",
  "Infusion and transfusion reaction",
  "Anaphylactic shock NOS",
  "Allergies, other",
  "Diaper or napkin rash",
  "Spinal cord injury without evidence of spinal bone injury",
  "Injury to other and unspecified nerves",
  "Certain early complications of trauma or procedure",
  "Postoperative shock",
  "Traumatic and surgical subcutaneous emphysema",
  "Poisoning by antibiotics",
  "Adverse effects of antibacterials (not penicillins)",
  "Allergy/adverse effect of penicillin",
  "Poisoning by antifungal antibiotics",
  "Poisoning by other anti-infectives",
  "Poisoning/allergy of sulfonamides",
  "Poisoning by hormones and synthetic substitutes",
  "Adrenal cortical steroids causing adverse effects in therapeutic use",
  "Insulins and antidiabetic agents causing adverse effects in therapeutic use",
  "Hormones and synthetic substitutes causing adverse effects in therapeutic use",
  "Poisoning by primarily systemic agents",
  "Antineoplastic and immunosuppressive drugs causing adverse effects",
  "Poisoning by agents primarily affecting blood constituents",
  "Anticoagulants causing adverse effects",
  "Poisoning by analgesics, antipyretics, and antirheumatics",
  "Opiates and related narcotics causing adverse effects in therapeutic use",
  "Antirheumatics causing adverse effects in therapeutic use",
  "Salicylates causing adverse effects in therapeutic use",
  "Poisoning by anticonvulsants and anti-Parkinsonism drugs",
  "Adverse effects of sedatives or other central nervous system depressants and anesthetics",
  "Poisoning by psychotropic agents",
  "Poisoning by drugs primarily affecting the autonomic nervous system",
  "Poisoning by agents primarily affecting the cardiovascular system",
  "Cardiac rhythm regulators causing adverse effects in therapeutic use",
  "Antilipemic and antiarteriosclerotic drugs causing adverse effects in therapeutic use",
  "Antihypertensive agents causing adverse effects",
  "Poisoning by agents primarily affecting the gastrointestinal system",
  "Poisoning by water, mineral, and uric acid metabolism drugs",
  "Poisoning by agents primarily acting on the smooth and skeletal muscles and respiratory system",
  "Poisoning by agents primarily affecting skin & mucous membrane, ophthalmological, otorhinolaryngological, & dental drugs",
  "Personal history of allergy to medicinal agents",
  "Adverse drug events and drug allergies",
  "Toxic effect of (non-ethyl) alcohol and petroleum and other solvents",
  "Toxic effect of corrosive aromatics, acids, and caustic alkalis",
  "Toxic effect of lead and its compounds (including fumes)",
  "Toxic effect of other metals",
  "Toxic effect of carbon monoxide",
  "Toxic effect of other gases, fumes, or vapors",
  "Toxic effect of noxious substances eaten as food",
  "Toxic effect of other substances, chiefly nonmedicinal as to source",
  "Effects radiation NOS",
  "Sepsis and SIRS",
  "Systemic inflammatory response syndrome (SIRS)",
  "Sepsis",
  "Septic shock",
  "Complications peculiar to certain specified procedures",
  "Osteomyelitis, periostitis, and other infections involving bone",
  "Osteomyelitis",
  "Acute osteomyelitis",
  "Chronic osteomyelitis",
  "Unspecified osteomyelitis",
  "Periostitis",
  "Osteopathy resulting from poliomyelitis",
  "Arthropathy associated with infections",
  "Pyogenic arthritis",
  "Reiter's disease",
  "Behcet's syndrome",
  "Infective connective tissue disorders",
  "Arthropathy associated with other disorders classified elsewhere",
  "Arthropathy associated with neurological disorders",
  "Rheumatoid arthritis and other inflammatory polyarthropathies",
  "Rheumatoid arthritis",
  "Juvenile rheumatoid arthritis",
  "Other inflammatory spondylopathies",
  "Sacroiliitis NEC",
  "Ankylosing spondylitis",
  "Spinal enthesopathy",
  "Other arthropathies",
  "Unspecified polyarthropathy or polyarthritis",
  "Unspecified monoarthritis",
  "Kaschin-Beck disease",
  "Palindromic rheumatism",
  "Arthropathy NOS",
  "Polymyalgia Rheumatica",
  "Spinal stenosis",
  "Spinal stenosis of lumbar region",
  "Spondylosis and allied disorders",
  "Spondylosis without myelopathy",
  "Spondylosis with myelopathy",
  "Other allied disorders of spine",
  "Intervertebral disc disorders",
  "Displacement of intervertebral disc",
  "Schmorl's nodes",
  "Degeneration of intervertebral disc",
  "Intervertebral disc disorder with myelopathy",
  "Postlaminectomy syndrome",
  "Other and unspecified disc disorder",
  "Other disorders of cervical region",
  "Torticollis",
  "Other and unspecified disorders of back",
  "Disorders of sacrum",
  "Disorders of coccyx",
  "Other symptoms referable to back",
  "Other unspecified back disorders",
  "Peripheral enthesopathies and allied syndromes",
  "Enthesopathy",
  "Synoviopathy",
  "Bursitis",
  "Calcaneal spur; Exostosis NOS",
  "Other disorders of synovium, tendon, and bursa",
  "Synovitis and tenosynovitis",
  "Bursitis disorders",
  "Ganglion and cyst of synovium, tendon, and bursa",
  "Rupture of synovium",
  "Rupture of tendon, nontraumatic",
  "Contracture of tendon (sheath)",
  "Plica syndrome",
  "Disorders of muscle, ligament, and fascia",
  "Muscular calcification and ossification",
  "Laxity of ligament or hypermobility syndrome",
  "Fasciitis",
  "Contracture of palmar fascia [Dupuytren's disease]",
  "Other disorders of soft tissues",
  "Rheumatism, unspecified and fibrositis",
  "Panniculitis",
  "Nontraumatic compartment syndrome",
  "Osteitis deformans and osteopathies associated with other disorders classified elsewhere",
  "Osteitis deformans [Paget's disease of bone]",
  "Osteochondropathies",
  "Juvenile osteochondrosis",
  "Osteochondritis dissecans",
  "Other disorders of bone and cartilage",
  "Cyst of bone",
  "Aseptic necrosis of bone",
  "Costochondritis",
  "Malunion and nonunion of fracture",
  "Chondromalacia",
  "Acquired foot deformities",
  "Flat foot",
  "Acquired toe deformities",
  "Hammer toe (acquired)",
  "Claw toe (acquired)",
  "Hallux rigidus",
  "Hallux valgus (Bunion)",
  "Other acquired deformities of limbs",
  "Acquired deformities of forearm",
  "Acquired deformities of finger",
  "Acquired deformities of hip",
  "Genu valgum or varum (acquired)",
  "Acquired deformities of knee",
  "Unequal leg length (acquired)",
  "Curvature of spine",
  "Kyphosis (acquired)",
  "Lordosis (acquired)",
  "Kyphoscoliosis and scoliosis",
  "Other acquired musculoskeletal deformity",
  "Acquired spondylolisthesis",
  "Contracture of joint",
  "Osteoarthrosis",
  "Osteoarthritis; localized",
  "Osteoarthrosis, localized, primary",
  "Osteoarthrosis, localized, secondary",
  "Osteoarthrosis, generalized",
  "Osteoarthrosis involving more than one site, but not specified as generalized",
  "Osteoarthrosis NOS",
  "Symptoms and disorders of the joints",
  "Ankylosis of joint",
  "Stiffness of joint",
  "Difficulty in walking",
  "Joint effusions",
  "Hemarthrosis",
  "Villonodular synovitis",
  "Derangement of joint, non-traumatic",
  "Loose body in joint",
  "Pathological, developmental or recurrent dislocation",
  "Articular cartilage disorder",
  "Other derangement of joint",
  "Osteoporosis, osteopenia and pathological fracture",
  "Osteoporosis",
  "Osteoporosis NOS",
  "Senile osteoporosis",
  "Other specified osteoporosis",
  "Pathologic fracture",
  "Pathologic fracture of vertebrae",
  "Pathologic fracture of femur",
  "Stress fracture",
  "Osteopenia or other disorder of bone and cartilage",
  "Pain in joint"
]

include = {}
for cat in selected_categories:
  include[cat] = True
  patient_demographics[cat] = False

for i in range(len(patient_phecodes)):
  if (i % 10000 == 0):
    print("Part 1:",(i/len(patient_phecodes) * 100),"% percent")
  subject_id = str(patient_phecodes['subject_id'][i])
  if (pd.isna(patient_phecodes['phecodes'][i])): continue
  patient_data[subject_id] = {}
  try:
    phecode_strings = str(patient_phecodes['phecodes'][i]).split(", ")
    for string in phecode_strings: 
      phecode_string = categorizer[string]
      if (phecode_string in include):
        patient_data[subject_id][phecode_string] = True
  except KeyError:
    pass
  
for i in range(len(patient_demographics)):
  if (i % 10000 == 0):
    print("Part 2:",(i/len(patient_demographics) * 100),"% percent")
  subject_id = str(patient_demographics['subject_id'][i])
  try:
    for category in patient_data[subject_id].keys():
      patient_demographics.at[i, category] = True 
  except KeyError:
    pass # Not all patients have phecode diagnoses
    
# Remove first column (column 1)
# patient_demographics.drop("Unnamed: 0", axis=1, inplace=True)

patient_demographics.to_csv(copyTitle + "/All Patient Data/training_data_with_all_conditions.csv", index=False)