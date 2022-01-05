#!/usr/bin/python

import sys

args_count = len(sys.argv)

if args_count != 2:
  print("Please specify file name!")
  exit(1)

filepath = sys.argv[1]
print("Loading file {}…".format(filepath))

import pytesseract
from pytesseract import Output
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Read the image
image = cv2.imread(filepath)
# convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# blur
# blur = cv2.GaussianBlur(gray, (0,0), sigmaX=33, sigmaY=33)

# divide
# divide = cv2.divide(gray, blur, scale=255)

# otsu threshold
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_TOZERO)[1]

filename = 'savedImage.jpg'

d = pytesseract.image_to_data(thresh, output_type=Output.DICT)
n_boxes = len(d['level'])
for i in range(n_boxes):
	(x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])    

img = cv2.rectangle(thresh, (x, y), (x + w, y + h), (255, 255, 255), 2)

extracted_text = pytesseract.image_to_string(image, lang = 'swe')

cv2.imwrite(filename, img)

receipt_ocr = {}

splits = extracted_text.rstrip("\n")
splits = splits.splitlines()
name = splits[0]

print(splits)

file = open(r"{}.txt".format(filepath),"w+")

for line in splits:
  line_splits = line.split()
  for line_split in line_splits:
    line_split = line_split.strip()
    if len(line_split) == 0:
      continue

    file.writelines(line_split + "\n")
    print(line_split)

file.close()

# import re

# lines_with_sek = []
# reciept = []

# for line in splits:
#   if re.search('VOLT',line):
#     reciept.append(line)
    
#   if re.search('SEK',line):
#     lines_with_sek.append(line)
    
#   if re.search('Totalt',line):
#     reciept.append(line)
  
#   if re.search('Moms', line):
#     reciept.append(line)

# print(reciept)