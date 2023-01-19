
import json
import shutil, os
with open(".../labeledData.json", 'r') as f:
    data = json.load(f)

dataLoc = ".../combined"

counter = 0
for i in data:
    filename = i['file_upload']
    label = i['annotations'][0]['result'][0]['value']['rectanglelabels'][0]

    if counter >= 391:
        splt = filename.split("_")[0:5]
        filename = '_'.join(splt) + '.png'

    file = dataLoc + "/" + filename
    if label == 'text':
        shutil.copy(file, '.../text')
    elif label == 'cant close':
        shutil.copy(file, '.../cantDetect')
    else:
        shutil.copy(file, '.../withIcons')
    counter += 1

    print(counter)
