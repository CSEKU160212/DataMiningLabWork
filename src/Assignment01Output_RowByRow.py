import os
import cv2
import numpy as np
import re
import xlsxwriter

os.chdir("/home/cseku160212/PycharmProjects/DataMining/Train and test ETH 80 dataset/TrainETH80data2952")
allImages = sorted(os.listdir("."))

outputDir = "/home/cseku160212/PycharmProjects/DataMining/Assignment01Output/"
os.chdir(outputDir)

workbook = xlsxwriter.Workbook("Assignment01_Mean_SD_OneByOneInsertion.xlsx")
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': True})

worksheet.write('A1', 'Label', bold)
worksheet.write('B1', 'Mean', bold)
worksheet.write('C1', 'Standard Deviation', bold)

row = 1
column = 0

for eachImage in allImages:
    os.chdir("/home/cseku160212/PycharmProjects/DataMining/Train and test ETH 80 dataset/TrainETH80data2952")
    image = cv2.imread(eachImage, cv2.IMREAD_GRAYSCALE)
    imageIntensityArray = np.array(image)

    label = re.split('1|2|3|4|5|6|7|8|9|-', eachImage)
    mean = np.mean(imageIntensityArray)
    sd = np.std(imageIntensityArray)

    os.chdir(outputDir)
    worksheet.write(row, column, label[0])
    worksheet.write(row, column + 1, mean)
    worksheet.write(row, column + 2, sd)

    print("For Image", eachImage, "Mean = ", mean, "\tStandard Deviation: ", sd)
    row += 1

workbook.close()




