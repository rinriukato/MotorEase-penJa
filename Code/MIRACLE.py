import os
#from application.app.folder.file import func_name
from detectors.Visual.TouchTarget import checkTouchTarget
from detectors.Motor.Closure import *
from detectors.Motor.Closure import detectClosure
from detectors.Motor.patternMatching.pattern_matching import *
from detectors.Motor.persistentElements import *
from detectors.Motor.persistentElements import PersistentDriver

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
	txt = open("AccessibilityReport.txt", "w")
	file_extensions = ['.png', '.xml']
	files = []
	print(">> Getting Files and Screenshots\n")
	for root, dirs, files_in_dir in os.walk(data_folder):
		for file_name in files_in_dir:
			files.append(os.path.join(root, file_name[:-4]))
	print(">> Initializing Detectors\n")
	
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
			#print(touchText)  
			txt.write(touchText + '\n')  

			print("===== Running Expanding Elements =====")
			expanding = detectClosure(image, xml)
			expandingText = "Expanding Sections Detector>> " +"Expanding elements: " + str(expanding) + "\n"
			#print(expandingText)
			txt.write(expandingText + '\n')
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
	persistentText = "Persisting Elements Detector>> " + "Violating Screens: " + str(persistent[1])
	#print(persistentText)

	print("\n>> Generating Accessibility Report")

	txt.write(persistentText + '\n')
	print("\nAccessibility Report Generated: AccessibilityReport.txt")

	txt.close()

# set the path to the directory of the Miracle Project
# this path should lead to the directory that has "code" and "data" in it
MIRACLE_PATH = "/Users/JONDOE/Documents/MiracleProject/"
os.chdir(MIRACLE_PATH)

# the data folder should have the images and screenshots from a single application
AppPath = MIRACLE_PATH + '/Data'
RunDetectors(AppPath) 




















