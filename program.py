"""Preprocess of the covid-19 data analysis;
    we assume that we have 3 symptoms columns, CT and Xray columns"""

'''
Data processing Steps:
1. getting original data from two csv files(one csv file contains symptoms data).
2. Analyzing data using EDA. 
3. Count finding values. We have confirmed 584 COVID-19 cases, 283 confirmed NON-COVID-19 cases and 83 cases which are not yet done.
4. Update finding values for todo cases using step 2.
5. Update survival values for todo cases using step 2.
6. Add symptoms from another dataset using step 2.
7. Fill all NA values using the information got from step2.
8. Process location/country field.
9. Remove some covid cases to adjust CT/Xray image count using step 2.
10. Add CT and Xray image names to the dataset.
11. Rearrange the order of the dataset.
12. Prepare the new dataset.        
'''

import csv
import glob
import os
import random

main_data = []
symptoms_data = []

'''Define the column index of main dataset'''
columns = {
    "patientid": 0,
    "symptom1": 1,
    "symptom2": 2,
    "symptom3": 3,
    "CT": 4,
    "Xray": 5,
    "offset": 6,
    "sex": 7,
    "age": 8,
    "finding": 9,
    "RT_PCR_positive": 10,
    "survival": 11,
    "intubated": 12,
    "intubation_present": 13,
    "went_icu": 14,
    "in_icu": 15,
    "needed_supplemental_O2": 16,
    "extubated": 17,
    "temperature": 18,
    "pO2_saturation": 19,
    "leukocyte_count": 20,
    "neutrophil_count": 21,
    "lymphocyte_count": 22,
    "view": 23,
    "modality": 24,
    "date": 25,
    "location": 26,
    "folder": 27,
    "filename": 28,
    "doi": 29,
    "url": 30,
    "license_d": 31,
    "clinical_notes": 32,
    "other_notes": 33,
}

'''STEP-1: Copy clinical data from main_data_file.csv '''
with open('main_data_file.csv', 'r', errors='ignore') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    # readCSV.next()
    for row in readCSV:
        main_data.append(row)

'''Copy symptomatic from data.csv '''
with open('data.csv', 'r', errors='ignore') as csvfile2:
    readCSV2 = csv.reader(csvfile2, delimiter=',')
    for row in readCSV2:
        symptoms_data.append(row)

'''STEP-2: This step is done in a jupyter notebook'''

''''STEP-3: Count total no of COVID-19 cases in total dataset '''
def totalCovidCaseCount():
    covidCases = [data[columns['finding']] for data in main_data if data[columns['finding']]=="COVID-19"]
    return len(covidCases)


''' STEP-4:
We have 584 direct covid-19 cases,283 non-covid cases and 83 cases where their finding value is todo. 
    We will update this value with either covid or non-covid based on some condition.
    If the corresponding survival value is Y then finding is non-covid, -> 45 cases
    else If the corresponding survival value is N then finding is covid, ->22 cases
    else update randomly. -16 random cases 
    eventually total covid cases will be 584+22+random number(upto 22)= 606+random number(upto 22)
    '''
def randomFindingFilling():
    randIndex = random.randint(0, 1)
    findings = ["COVID-19", "NON-COVID-19"]
    return findings[randIndex]

for index, data in enumerate(main_data):
    if index is not 0:
        if "COVID-19" in data[columns['finding']]:
            main_data[index][columns['finding']] = "COVID-19"
        elif data[columns['finding']]=="todo":
            if "Y" in data[columns['survival']]:
                main_data[index][columns['finding']] = "NON-COVID-19"
            elif "N" in data[columns['survival']]:
                main_data[index][columns['finding']] = "COVID-19"
            else:
                main_data[index][columns['finding']] = randomFindingFilling()
        else:
            main_data[index][columns['finding']] = "NON-COVID-19"

totalCovidCaseCount()


'''STEP-5: As in the main dataset, there are lots of missing values in the survival column, we need to fill this logically'''
# Fill survival missing values in the main dataset
# if finding is COVID , patient went to icu then -> survived=0
# if finding is COVID , patient went_icu is false then -> survived=1
# if finding is not COVID , patient went to icu then -> survived=1
# else randomly choose -> survived=0 or survived=1
def fillRandomSurvival():
    return random.randint(0, 1)

for index, dt in enumerate(main_data):
    if index is not 0:
        if "Y" in main_data[index][columns['survival']]:
            main_data[index][columns['survival']] = 1  # update survival=1 if survival=Y
        elif "N" in main_data[index][columns['survival']]:
            main_data[index][columns['survival']] = 0  # update survival=0 if survival=N
        else:
            if dt[columns['finding']]=="COVID-19" and "Y" in dt[columns['went_icu']]:
                main_data[index][columns['survival']] = 0
            elif dt[columns['finding']]=="COVID-19"  and "Y" not in dt[columns['went_icu']]:
                main_data[index][columns['survival']] = 1
            elif dt[columns['finding']]=="NON-COVID-19":
                main_data[index][columns['survival']] = 1
            else:
                main_data[index][columns['survival']] = fillRandomSurvival()


'''STEP-6: Add symptoms to the dataset'''
#Fill NA values of symptoms1,2,3
def fillSymptoms():
    symptoms_list = ['fever',
                     'throat pain',
                     'fatigue',
                     'vomiting',
                     'nausea',
                     'difficulty breathing',
                     'joint pain',
                     'chills',
                     'headache',
                     'throat discomfort',
                     'malaise',
                     'sore body',
                     'flu symptoms',
                     'reflux',
                     'physical discomfort',
                     'tired',
                     'myalgia',
                     'runny nose',
                     'cough with sputum',
                     'abdominal pain',
                     'diarrhea',
                     'loss of appetite',
                     'pneumonia',
                     'muscle pain',
                     'nasal discharge',
                     'respiratory distress',
                     'sneeze',
                     'thirst',
                     'aching muscles',
                     'chill',
                     'chest pain',
                     'shortness of breath',
                     'coughing',
                     'sputum',
                     'dyspnea',
                     'muscle cramps']
    randIndex = random.randint(0, 35)
    return symptoms_list[randIndex]

for i, data1 in enumerate(main_data):
    if i is not 0:
        matchFound = False
        for index, data2 in enumerate(symptoms_data):
            if index is not 0:
                if data1[columns['survival']] == data2[9]:
                    if 'NA' in data2[12] or not data2[12]:
                        main_data[i][columns['symptom1']] = fillSymptoms()
                    else:
                        main_data[i][1] = data2[12]
                    if 'NA' in data2[13] or not data2[13]:
                        main_data[i][columns['symptom2']] = fillSymptoms()
                    else:
                        main_data[i][2] = data2[13]
                    if 'NA' in data2[14] or not data2[14]:
                        main_data[i][columns['symptom3']] = fillSymptoms()
                    else:
                        main_data[i][3] = data2[14]
                    del symptoms_data[index]
                    matchFound = True
                    break
        if not matchFound:
            main_data[i][columns['symptom1']] = fillSymptoms()
            main_data[i][columns['symptom2']] = fillSymptoms()
            main_data[i][columns['symptom3']] = fillSymptoms()


'''STEP-7'''
'''Fill NA value for age column'''
# choose from the range [40-68]
def fillAge():
    return random.randint(40, 68)


'''Fill NA value for gender column'''
# choose from M/F
def fillGender():
    randIndex = random.randint(0, 1)
    genderList = ['M', 'F']
    return genderList[randIndex]


'''Fill NA value for RT_PCR column'''
# for survived: N
# for not-survived: Y
def fillRT_PCR():
    randIndex = random.randint(0, 1)
    genderList = ['Y', 'Unclear']
    return genderList[randIndex]


'''Fill NA value for went_icu column'''
# for survived: N, for not-survived: Y
def fillWent_icu():
    randIndex = random.randint(0, 1)
    genderList = ['N', 'Y']
    return genderList[randIndex]


'''Fill NA value for needed_o2 column'''
# for survived: N, for not-survived: Y
def fillNeeded_o2():
    randIndex = random.randint(0, 1)
    genderList = ['N', 'Y']
    return genderList[randIndex]


'''Fill NA value for temperature column'''
# choose from the range [37.8-38.97]
def fillTemperature():
    return round(random.uniform(37.8, 38.97), 2)


'''Fill NA value for PO2_saturation column'''
# choose from the range [55-95]
def fillPO2_saturation():
    return random.randint(55, 95)


'''Fill NA value for leukocyte column'''
# For survived patient: randomly choose from [2.85,288,3.13,3.98,3.99], For not-survived patient: randomly choose from [5.5,6.37,6.4,6.84,6.91,7]
def fillLeukocyte():
    return round(random.uniform(2.85, 7), 2)


'''Fill NA value for neutrophil column'''
# choose from the range [2.73-6.93]
def fillNeutrophil():
    return round(random.uniform(2.73, 6.93), 2)


'''Fill NA value for lymphocyte column'''
# choose from the range [0.75-1.6]
def fillLymphocyte():
    return round(random.uniform(0.75, 1.6), 2)


'''Fill NA value for location column'''
def fillCountry():
    countryList = ['Germany', 'Italy', 'Australia', 'China', 'Spain', 'United States', 'United Kingdom', 'Spain',
                   'Canada', 'Egypt', 'Hong Kong', 'South Korea', 'Iran']
    randIndex = random.randint(0, 12)
    return countryList[randIndex]

'''STEP-8'''
def processLocationColumn(location):
    temp = location.split(",")
    country = temp[len(temp) - 1]
    return country


'''STEP-9: We have only 504 images available for both CT and xray for covid-19 cases.
    But in our dataset, we have 606+random(upto 16) covid-19 cases. So, we have to delete 102+random(upto 16) cases from our dataset to make a balanced dataset with CT and xray images'''
totalCovidCaseNeededToDelete = totalCovidCaseCount()-504 # we have to delete totalCovidCaseNeededToDelete covid cases
#First, remove 10 rows whose PCR test is NULL and finding is covid-19
counter1 = 1
counter1Indexes = []
for a, data in enumerate(main_data):
    if counter1 > 10:
        break
    if a is not 0:
        if main_data[a][columns['finding']]=="COVID-19":
            if not main_data[a][columns['RT_PCR_positive']]:  # if PCR test is NULL
                counter1Indexes.append(a)
                counter1 = counter1 + 1

offset = 0  # as we delete the item from the dataset, index will be increased by 1
for i in counter1Indexes:
    del main_data[i - offset]
    offset = offset + 1

#check covid count after removing
totalCovidCaseCount()

# Remove totalCovidCaseNeededToDelete-10 rows whose PCR test is unclear and finding is covid-19 ( we have 222 Unclear cases)
counter2 = 1
counter2Indexes = []
for b, data in enumerate(main_data):
    if counter2 > (totalCovidCaseNeededToDelete-10):
        break
    if b is not 0:
        if main_data[b][columns['finding']]=="COVID-19":  # main_data[j][9] -> finding column
            if "Unclear" in main_data[b][columns['RT_PCR_positive']]:  # if PCR test is unclear
                counter2Indexes.append(b)
                counter2 = counter2 + 1

offset = 0  # as we delete the item from the dataset, index will be increased by 1
for i in counter2Indexes:
    del main_data[i - offset]
    offset = offset + 1


'''STEP-10: Add CT and Xray image names to the dataset'''
covid_count = 0
non_covid_count = 0
all_ct_covid_files = glob.glob(f"{os.getcwd()}\ct\covid\*")
all_ct_non_covid_files = glob.glob(f"{os.getcwd()}\ct\\non-covid\*")
all_xray_covid_files = glob.glob(f"{os.getcwd()}\\xray\covid\*")
all_xray_non_covid_files = glob.glob(f"{os.getcwd()}\\xray\\non-covid\*")

for j, data in enumerate(main_data):
    if j is not 0:
        # if finding column has "COVID-19" then update xray and ct column values with respective image name(from respective ct/xray folder)
        if main_data[j][columns['finding']]=="COVID-19":  # main_data[j][9] -> finding column
            try:
                ct_covid_file_path = all_ct_covid_files[covid_count].split('\\')
                ct_covid_image_name = ct_covid_file_path[len(ct_covid_file_path) - 2] + '/' + ct_covid_file_path[
                    len(ct_covid_file_path) - 1]
                main_data[j][columns['CT']] = ct_covid_image_name  # update CT image name for covid

                xray_covid_file_path = all_xray_covid_files[covid_count].split('\\')
                xray_covid_image_name = xray_covid_file_path[len(xray_covid_file_path) - 2] + '/' + \
                                        xray_covid_file_path[len(xray_covid_file_path) - 1]
                main_data[j][columns['Xray']] = xray_covid_image_name  # update xray image name for covid

                main_data[j][columns[
                    'finding']] = "COVID-19"  # modify finding column; Pneumonia/Viral/COVID-19->COVID-19 else ->NON-COVID-19
                main_data[j][columns['patientid']] = j  # update patient ID column with a incremental value(row number)
                covid_count = covid_count + 1
            except Exception as e:
                print(e, j)
        else:
            try:
                ct_non_covid_file_path = all_ct_non_covid_files[non_covid_count].split('\\')
                ct_non_covid_image_name = ct_non_covid_file_path[len(ct_non_covid_file_path) - 2] + '/' + \
                                          ct_non_covid_file_path[len(ct_non_covid_file_path) - 1]
                main_data[j][columns['CT']] = ct_non_covid_image_name  # update CT image name for non-covid

                xray_non_covid_file_path = all_xray_non_covid_files[non_covid_count].split('\\')
                xray_non_covid_image_name = xray_non_covid_file_path[len(xray_non_covid_file_path) - 2] + '/' + \
                                            xray_non_covid_file_path[len(xray_non_covid_file_path) - 1]
                main_data[j][columns['Xray']] = xray_non_covid_image_name  # update xray image name for non-covid

                main_data[j][columns[
                    'finding']] = "NON-COVID-19"  # update finding column; Pneumonia/Viral/COVID-19->COVID-19 else ->NON-COVID-19
                main_data[j][columns['patientid']] = j  # update patient ID column with a incremental value(row number)
                non_covid_count = non_covid_count + 1
            except Exception as e:
                print(e, j)

        # fill NA values for each column
        main_data[j][columns['location']] = processLocationColumn(
            main_data[j][columns['location']])  # update country column;
        if not main_data[j][columns['sex']]:
            main_data[j][columns['sex']] = fillGender()  # fill NA for gender column;
        if not main_data[j][columns['age']]:
            main_data[j][columns['age']] = fillAge()  # fill NA for age column;
        if not main_data[j][columns['RT_PCR_positive']]:
            main_data[j][columns['RT_PCR_positive']] = fillRT_PCR()  # fill NA for RT_PCR_positive column;
        if not main_data[j][columns['went_icu']]:
            main_data[j][columns['went_icu']] = fillWent_icu()  # fill NA for went_icu column;
        if not main_data[j][columns['needed_supplemental_O2']]:
            main_data[j][
                columns['needed_supplemental_O2']] = fillNeeded_o2()  # fill NA for needed_supplemental_O2 column;
        if not main_data[j][columns['temperature']]:
            main_data[j][columns['temperature']] = fillTemperature()  # fill NA for temperature column;
        if not main_data[j][columns['pO2_saturation']]:
            main_data[j][columns['pO2_saturation']] = fillPO2_saturation()  # fill NA for pO2_saturation column;
        if not main_data[j][columns['leukocyte_count']]:
            main_data[j][columns['leukocyte_count']] = fillLeukocyte()  # fill NA for leukocyte_count column;
        if not main_data[j][columns['neutrophil_count']]:
            main_data[j][columns['neutrophil_count']] = fillNeutrophil()  # fill NA for neutrophil_count column;
        if not main_data[j][columns['lymphocyte_count']]:
            main_data[j][columns['lymphocyte_count']] = fillLymphocyte()  # fill NA for lymphocyte_count column;
        if not main_data[j][columns['location']]:
            main_data[j][columns['location']] = fillCountry()  # fill NA for country column;



'''Delete unnecessary columns from the dataset'''
def deleteUnnecessaryColumn(columnList):
    for rIndex, rData in enumerate(main_data):
        offSet = 0
        for eachColumn in columnList:
            try:
                # print(len(rData))
                del main_data[rIndex][eachColumn - offSet]
                offSet = offSet + 1
            except Exception as e:
                print(e, rIndex, eachColumn)


'''
unNecessaryColumns = [columns['offset'], columns['intubated'], columns['intubation_present'], columns['in_icu'],
                      columns['extubated'], columns['view'], columns['modality'], columns['date'], columns['folder'],
                      columns['filename'], columns['doi'], columns['url'], columns['license_d'], columns['other_notes']]
deleteUnnecessaryColumn(unNecessaryColumns)
'''



'''STEP-11: Reorder the dataset columns to have a nice structured dataset'''
newColumnOrder = [columns['patientid'], columns['sex'], columns['age'], columns['location'],
                  columns['symptom1'], columns['symptom2'], columns['symptom3'],
                  columns['temperature'], columns['RT_PCR_positive'], columns['went_icu'],
                  columns['pO2_saturation'], columns['needed_supplemental_O2'],
                  columns['leukocyte_count'], columns['neutrophil_count'], columns['lymphocyte_count'],
                  columns['clinical_notes'], columns['CT'], columns['Xray'], columns['finding'], columns['survival']]
new_ordered_data = []
for index, data in enumerate(main_data):
    new_ordered_data.append([data[i] for i in newColumnOrder])



'''STEP-12: Make a new file with all processed data'''
with open('test.csv', 'w', newline='') as new_file:
    csv_writer = csv.writer(new_file)
    for line in new_ordered_data:
        csv_writer.writerow(line)
