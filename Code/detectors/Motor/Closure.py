import xml.etree.ElementTree as ET
import xml.dom.minidom
import cv2
from PIL import Image
import os
import pytesseract
import importlib
from detectors.Motor.patternMatching.pattern_matching.matching import match_patterns
from detectors.Motor.objectDetect import objectDetect

def LargestElement(path):
	largestLayoutArea = 0
	largestLayout = None
	largestListArea = 0
	largestList = None
	tree = ET.parse(path)
	for elem in tree.iter():
		obj = elem.items()
		if len(obj) > 2:
			#print(obj[3])
			if obj[3][1] == 'android.widget.FrameLayout':
				bounds = obj[len(obj)-1][1]
				bounds = getBounds(bounds)
				width = bounds[1][0] - bounds[0][0]
				height = bounds[1][1] - bounds[0][1]
				size = width * height
				
				if size > largestLayoutArea and width != 1200 and height != 1824:
					largestLayoutArea = size
					largestLayout = (obj, bounds, [width, height])
					
			if obj[3][1] == "android.widget.ListView":
				bounds = obj[len(obj)-1][1]
				bounds = getBounds(bounds)
				width = bounds[1][0] - bounds[0][0]
				height = bounds[1][1] - bounds[0][1]
				size = width * height
				if size > largestListArea and width != 1200 and height != 1824:
					largestListArea = size
					largestList = (obj, bounds, [width, height])
	return([largestLayout, largestList])

def getBounds(inText):
	split = inText.split('][')
	
	split[0] = split[0].strip('[')
	split[1] = split[1].strip(']')
	
	split[0] = split[0].split(",")
	split[1] = split[1].split(",")
	
	split[0] = [int(split[0][0]), int(split[0][1])]
	split[1] = [int(split[1][0]), int(split[1][1])]
	return split

def detectClosure(imgPath, xmlPath):
	ctr = 0
	frames = 0
	lists = 0
	largests = LargestElement(xmlPath)
	im = Image.open(imgPath)
	imW,imH = im.size
	saveFile = "./Code/detectors/Motor/Temp/" + imgPath.split('/')[-1]
	if largests[0] != None and largests[1] == None:
		if largests[0][1][1] != [1080, 1794]:
			im1 = im.crop((largests[0][1][0][0], largests[0][1][0][1], largests[0][1][1][0], largests[0][1][1][1]))
			#im1.show()
			im1.save(saveFile) 
			frames += 1
			#print("Frame1")
			#print("written 1")
	#1080 × 1920
	elif largests[1] != None and largests[0] == None:
		if largests[1][1][1] != [1080, 1794]:
			im1 = im.crop((largests[1][1][0][0], largests[1][1][0][1], largests[1][1][1][0], largests[1][1][1][1]))
			im1.save(saveFile) 
			lists += 1
			#print("List1")
			#im1.show()
			#print("written 2")
		
	elif largests[1] != None and largests[0] != None:

		listSize = largests[1][2][0] * largests[1][2][1]
		layoutSize = largests[0][2][0] * largests[0][2][1]
		if (listSize/(imW*imH) > 0.1 and listSize/(imW*imH) < 0.60) or largests[1][1][0][0] == 0:
			if largests[1][1][1] != [1080, 1794]:
				im1 = im.crop((largests[1][1][0][0], largests[1][1][0][1], largests[1][1][1][0], largests[1][1][1][1]))
				im1.save(saveFile)  

				lists += 1
				#print("List2")
		   # im1.show()
			#print("written 3")
		else:
			if largests[0][1][1] != [1080, 1794]:
				im1 = im.crop((largests[0][1][0][0], largests[0][1][0][1], largests[0][1][1][0], largests[0][1][1][1]))
				im1.save(saveFile) 
				frames += 1
	
	# Found Expanding Section
	textClose = 0
	if frames != 0 or lists != 0:
		# extracting text
		extractedText = pytesseract.image_to_string(saveFile) # extractedText = Settings	Close
		
		for i in extractedText.split("\n"):
			# pattern matching on text
			resultText = match_patterns(i)
			if resultText == "matched":
				textClose += 1
				os.remove(saveFile)
				return([imgPath, "closable", "text"])


		# image detection if no text is found that indicates closure
		useImage = False
		if textClose == 0 and useImage == True:
			#print(saveFile)
			result = objectDetect(saveFile)
			if len(result) > 1:
				return([imgPath, "closable", result[1]])

	return("NoExpandingDetected")


	

			

		











