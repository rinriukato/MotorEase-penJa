import os
import xml.etree.ElementTree as ET
from os import walk
import shutil
from src.touchTarget.uiedRun import *
import glob

def getBounds(inText):
    split = inText.split('][')
    
    split[0] = split[0].strip('[')
    split[1] = split[1].strip(']')
    
    split[0] = split[0].split(",")
    split[1] = split[1].split(",")
    
    split[0] = [int(split[0][0]), int(split[0][1])]
    split[1] = [int(split[1][0]), int(split[1][1])]
    return split

def extractObjects(path):
	directory = path
	# iterate over files in
	# that directory
	
	#increased the size of the guidelines by 15
	height = 63
	width = 63
	allViolations = {}
	counter = 0
	for filename in os.listdir(directory):
		counter += 1
		f = os.path.join(directory, filename)
	    # checking if it is a file
		if os.path.isfile(f) and ".xml" in f:
			tree = ET.parse(f)
			root = tree.getroot()
			singleScreenViolations = []
			for elem in root.iter():
				elements = elem.items()
				if len(elements) > 1:
					if elements[8][0] == 'clickable' and elements[8][1] =='true' and elements[16][1] != '[0,0][0,0]':
						try:
							bounds = getBounds(elements[16][1])
							first = bounds[1][0] - bounds[0][0]
							second = bounds[1][1] - bounds[0][1]
							#if elements[3][1] == 'android.widget.Button':
							info = [elements[2][1], elements[3][1], [first, second], bounds]
							singleScreenViolations.append(info)
						except: 
							continue
			if len(singleScreenViolations) > 0:
				allViolations[f] = singleScreenViolations
		
	#print(len(allViolations))
	import cv2
	from PIL import Image
	# 00, 01, 10, 11
	counter = 0
	for i in allViolations: 
		dirPath = path
		filename = i.split('/')
		filename = filename[-1][:-4]+".png"
		filePath = dirPath + "/" +filename
		#print(filePath)
		try:
			file = open(filePath)
			#print(filePath)
			if len(allViolations[i]) > 0:
				for violations in allViolations[i]:
					bounds = violations[3]
					im = Image.open(filePath)
					if (bounds[0][0]-15 >= 0 and  bounds[0][1]-15 > 0) and (bounds[1][0]+15 <= 1920 and bounds[1][1]+15 <= 1920):
						im1 = im.crop((bounds[0][0]-15, bounds[0][1]-15, bounds[1][0]+15, bounds[1][1]+15))
						modFile = str(filename) +"---"+ str(violations[0]) +"_"+ str(violations[1]) +"_"+ str(violations[2]) 
						savePath = ".../MIRACLE/Data/touchScreens/cropped" + modFile +  '.png'
						im1 = im1.save(savePath)
					#print(bounds)

			if counter % 50 == 0:
				print(counter)
			counter += 1
		except:
			allViolations[i] = 'INVALID'

	# runUIED
	
	uied()

	# NOW FILTERING
	#print("after")
	screenFiles = next(walk('.../MIRACLE/Data/touchScreens/Output'), (None, None, []))[2]  # [] if no file

	croppedFiles = next(walk('.../MIRACLE/Data/touchScreens/cropped'), (None, None, []))[2]  # [] if no file

	print(len(screenFiles))
	print(len(croppedFiles))

	newScreens = []

	count = 0
	for i in croppedFiles:
		name = i[:-4] + ".jpg"
		if name in screenFiles and name not in newScreens: 
			newScreens.append(name)

	filteredOut = '.../MIRACLE/Data/touchScreens/filteredOut'

	
	#print(len(newScreens))

	src_dir = ".../MIRACLE/Data/touchScreens/Output"
	dst_dir = filteredOut
	for jpgfile in newScreens:
		try:
			toMove = src_dir + jpgfile[0:-4] + ".json"
			shutil.copy(toMove, dst_dir)
		except:
			print('nope')


	# Now analyze the UIED
	import json


	def hasViolation(file):
		jsonPath = open(file)
		fileLoc = json.load(jsonPath)
		h = 48
		w = 48
		counter = 0
		for i in fileLoc['compos']:
			height = i['height']
			width = i['width']
			if height < h or width < w:
				return (counter, True)
			counter += 1
		return (counter, False)

	initialScreens = glob.glob(".../MIRACLE/code/src/touchTarget/cropped/*")
	resultScreens = glob.glob(".../MIRACLE/code/src/touchTarget/UIEDoutput/ip/*.json")

	print(initialScreens)
	print(len(resultScreens))

	screenDict = {}
	for i in resultScreens:
		key = i.split('/')[-1].split('---')[0][:-4] + ".png"
		screenDict[key] = []

	for i in resultScreens:
		key = i.split('/')[-1].split('---')[0][:-4] + ".png"
		existing = screenDict[key]
		existing = []
		if hasViolation(i)[1]:
			existing.append("VIOLATION DETECTED")
			print("VIOLATION")
		else:
			continue
		#print(existing)
		#print(key)
	#print(screenDict)
	import csv

	with open('.../MIRACLE/results/resultsTouch1.csv', 'w') as f:
	    for key in screenDict.keys():
	        f.write("%s,%s\n"%(key,screenDict[key]))














