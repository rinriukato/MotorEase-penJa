import xml.etree.ElementTree as ET
from PIL import Image
import cv2
import os
import importlib  
foobar = importlib.import_module("detectors.Visual.UIED-master.run_single")
import json
import numpy as np
from sklearn.cluster import KMeans
import pytesseract
def __init__(self):
	pass

def bbox_dimensions(bbox):
    # Assuming bbox is a tuple or list with 4 elements: (x1, y1, x2, y2)
    x1, y1, x2, y2 = bbox

    # Calculate the width and height of the bounding box
    width = x2 - x1
    height = y2 - y1

    # Return the width and height as a tuple
    return (width, height)

def BoundDistance(bbox_i, bbox_j):
	horiz_dist = max(0, abs(min(bbox_i[2], bbox_j[2]) - max(bbox_i[0], bbox_j[0])))
	vert_dist = max(0, abs(min(bbox_i[3], bbox_j[3]) - max(bbox_i[1], bbox_j[1])))

	result_list = [bbox_i[i] - bbox_j[i] for i in range(len(bbox_i))]
	for i in result_list:
		if abs(i) <=8:
			return ([horiz_dist, vert_dist, i])
	return ([horiz_dist, vert_dist, 10])

def check_no_matching_numbers(arr1, arr2):
	for num1 in arr1:
		for num2 in arr2:
			if num1 == num2:
				return False	
	return True
def is_overlapping(box1, box2):
	x1_min, y1_min, x1_max, y1_max = box1
	x2_min, y2_min, x2_max, y2_max = box2

	if (x1_max < x2_min) or (x2_max < x1_min) or (y1_max < y2_min) or (y2_max < y1_min):
		return False
	else:
		return True
def getBounds(inText):
	split = inText.split('][')
	
	split[0] = split[0].strip('[')
	split[1] = split[1].strip(']')
	
	split[0] = split[0].split(",")
	split[1] = split[1].split(",")
	
	split[0] = [int(split[0][0]), int(split[0][1])]
	split[1] = [int(split[1][0]), int(split[1][1])]
	return split
						
def is_single_color_image(image_path):
	"""
	Checks if an image is just a single solid color.
	"""
	# Open the image using Pillow
	img = Image.open(image_path)

	# Get the image dimensions
	width, height = img.size

	# Get the color of the top-left pixel
	pixel = img.getpixel((0, 0))

	# Check if all pixels in the image have the same color
	for x in range(width):
		for y in range(height):
			if img.getpixel((x, y)) != pixel:
				return False
	img.close()
	# If all pixels have the same color, return True
	return True


def getDistance(screenshot_path, xml_path):
# Load the XML file
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
					box_string = elements[16][1]
					
					try:
						# Extract the four values from the bounding box string
						left = int(box_string[1:box_string.index(",")])
						top = int(box_string[box_string.index(",")+1:box_string.index("]")])
						right = int(box_string[box_string.index("[", 1)+1:box_string.index(",", box_string.index(",")+1)])
						bottom = int(box_string.split(str(right))[1].strip(',').strip(']'))
						# Create a list of the four values
						bbox = [left, bottom, right, top]
							
						im = Image.open(screenshot_path)
						if bounds[0][0] > bounds[1][0]:
							temp = bounds[0][0]
							bounds[0][0] = bounds[1][0]
							bounds[1][0] = temp
						if bounds[0][1] > bounds[1][1]:
							temp = bounds[0][1]
							bounds[0][1] = bounds[1][1]
							bounds[1][1] = temp
						#print(bounds)
						im1 = im.crop((bounds[0][0]-15, bounds[0][1]-15, bounds[1][0]+15, bounds[1][1]+15))
						
						savePath = "./Code/detectors/Visual/UIED-master/data/input/" + str(screenshot_path.split('/')[-1])
						im1.save(savePath)
						im1.close()
						# print(is_single_color_image(savePath))
						extractedText = pytesseract.image_to_string(savePath)
						if len(extractedText) > 10 and is_single_color_image(savePath) == False:
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
											ogBoxWidth, ogBoxHeight = bbox_dimensions(bbox)

											#subHeight = int(height/2)
											#subWidth = int(width/2)

											subHeight = int((ogBoxHeight-height)/2)
											subWidth = int((ogBoxWidth-width)/2)

											newBox = [bbox[0]+subWidth, bbox[3] + subHeight, bbox[2] - subWidth, bbox[1] - subHeight]
											if height > 55 and width > 55:
												bounding_boxes.append(newBox)
												break
						im.close()
					except: 
						print('ERROR')
						continue
					

		uniqueDistances = {}
		for i in range(0, len(bounding_boxes)):
			for j in range(i+1, len(bounding_boxes)):
				if bounding_boxes[i] != bounding_boxes[j] and check_no_matching_numbers(bounding_boxes[i], bounding_boxes[j]) and (is_overlapping(bounding_boxes[i], bounding_boxes[j]) == False) :
					distances = BoundDistance(bounding_boxes[i],bounding_boxes[j])
					distT = tuple(distances)
					distT
					#if (distances[0] < 8 or distances[1] < 8) and (distances[0] != 0 and distances[1] != 0) and (abs(distances[0] - distances[1]) < 50) :
					if distT[2] < 10 :	
						if distT not in uniqueDistances.keys():
							uniqueDistances[distT] = [[bounding_boxes[i],bounding_boxes[j]]]

							break
						else:
							del uniqueDistances[distT]
							# mod = uniqueDistances[distT]
							# mod.append([bounding_boxes[i],bounding_boxes[j]])
							# uniqueDistances[distT] = mod 
		
		if len(uniqueDistances.keys()) > 0 and len(uniqueDistances.keys()) < 50:
			print(screenshot_path)
			return(1)
		else:
			return(0)


		













