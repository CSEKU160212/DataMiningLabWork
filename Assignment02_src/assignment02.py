#!/usr/bin/python3

import os
import cv2
import re
import xlsxwriter
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd


def load_training_folder():
    global training_folder_path
    display.configure(text="Object Type Will be Shown here")
    training_folder_path = filedialog.askdirectory()
    if training_folder_path != "":
        messagebox.showinfo("Training Image Loader Message", "Loaded Training Images Successfully.")
        print(training_folder_path)
    else:
        print("No folder is selected.")
        messagebox.showinfo("Error Message", "No folder is selected.")


def extract_features_and_store_in_database():
    display.configure(text="Object Type Will be Shown here")
    if training_folder_path == "":
        print("Path is not selected, please select first.")
        messagebox.showinfo("Error Message", "Path is not selected, please select first.")
    else:
        os.chdir(training_folder_path)
        allImages = sorted(os.listdir("."))

        outputDir = r"/home/cseku160212/PycharmProjects/DataMining/Assignment02_Output"
        os.chdir(outputDir)

        workbook = xlsxwriter.Workbook("Assignment02.xlsx")
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', 'Label', bold)
        worksheet.write('B1', 'Mean', bold)
        worksheet.write('C1', 'Median', bold)
        worksheet.write('D1', 'Midrange', bold)

        row = 1
        column = 0

        messagebox.showinfo("Extraction Message", "You will be notified after the Extraction. \nTo start the Extraction please click on OK Button or Close the window!")

        for eachImage in allImages:
            os.chdir(training_folder_path)
            image = cv2.imread(eachImage, cv2.IMREAD_GRAYSCALE)
            imageIntensityArray = np.array(image, dtype='int64')

            label = re.split('1|2|3|4|5|6|7|8|9|-', eachImage)
            mean = np.mean(imageIntensityArray)
            median = np.median(imageIntensityArray)
            min = np.min(imageIntensityArray)
            max = np.max(imageIntensityArray)
            midrange = (min + max) / 2

            os.chdir(outputDir)
            worksheet.write(row, column, label[0])
            worksheet.write(row, column + 1, mean)
            worksheet.write(row, column + 2, median)
            worksheet.write(row, column + 3, midrange)

            print("For Image", eachImage, "Mean = ", mean, "\tmedian: ", median, "\tmidrange:", midrange)
            row += 1

        workbook.close()
        messagebox.showinfo("Features Extraction Message", "Features extracted successfully")


def load_features_data():
    global labelList
    global meanList
    global medianList
    global midrangeList
    global load_features_file
    load_features_file = ""

    display.configure(text="Object Type Will be Shown here")

    load_features_file = filedialog.askopenfilename()

    if load_features_file != "":
        df = pd.read_excel(load_features_file)
        labelList = df.iloc[:, 0]
        meanList = df.iloc[:, 1]
        medianList = df.iloc[:, 2]
        midrangeList = df.iloc[:, 3]
        messagebox.showinfo("Features Data Loader Message", "Features Data Loaded Successfully")
    else:
        print("No Features Data File selected.")
        messagebox.showinfo("Error Message", "No Features Data File is selected, Please Select First.")


def load_query_image():
    global meanTestImage
    global medianTestImage
    global midrangeTestImage
    global load_features_file

    display.configure(text="Object Type Will be Shown here")

    if load_features_file == "":
        print("Please Load Features File First.")
        messagebox.showinfo("Error Message", "Please Load Features File First.")
    else:
        test_image = filedialog.askopenfilename()
        if test_image != "":
            print(test_image)
            image_data = cv2.imread(test_image, cv2.IMREAD_GRAYSCALE)
            testImageDataArray = np.array(image_data, dtype='int64')

            meanTestImage = np.mean(testImageDataArray)
            medianTestImage = np.median(testImageDataArray)
            minTest = np.min(testImageDataArray)
            maxTest = np.max(testImageDataArray)
            midrangeTestImage = (minTest + maxTest) / 2

            print("New Image:\nMean:", meanTestImage, "Median:", medianTestImage, "Midrange:", midrangeTestImage)
            messagebox.showinfo("Test Image Selector Message", "Test Image Selected Successfully")
            print(mode)

def recognition_test_image():
    global meanTestImage
    global medianTestImage
    global midrangeTestImage

    display.configure(text="Object Type Will be Shown here")

    minimumDistance = np.sqrt((meanTestImage - meanList[0])**2 + (medianTestImage - medianList[0])**2 + (midrangeTestImage-midrangeList[0])**2)

    index = 0
    minIndex = 0

    for label, mean, median, midrange in zip(labelList, meanList, medianList, midrangeList):
        eucledianDistance = np.sqrt((meanTestImage - mean)**2 + (medianTestImage - median)**2 + (midrangeTestImage-midrange)**2 )
        if eucledianDistance <= minimumDistance:
            minimumDistance = eucledianDistance
            minIndex = index
        index += 1

    message = "Test Object Type: "+labelList[minIndex]
    print(message)
    display.configure(text=message)
    messagebox.showinfo("Recognition Message", "Image Recognized Successfully")


#Main program Starts here
#global variables
global training_folder_path, load_features_file, labelList, meanList, medianList, midrangeList, meanTestImage, medianTestImage, midrangeTestImage
training_folder_path = ""
load_features_file = ""
labelList = []
meanList = []
medianList = []
midrangeList = []

meanTestImage = 0
medianTestImage = 0
midrangeTestImage = 0


root = tk.Tk()
root.title("Object Recognition using Euclidean Distance")
root.geometry("920x400")

topframe = tk.Frame(root, padx=50, pady=50, height=350, width=480)
topframe.pack(side='top')

display = tk.Label(topframe, text="Object Type Will be Shown here", padx=100, pady=100)
display.grid(row=5, column=10)

bottomframe = tk.Frame(root, padx=20, pady=20)
bottomframe.pack(side='bottom')

loadTrainingFolderButton = tk.Button(bottomframe, text="Load Training images", padx=10, pady=10, command=load_training_folder)
extractFeaturesButton = tk.Button(bottomframe, text="Extract Feature and store in database", padx=10, pady=10, command=extract_features_and_store_in_database)
loadFeaturesData = tk.Button(bottomframe, text="Load Feature Data", padx=10, pady=10, command=load_features_data)
loadQueryImageButton = tk.Button(bottomframe, text="Load Query image", padx=10, pady=10, command=load_query_image)
recognitionButton = tk.Button(bottomframe, text="Recognition", padx=10, pady=10, command=recognition_test_image)

loadTrainingFolderButton.pack(side='left')
extractFeaturesButton.pack(side='left')
loadFeaturesData.pack(side='left')
loadQueryImageButton.pack(side='left')
recognitionButton.pack(side='left')

loadTrainingFolderButton.configure(background='red')
extractFeaturesButton.configure(background='green')
loadFeaturesData.configure(background='blue')
loadQueryImageButton.configure(background='yellow')
recognitionButton.configure(background='white')

root.mainloop()

