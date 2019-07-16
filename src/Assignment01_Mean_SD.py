import os
import cv2
import numpy as np
import pandas as pd
import re

os.chdir("/home/cseku160212/PycharmProjects/DataMining/Train and test ETH 80 dataset/TrainETH80data2952")
allImages = sorted(os.listdir("."))

outputDir = "/home/cseku160212/PycharmProjects/DataMining/Assignment01Output/"

imageLabel = []
MeanList = []
standardDeviationList = []

for eachImage in allImages:
    image = cv2.imread(eachImage, cv2.IMREAD_GRAYSCALE)
    imageIntensityArray = np.array(image)

    label = re.split('1|2|3|4|5|6|7|8|9|-', eachImage)

    imageLabel.append(label[0])

    mean = np.round(np.mean(imageIntensityArray), 3)
    MeanList.append(mean)

    sd = round(np.std(imageIntensityArray), 3)
    standardDeviationList.append(sd)
    print("For Image", eachImage, "Mean = ", mean, "\tStandard Deviation: ", sd)


os.chdir(outputDir)

df = pd.DataFrame({'Label': imageLabel, 'Mean': MeanList, 'Standard Deviation': standardDeviationList})

writer = pd.ExcelWriter('Assignment01Output.xlsx', engine='xlsxwriter')

df.to_excel(writer, sheet_name='Sheet1')

writer.save()



