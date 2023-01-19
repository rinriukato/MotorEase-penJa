import json
import shutil, os
with open('.../data/result.json', 'r') as f:
  data = json.load(f)


for i in data['images']:
	print("Transferred:", i['file_name'])
	shutil.copy(i['file_name'], '.../data/modData')









































