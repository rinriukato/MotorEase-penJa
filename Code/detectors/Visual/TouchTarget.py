import xml.etree.ElementTree as ET
from PIL import Image
import cv2
import os
import importlib  
foobar = importlib.import_module("detectors.Visual.UIED-master.run_single")
import json

def __init__(self):
	pass

def getBounds(inText):

    split = inText.split('][')
    
    split[0] = split[0].strip('[')
    split[1] = split[1].strip(']')
    
    split[0] = split[0].split(",")
    split[1] = split[1].split(",")
    
    split[0] = [int(split[0][0]), int(split[0][1])]
    split[1] = [int(split[1][0]), int(split[1][1])]
    return split

def checkTouchTarget(screenshot_path, xml_path, min_size=(48, 48)):
# Load the XML file
	"""

	screenshot_path - path to screenshot in directory
	xml_path - path to xml file in directory
	min_size - minimum size of the picture bounds?

	This function tests if interactive elements, in an app are big enough to be useable (dictated by min_size)
	of 48x48 pixels. 

	"""

	if ".DS_S" not in xml_path:
		tree = ET.parse(xml_path)
		root = tree.getroot()
		bounding_boxes = []
		singleScreenViolations = []

		violations = 0
		nonViolations = 0

		for elem in root.iter():
			elements = elem.items()
			if len(elements) > 1:
				if elements[8][0] == 'clickable' and elements[8][1] =='true' and elements[16][1] != '[0,0][0,0]':
					# Find all bounding boxes in the XML file
					bounds = getBounds(elements[16][1])
					first = bounds[1][0] - bounds[0][0]
					second = bounds[1][1] - bounds[0][1]

					# The element at this coordinate is too small!
					if first <48 or second <48:
						#print(elements)
						#print(bounds)
						violations+=1

					else:
						
						im = Image.open(screenshot_path)
						
						im1 = im.crop((bounds[0][0]-15, bounds[0][1]-15, bounds[1][0]+15, bounds[1][1]+15))
						
						savePath = "./Code/detectors/Visual/UIED-master/data/input/" + str(screenshot_path.split('/')[-1])
						im1 = im1.save(savePath)
						foobar.runSingle(savePath)
						os.remove(savePath)
						for root, dirs, files_in_dir in os.walk("./Code/detectors/Visual/UIED-master/data/output/ip/"):
							for file_name in files_in_dir:
								if ".json" in file_name:
									data = []
									#print(file_name)
									with open("./Code/detectors/Visual/UIED-master/data/output/ip/" + file_name, "r") as file:
										data = json.load(file)
									for i in range(len(data["compos"])):
										height = data["compos"][i]['height']
										width = data["compos"][i]['width']
										if height < 48 or width < 48:
											violations += 1
										else:
											nonViolations += 1

										#print(violations)
										#print(nonViolations)

									if "DS_Store" not in file_name:
										os.remove("./Code/detectors/Visual/UIED-master/data/output/ip/" + file_name)
								else:
									os.remove("./Code/detectors/Visual/UIED-master/data/output/ip/" +file_name)
		return([violations, violations+nonViolations, xml_path])
										

						#return([bounds, screenshot_path, elements])

		













