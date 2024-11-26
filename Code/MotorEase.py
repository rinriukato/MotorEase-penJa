print(">> Starting MotorEase\n")
import json
import os
#from application.app.folder.file import func_name
from detectors.Visual.TouchTarget import checkTouchTarget
from detectors.Visual.IconDistance import getDistance
#from detectors.Visual.LabeledElements import checkLabeled
from detectors.Motor.Closure import *
from detectors.Motor.Closure import detectClosure
from detectors.Motor.patternMatching.pattern_matching import *
from detectors.Motor.persistentElements import *
from detectors.Motor.persistentElements import PersistentDriver
import pickle
from numpy import asarray

import importlib  
pre = importlib.import_module("detectors.Visual.UIED-master.detect_compo.lib_ip.ip_preprocessing")
draw = importlib.import_module("detectors.Visual.UIED-master.detect_compo.lib_ip.ip_draw")
det = importlib.import_module("detectors.Visual.UIED-master.detect_compo.lib_ip.ip_detection")
file = importlib.import_module("detectors.Visual.UIED-master.detect_compo.lib_ip.file_utils")
Compo = importlib.import_module("detectors.Visual.UIED-master.detect_compo.lib_ip.Component")
ip = importlib.import_module("detectors.Visual.UIED-master.detect_compo.ip_region_proposal")
Congfig = importlib.import_module("detectors.Visual.UIED-master.config.CONFIG_UIED")

def RunDetectors(data_folder):
	print(">> Extracting Path\n")
	txt = open("AccessibilityReportTEXT.txt", "a")
	txt = open("predictions2.txt", "a")
	file_extensions = ['.png', '.xml']
	files = []
	print(">> Getting Files and Screenshots\n")
	for root, dirs, files_in_dir in os.walk(data_folder):
		for file_name in files_in_dir:
			files.append(os.path.join(root, file_name[:-4]))
	print(">> Initializing Detectors\n")

	print(">> Initializing Embedding Model (may take some time)\n")
	# Load pre-trained GloVe embeddings
	# glove_model_array = ""
	# with open('./code/glove_model.pkl', 'rb') as f:
	# 	try:
	# 		glove_model_array = pickle.load(f)
	# 	except EOFError as e: 
	# 		print(f"EOFError: {e}")

	# All glove file paths
	GLOVE_MODELS = {
    	"6B": {
			"50d": "glove.6B.50d.txt",
			"100d": "glove.6B.100d.txt",
			"200d": "glove.6B.200d.txt",
			"300d": "glove.6B.300d.txt",
		},
		"42B": {
			"300d": "glove.42B.300d.txt",
		},
		"840B": {
			"300d": "glove.840B.300d.txt",
		}
	}

	DEFAULT_MODEL = {
		"tokens": "6B",
		"vectors": "50d"
	}

	# Get preferred model
	if os.path.exists('./save.json'):
		with open('./save.json', 'r') as f:
			save = json.load(f)
	
		if 'glove_model' in save:
			glove_model = save['glove_model']
		else:
			glove_model = DEFAULT_MODEL

	else:
		glove_model = DEFAULT_MODEL

	# Load GloVe model
	glove_model = "./Code/" + GLOVE_MODELS[glove_model['tokens']][glove_model['vectors']]
	model = {}
	with open(glove_model, 'r', encoding='utf-8') as file:
		for line in file:
			parts = line.split()
			word = parts[0]
			vector = [float(x) for x in parts[1:]]  # Convert string components to floats
			model[word] = vector
	
	glove_model_array = model

	counter = 0
	for i in range(0, len(files), 2):

		if "DS_S" not in files[i]:
			image = files[i] + ".png"
			xml = files[i] + ".xml"  
			txt.write("============================================\n")
			txt.write('FILENAME: ' + image.split('/')[-1] + "\n")

			print("_______Analyzing Next File______")

			print("===== Running Touch Target =====")
			touchTarget = checkTouchTarget(image, xml) #Format-> [25 (violations), 26 (elements), './Data/ca.mimic.apphangar_Bottom_Up_0.xml']
			touchText = "Touch Target Detector>> "  + "Interactive Elements: " + str(touchTarget[1]) + " | Violating Elements: " + str(touchTarget[0]) + "\n"
			print(touchText)  
			txt.write(touchText + '\n')  

			print("===== Running Expanding Elements =====")
			expanding = detectClosure(image, xml, glove_model_array)
			expandingText = image + ":\n" + "Expanding Sections Detector>> " +"Expanding elements: " + str(expanding) + "\n"
			print(expandingText)
			txt.write(expandingText + '\n')
			print("\n")

			print("===== Running Icon Distances =====")
			distances = getDistance(image, xml)
			print(distances)
			txt.write(str(image.split('/')[-1]) + ', ' + str(distances) + "\n")
			print("\n")

			#for testing
			if counter > 1:
				continue
			counter += 1

	txt.write("============================================\n")
	txt.write("\nAll Screens \n")
	print("_______Analyzing All Screens_______")
	print("===== Running Persistent Elements =====")
	persistent = PersistentDriver(data_folder)
	persistentText = data_folder + ': \n' "Persisting Elements Detector>> " + "Violating Screens: " + str(persistent[1])
	print(persistentText)

	print("\n>> Generating Accessibility Report")

	txt.write(persistentText + '\n')
	print("\nAccessibility Report Generated: AccessibilityReport.txt")

	txt.close()

# set the path to the directory of the Miracle Project
MotorEase_PATH = "./"
os.chdir(MotorEase_PATH)


AppPath = MotorEase_PATH + 'Data'
RunDetectors(AppPath) 




















