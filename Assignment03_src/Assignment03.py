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
from scipy import stats


def mad(data, axis=None):
    return np.mean(np.absolute(data - np.mean(data, axis)), axis)


def load_training_button_onclick():
    global training_folder_path
    display.configure(text="Object Type Will be Shown here")
    training_folder_path = filedialog.askdirectory()
    if training_folder_path != "":
        messagebox.showinfo("Training Image Loader Message", "Loaded Training Images Successfully.")
        print(training_folder_path)
    else:
        print("No folder is selected.")
        messagebox.showinfo("Error Message", "No folder is selected.")


def extract_features_button_onclick():
    display.configure(text="Object Type Will be Shown here")
    if training_folder_path == "":
        print("Path is not selected, please select first.")
        messagebox.showinfo("Error Message", "Path is not selected, please select first.")
    else:
        os.chdir(training_folder_path)
        allImages = sorted(os.listdir("."))

        outputDir = r"/home/cseku160212/PycharmProjects/DataMining/Assignment03Output"
        os.chdir(outputDir)

        workbook = xlsxwriter.Workbook("Assignment03Output.xlsx")
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', 'Label', bold)
        worksheet.write('B1', 'Minimum', bold)
        worksheet.write('C1', 'Q1', bold)
        worksheet.write('D1', 'Median', bold)
        worksheet.write('E1', 'Q3', bold)
        worksheet.write('F1', 'Maximum', bold)
        worksheet.write('G1', 'Variance', bold)
        worksheet.write('H1', 'MeanDeviation', bold)
        worksheet.write('I1', 'Skewness', bold)
        worksheet.write('J1', 'CoefficientOfVariation', bold)

        row = 1
        column = 0

        messagebox.showinfo("Extraction Message", "You will be notified after the Extraction.\nTo start the "
                                                  "Extraction please click on OK Button or Close the window!")
        print("Feature Extraction Starts...")

        for eachImage in allImages:
            os.chdir(training_folder_path)

            image = cv2.imread(eachImage, cv2.IMREAD_GRAYSCALE)
            imageIntensityArray = np.array(image, dtype='int64')

            label = re.split('1|2|3|4|5|6|7|8|9|-', eachImage)
            minimum = np.min(imageIntensityArray)
            q1 = np.percentile(imageIntensityArray, 25)
            median = np.median(imageIntensityArray)
            q3 = np.percentile(imageIntensityArray, 75)
            maximum = np.max(imageIntensityArray)
            variance = np.var(imageIntensityArray)
            mean_deviation = mad(imageIntensityArray)
            skewness = stats.skew(imageIntensityArray, axis=None)
            coefficient_of_variation = stats.variation(imageIntensityArray, axis=None)

            os.chdir(outputDir)
            worksheet.write(row, column, label[0])
            worksheet.write(row, column + 1, minimum)
            worksheet.write(row, column + 2, q1)
            worksheet.write(row, column + 3, median)
            worksheet.write(row, column + 4, q3)
            worksheet.write(row, column + 5, maximum)
            worksheet.write(row, column + 6, variance)
            worksheet.write(row, column + 7, mean_deviation)
            worksheet.write(row, column + 8, skewness)
            worksheet.write(row, column + 9, coefficient_of_variation)

            print("Extracting Image " + eachImage)

            row += 1

        print("Features Extracted and Stored in Database successfully.")
        workbook.close()
        messagebox.showinfo("Features Extraction Message", "Features extracted successfully")


def load_features_button_onclick():
    global label_list, minimum_list, q1_list, median_list, q3_list, maximum_list, variance_list
    global mean_deviation_list, skewness_list, coefficient_of_variation_list, load_features_file

    load_features_file = ""

    display.configure(text="Object Type Will be Shown here")

    load_features_file = filedialog.askopenfilename()

    if load_features_file != "":
        df = pd.read_excel(load_features_file)
        label_list = df.iloc[:, 0]
        minimum_list = df.iloc[:, 1]
        q1_list = df.iloc[:, 2]
        median_list = df.iloc[:, 3]
        q3_list = df.iloc[:, 4]
        maximum_list = df.iloc[:, 5]
        variance_list = df.iloc[:, 6]
        mean_deviation_list = df.iloc[:, 7]
        skewness_list = df.iloc[:, 8]
        coefficient_of_variation_list = df.iloc[:, 9]

        messagebox.showinfo("Features Data Loader Message", "Features Data Loaded Successfully")

    else:
        print("No Features Data File selected.")
        messagebox.showinfo("Error Message", "No Features Data File is selected, Please Select First.")


def load_query_image_onclick():
    global minimum_test_image, q1_test_image, median_test_image, q3_test_image, maximum_test_image
    global variance_test_image, mean_deviation_test_image, skewness_test_image, coefficient_of_variation_test_image
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

            minimum_test_image = np.min(testImageDataArray)
            q1_test_image = np.percentile(testImageDataArray, 25)
            median_test_image = np.median(testImageDataArray)
            q3_test_image = np.percentile(testImageDataArray, 75)
            maximum_test_image = np.max(testImageDataArray)
            variance_test_image = np.var(testImageDataArray)
            mean_deviation_test_image = mad(testImageDataArray)
            skewness_test_image = stats.skew(testImageDataArray, axis=None)
            coefficient_of_variation_test_image = stats.variation(testImageDataArray, axis=None)

            print("Test Image Loaded Successfully..")
            messagebox.showinfo("Test Image Selector Message", "Test Image Selected Successfully")


def recognition_button_onclick():
    global label_list, minimum_list, q1_list, median_list, q3_list, maximum_list, variance_list
    global mean_deviation_list, skewness_list, coefficient_of_variation_list
    global minimum_test_image, q1_test_image, median_test_image, q3_test_image, maximum_test_image
    global variance_test_image, mean_deviation_test_image, skewness_test_image, coefficient_of_variation_test_image
    n = 9
    display.configure(text="Object Type Will be Shown here")

    a0b0 = minimum_list[0] * minimum_test_image + q1_list[0] * q1_test_image + median_list[0] * median_test_image +\
           q3_list[0] * q3_test_image + maximum_list[0] * maximum_test_image + \
           variance_list[0] * variance_test_image + mean_deviation_list[0] * mean_deviation_test_image +\
           skewness_list[0] * skewness_test_image + coefficient_of_variation_list[0] * coefficient_of_variation_test_image

    A_mean = np.mean([minimum_list[0], q1_list[0], median_list[0], q3_list[0], maximum_list[0],
                     variance_list[0], mean_deviation_list[0], skewness_list[0], coefficient_of_variation_list[0]])

    B_mean = np.mean([minimum_test_image, q1_test_image, median_test_image, q3_test_image,
                     maximum_test_image, variance_test_image, mean_deviation_test_image,
                     skewness_test_image, coefficient_of_variation_test_image])

    sigma_A = np.std([minimum_list[0], q1_list[0], median_list[0], q3_list[0], maximum_list[0],
                     variance_list[0], mean_deviation_list[0], skewness_list[0], coefficient_of_variation_list[0]])

    sigma_B = np.std([minimum_test_image, q1_test_image, median_test_image, q3_test_image,
                     maximum_test_image, variance_test_image, mean_deviation_test_image,
                     skewness_test_image, coefficient_of_variation_test_image])

    max_corelation = (a0b0 - n * A_mean * B_mean) / (n * sigma_A * sigma_B)

    index = 0
    max_index = 0
    for mi, q1, med, q3, ma, v, md, s, cov in zip(minimum_list, q1_list, median_list, q3_list,
                                                  maximum_list, variance_list, mean_deviation_list, skewness_list, coefficient_of_variation_list):
        aibi = mi * minimum_test_image + q1 * q1_test_image + med * median_test_image + \
               q3 * q3_test_image + ma * maximum_test_image + v * variance_test_image + \
               md * mean_deviation_test_image + s * skewness_test_image + cov * coefficient_of_variation_test_image

        A_mean2 = np.mean([mi, q1, med, q3, ma, v, md, s, cov])

        sigma2_A = np.std([mi, q1, med, q3, ma, v, md, s, cov])

        corelation = (aibi - n * A_mean2 * B_mean) / (n * sigma2_A * sigma_B)

        if corelation > max_corelation:
            max_corelation = corelation
            max_index = index

        index += 1

    message = "Test Object Type: "+label_list[max_index]
    print(message)
    display.configure(text=message)
    messagebox.showinfo("Recognition Message", "Image Recognized Successfully")


#Main program Starts here
#global variables

training_folder_path = ""
load_features_file = ""
label_list = []
minimum_list = []
q1_list = []
median_list = []
q3_list = []
maximum_list = []
variance_list = []
mean_deviation_list = []
skewness_list = []
coefficient_of_variation_list = []

minimum_test_image = 0
q1_test_image = 0
median_test_image = 0
q3_test_image = 0
maximum_test_image = 0
variance_test_image = 0
mean_deviation_test_image = 0
skewness_test_image = 0
coefficient_of_variation_test_image = 0


root = tk.Tk()
root.title("Object recognition using DD  measures and Correlation")
root.geometry("920x400")

topframe = tk.Frame(root, padx=50, pady=50, height=350, width=480)
topframe.pack(side='top')

display = tk.Label(topframe, text="Object Type Will be Shown here", padx=100, pady=100)
display.grid(row=5, column=10)

bottomframe = tk.Frame(root, padx=20, pady=20)
bottomframe.pack(side='bottom')

loadTrainingFolderButton = tk.Button(bottomframe, text="Load Training images", padx=10, pady=10,
                                     command=load_training_button_onclick)
extractFeaturesButton = tk.Button(bottomframe, text="Extract Feature and store in database", padx=10, pady=10,
                                  command=extract_features_button_onclick)
loadFeaturesData = tk.Button(bottomframe, text="Load Feature Data", padx=10, pady=10,
                             command=load_features_button_onclick)
loadQueryImageButton = tk.Button(bottomframe, text="Load Query image", padx=10, pady=10, command=load_query_image_onclick)
recognitionButton = tk.Button(bottomframe, text="Recognition", padx=10, pady=10, command=recognition_button_onclick)

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
