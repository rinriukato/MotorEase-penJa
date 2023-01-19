import glob
import pattern_matching.matching as pattern_matching
import os
# get OCR files
ocr_files = [file for file in glob.glob(".../testSet/ocr/" + "*.json")] # provide location of the OCR files
ocr_files.sort()
# print(ocr_files)
os.remove(".../testSet/patternMatchingResults.txt")
writing = open(".../testSet/patternMatchingResults.txt", 'a')
# pattern matching in OCR files
print(len(ocr_files))
for i in range(len(ocr_files)):
    print(i, ". processing: ", ocr_files[i])
    resultText = pattern_matching.match_patterns(ocr_files[i])
    #print(resultText)
    writing.write(str(resultText))
    writing.write('\n==========================================================\n')

writing.close()