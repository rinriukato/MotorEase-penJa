import os
import xml.etree.ElementTree as ET
import xml.dom.minidom
import cv2
#import InconSizeDetector
#from ExpandingMenu import *
from src.touchTarget.objectExtractor import *
from src.persistingElement.persistentElements import *
from src.ExpandingElements.ExpandingMenu import *
import glob

eachApp  = ".../MIRACLE/Data/RealData"

for subdir, dirs, files in os.walk(eachApp):
    for indApp in dirs:
        print('NEW APP')
        for subdir1, dirs1, files1 in os.walk(eachApp + "/" + indApp):
            extractObjects(subdir1)
            for file in files1:
                if ".png" in file: 
                    getExpandingScreens(file)
                    continue

# persisting element detector
PersistentDriver(eachApp)

# create accessibility report

writing = open(".../MIRACLE/results/ACCESSIBILITY-REPORT.txt", 'a')

expanding = open(".../MIRACLE/results/patternMatchingResultsFinal.txt")
persisting = open(".../MIRACLE/results/PeristentEvaluationResults.txt")
touch = open(".../MIRACLE/results/resultsTouch1.csv")

writing.write("Expanding Sections ---------------------------------\n")
for i in expanding:
    if "match_status" in i:
        splt = i.split("\'match_status\': ")
        if "\'yes\'" in splt[1]: 
            writing.write(str(i.split("\'filename\': \'")[1].split(',')[0].strip('\'')) + ": " + "Closable\n")
            #print("Matched")
            #print(i.split("\'filename\': \'")[1].split(',')[0].strip('\''))
        else:
            writing.write(i.split("\'filename\': \'")[1].split(',')[0].strip('\'') + ": " + "Not Closable\n")
    

writing.write("\n\n")
writing.write("Persisting Elements ---------------------------------\n")
for i in persisting:
    if i.split('--')[1] == '0\n':
        writing.write(str(i.split('--')[0]) + ': ' + "No Violations\n")
    else:
        writing.write(str(i.split('--')[0]) + ': ' + "Violations Present\n")


writing.write("\n\n")
writing.write("Touch Targets ---------------------------------\n")
for i in touch:
    #print(i.split(',')[0])
    if len(i.split(',')[1]) == 3:
        writing.write(str(i.split(',')[0]) + ': ' + "No Violations\n")
    else:
        writing.write(str(i.split(',')[0]) + ': ' + "Violations Present\n")

expanding.close()
persisting.close()
touch.close()
writing.close()









