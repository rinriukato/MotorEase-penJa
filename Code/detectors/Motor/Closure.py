
import xml.etree.ElementTree as ET
import xml.dom.minidom
import cv2
from PIL import Image
import os
import pytesseract
import importlib
from detectors.Motor.patternMatching.pattern_matching.matching import match_patterns
from detectors.Motor.objectDetect import objectDetect
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from gensim.models import KeyedVectors
def find_largest_number(numbers):
	largest_number = numbers[0] # assume first element is the largest
	for number in numbers:
		if number > largest_number:
			largest_number = number
	return largest_number

def load_glove_model(File):
	glove_model = {}
	with open(File, 'r') as f:
		for line in f:
			line = line.replace('.', '')
			split_line = line.split()
			#word = split_line[0]
			word = ''.join(split_line[:-300])
			#embedding = np.array(split_line[1:], dtype=np.float64)
			coefs = np.asarray(split_line[-300:], dtype='float32')
			glove_model[word] = coefs
	print(f"{len(glove_model)} words loaded!")
	return glove_model

def closureEmbedding(external_word, glove_vectors):

	# Define the list of closure-related words
	closure_words = ["close", "cancel", "dismiss", "done", "ok", "finish", "return"]
	additional_words = ["deny", "allow", "exit","end","terminate","quit","back","stop","ignore", "proceed","save","apply","submit","confirm","abort","decline","reject","ignore"]					
	# Define the input word to compare
	input_word = external_word

	# Calculate the cosine similarity between the input word and the closure-related words
	word_embeddings = [glove_vectors[word] for word in additional_words]
	if input_word in glove_vectors:
		input_word_embedding = glove_vectors[input_word]
		similarity_scores = cosine_similarity([input_word_embedding], word_embeddings)
		score = find_largest_number(similarity_scores[0])
		if score > 0.85:
			return("matched")


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

def detectClosure(imgPath, xmlPath, glove_vectors):
	# remove for testing
	frames = 1
	lists = 1
	if 1 == 0:
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

	# delete line below after testing
	saveFile = imgPath
	textClose = 0
	if frames != 0 or lists != 0:
		# extracting text
		extractedText = pytesseract.image_to_string(saveFile) # extractedText = Settings	Close
		
		for i in extractedText.split("\n"):
			# pattern matching on text
			#resultText = match_patterns(i)
			for j in i.split(' '):
				if len(j) > 1:
					resultText = closureEmbedding(j.lower(), glove_vectors)
					if resultText == "matched":
						textClose += 1
						os.remove(saveFile)
						return([imgPath, "closable", "text"])


		# image detection if no text is found that indicates closure
		useImage = True
		if textClose == 0 and useImage == True:
			#print(saveFile)
			result = objectDetect(saveFile)
			
			if result != None: 
				return([imgPath, "closable", result])
				
			else:
				return([imgPath, "NotClosable"])
	#im.close()
	return("NoExpandingDetected")


	

			

		











