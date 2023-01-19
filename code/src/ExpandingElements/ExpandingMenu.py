#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 17:58:57 2022

"""
# imports
import xml.etree.ElementTree as ET
import xml.dom.minidom
import cv2
from PIL import Image
#from UIED-master.run_single import *
import os
#import src.ExpandingElements.accessibility_pattern_matching_related.pattern_matching as pattern_matching
from src.ExpandingElements.accessibility_pattern_matching_related.pattern_matching.matching import *
from src.ExpandingElements.ImageDetection.object_detection_frcnn_mscoco_inference import *
from src.ExpandingElements.analyzeExpand import *
import glob
# returns tuple, ("pop"/"side", path) 
def detectExpansion(path):
    
    # parse through the xml
    tree = ET.parse(path)
    for elem in tree.iter():
        print(elem.items())
    # then find if a list view is 1/3-1/5 the size of the screen
    # if not, find the largest framelayout on the screen 
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

def getFileID(path):
    extract = path[len(path)-5:]
    ID = extract[0]
    return ID

def LargestListFrame(path):
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

frameStorage = ".../MIRACLE/code/src/ExpandingElements/Frames/"
listStorage = ".../MIRACLE/code/src/ExpandingElements/Lists/"

def getExpandingScreens(pathPng):
    rootdir = pathPng
    ctr = 0
    frames = 0
    lists = 0
    found = 0
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            filename = os.fsdecode(file) 
            fileID = filename[0:len(filename)-4]
            # Getting all XMLS
            try:
                xmlpath = pathXml + fileID + ".xml"
                largests = LargestListFrame(xmlpath)
                imgPath = pathPng + str(fileID) + ".png"
                im = Image.open(imgPath)
                found += 1
            except: 
                continue
            imW,imH = im.size
            
            if largests[0] != None and largests[1] == None:
                if largests[0][1][1] != [1080, 1794]:
                    im1 = im.crop((largests[0][1][0][0], largests[0][1][0][1], largests[0][1][1][0], largests[0][1][1][1]))
                    #im1.show()
                    im1.save(frameStorage + str(frames) + "_" + fileID + ".png") 
                    frames += 1
                    #print("written 1")
            #1080 × 1920
            elif largests[1] != None and largests[0] == None:
                if largests[1][1][1] != [1080, 1794]:
                    im1 = im.crop((largests[1][1][0][0], largests[1][1][0][1], largests[1][1][1][0], largests[1][1][1][1]))
                    im1.save(listStorage + str(lists) + "_" + fileID + ".png") 
                    lists += 1
                    #im1.show()
                    #print("written 2")
                
            elif largests[1] != None and largests[0] != None:
        
                listSize = largests[1][2][0] * largests[1][2][1]
                layoutSize = largests[0][2][0] * largests[0][2][1]
                if (listSize/(imW*imH) > 0.1 and listSize/(imW*imH) < 0.60) or largests[1][1][0][0] == 0:
                    if largests[1][1][1] != [1080, 1794]:
                        im1 = im.crop((largests[1][1][0][0], largests[1][1][0][1], largests[1][1][1][0], largests[1][1][1][1]))
                        im1.save(listStorage + str(lists) + "_" + fileID + ".png") 
                        lists += 1
                   # im1.show()
                    #print("written 3")
                else:
                    if largests[0][1][1] != [1080, 1794]:
                        im1 = im.crop((largests[0][1][0][0], largests[0][1][0][1], largests[0][1][1][0], largests[0][1][1][1]))
                        im1.save(frameStorage + str(frames) + "_" + fileID + ".png") 
                        frames += 1
                        #im1.show()
                        #print("written 4")
                
            if ctr % 100 == 0:
                print(ctr)
            ctr += 1
    
    source = '.../MIRACLE/code/src/ExpandingElements/Frames/'
    destination = '.../MIRACLE/code/src/ExpandingElements/combined'
     
    # gather all files
    allfiles = os.listdir(source)
    for f in allfiles:
        src_path = os.path.join(source, f)
        dst_path = os.path.join(destination, f)
        os.rename(src_path, dst_path)

    # source = '.../MIRACLE/code/src/ExpandingElements/Frames/'
    # destination = '.../MIRACLE/code/src/ExpandingElements/Frames/'
     
    # # gather all files
    # allfiles = os.listdir(source)
    # for f in allfiles:
    #     src_path = os.path.join(source, f)
    #     dst_path = os.path.join(destination, f)
    #     os.rename(src_path, dst_path)
    # #print(found)

    # runORC()

    #get OCR files
    ocr_files = [file for file in glob.glob(".../MIRACLE/code/src/ExpandingElements/OCRtxt/" + "*.json")] # provide location of the OCR files
    ocr_files.sort()
    # print(ocr_files)
    os.remove(".../MIRACLE/code/src/ExpandingElements/patternMatchingResults.txt")
    writing = open(".../MIRACLE/code/src/ExpandingElements/patternMatchingResults.txt", 'a')
    writing1 = open(".../MIRACLE/code/src/ExpandingElements/patternMatchingResultsFinal.txt", 'a')
    # pattern matching in OCR files
    print(len(ocr_files))
    for i in range(len(ocr_files)):
        #print(i, ". processing: ", ocr_files[i])
        resultText = match_patterns(ocr_files[i])
        #print(resultText)
        modded = resultText.copy()
        modded['filename'] = modded['filename'].split('/')[-1]
        writing.write(str(resultText))
        writing1.write(str(modded))
        writing.write('\n==========================================================\n')
        writing1.write('\n==========================================================\n')

    writing.close()
    writing1.close()


    results = open(".../MIRACLE/code/src/ExpandingElements/patternMatchingResults.txt")
    count = 0
    import shutil
    detected = []
    notDetected = '.../object_detection_frcnn_mscoco_boilerplate/testSet/notDetected'
    copyFrom = ".../object_detection_frcnn_mscoco_boilerplate/testSet/allCombined/"
    for i in results: 
        if "======" not in i and "\'match_info\': []" not in i:
            filename = i.split('/OCRtxt/')[1].split(',')[0].strip('\'')
            detectObj = [filename, "Text"]
            detected.append(detectObj)
        elif "======" not in i and "\'match_info\': []" in i:
            filename = i.split('/OCRtxt/')[1].split(',')[0].strip('\'')
            detectObj = [filename, "NoText"]
            detected.append(detectObj)
            shutil.copy(copyFrom + filename[:-5] + ".png", notDetected)

    print("MATCHED PATTERNS")

    shutil.copyfile(".../MIRACLE/code/src/ExpandingElements/patternMatchingResultsFinal.txt", ".../MIRACLE/results/patternMatchingResultsFinal.txt")

#getExpandingScreens(pngPath, xmlPath)


    #objectDetect()

    #analysis()














