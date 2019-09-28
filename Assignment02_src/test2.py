#!/usr/bin/python3

import cv2
import numpy as np
from tkinter import filedialog

test_image = filedialog.askopenfilename()
image_data = cv2.imread(test_image)
testImageDataArray = np.array(image_data)

meanTestImage = np.mean(testImageDataArray)
medianTestImage = np.median(testImageDataArray)
minTest = np.min(testImageDataArray)
maxTest = np.max(testImageDataArray)
midrangeTestImage = (minTest + maxTest) / 2

print("New Image:\nMean:", meanTestImage, "Median:", medianTestImage, "Midrange:", midrangeTestImage)
