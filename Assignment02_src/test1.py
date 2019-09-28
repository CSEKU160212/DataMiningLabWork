#!/usr/bin/python3

import cv2
import numpy as np

image_data = cv2.imread(r'/home/cseku160212/PycharmProjects/DataMining/test/apple1-022-180.png')
testImageDataArray = np.array(image_data)

meanTestImage = np.mean(testImageDataArray)
medianTestImage = np.median(testImageDataArray)
minTest = np.min(testImageDataArray)
maxTest = np.max(testImageDataArray)
midrangeTestImage = (minTest + maxTest) / 2

print("New Image:\nMean:", meanTestImage, "Median:", medianTestImage, "Midrange:", midrangeTestImage)
