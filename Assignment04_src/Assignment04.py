#!/usr/bin/python3

import os
import cv2
import xlsxwriter
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from scipy import stats
import pandas as pd
from skimage.feature import local_binary_pattern
from scipy.stats import itemfreq
from sklearn import tree


#global variables
training_folder_path = ""
total_cols = 0
labelList = []
meanList = []
medianList = []
modeList = []
midrangeList = []
load_features_file = ""
minimum_list = []
q1_list = []
q3_list = []
maximum_list = []
variance_list = []
mean_deviation_list = []
skewness_list = []
cov_list = []
hist = []

label_test_list = []
mean_test_list = []
median_test_list = []
mode_test_list = []
midrange_test_list = []
minimum_test_list = []
q1_test_list = []
q3_test_list = []
maximum_test_list = []
variance_test_list = []
mean_deviation_test_list = []
skewness_test_list = []
cov_test_list = []
hist_test = []

outputDir = r"/home/cseku160212/PycharmProjects/DataMining/Assignment04_output"


def mad(data, axis=None):
    return np.mean(np.absolute(data - np.mean(data, axis)), axis)


def load_training_images_onclick():
    global training_folder_path

    training_folder_path = filedialog.askdirectory()
    if training_folder_path != "":
        messagebox.showinfo("Training Image Loader Message", "Loaded Training Images Successfully.")
        print(training_folder_path)
    else:
        print("No folder is selected.")
        messagebox.showinfo("Error Message", "No folder is selected.")


def extract_ct_feature_onclick():
    global outputDir
    if training_folder_path == "":
        print("Path is not selected, please select first.")
        messagebox.showinfo("Error Message", "Path is not selected, please select first.")
    else:
        os.chdir(training_folder_path)
        allImages = sorted(os.listdir("."))

        os.chdir(outputDir)

        workbook = xlsxwriter.Workbook("CT_Features.xlsx")
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', 'Label', bold)
        worksheet.write('B1', 'Mean', bold)
        worksheet.write('C1', 'Median', bold)
        worksheet.write('D1', 'Mode', bold)
        worksheet.write('E1', 'Midrange', bold)

        row = 1
        column = 0

        messagebox.showinfo("Extraction Message", "You will be notified after the Extraction. \nTo "
                                                  "start the Extraction please click on OK Button or Close the window!")

        for eachImage in allImages:
            os.chdir(training_folder_path)
            image = cv2.imread(eachImage, cv2.IMREAD_GRAYSCALE)
            imageIntensityArray = np.array(image, dtype='int64')

            label = eachImage.split('.')
            label_main = label[0] + "." + label[1]
            print(label_main)
            mean = np.mean(imageIntensityArray)
            median = np.median(imageIntensityArray)

            count = []
            for j in range(0, len(image)):
                count.append(0)

            for i in range(0, len(image)):
                for k in range(0, len(image)):
                    if image[i][k] == k:
                        count[k] += 1

            n = np.max(count)
            mode = []
            for i in range(0, len(count)):
                if count[i] == n:
                    mode.append(i)

            mode1 = int(mode[0])

            min = np.min(imageIntensityArray)
            max = np.max(imageIntensityArray)
            midrange = (min + max) / 2

            os.chdir(outputDir)
            worksheet.write(row, column, label_main)
            worksheet.write(row, column + 1, mean)
            worksheet.write(row, column + 2, median)
            worksheet.write(row, column + 3, mode1)
            worksheet.write(row, column + 4, midrange)

            print("Feature Extracting, Please wait.")
            row += 1

        workbook.close()
        messagebox.showinfo("Features Extraction Message", "Features extracted successfully")


def extract_dd_feature_onclick():
    global outputDir

    if training_folder_path == "":
        print("Path is not selected, please select first.")
        messagebox.showinfo("Error Message", "Path is not selected, please select first.")
    else:
        os.chdir(training_folder_path)
        allImages = sorted(os.listdir("."))

        os.chdir(outputDir)

        workbook = xlsxwriter.Workbook("DD_Features.xlsx")
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

            label = eachImage.split('.')
            label_main = label[0] + "." + label[1]
            print(label_main)

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
            worksheet.write(row, column, label_main)
            worksheet.write(row, column + 1, minimum)
            worksheet.write(row, column + 2, q1)
            worksheet.write(row, column + 3, median)
            worksheet.write(row, column + 4, q3)
            worksheet.write(row, column + 5, maximum)
            worksheet.write(row, column + 6, variance)
            worksheet.write(row, column + 7, mean_deviation)
            worksheet.write(row, column + 8, skewness)
            worksheet.write(row, column + 9, coefficient_of_variation)

            print("Feature Extracting, Please wait.")

            row += 1

        print("Features Extracted and Stored in Database successfully.")
        workbook.close()
        messagebox.showinfo("Features Extraction Message", "Features extracted successfully")


def extract_ctdd_feature_onclick():
    global outputDir
    if training_folder_path == "":
        print("Path is not selected, please select first.")
        messagebox.showinfo("Error Message", "Path is not selected, please select first.")
    else:
        os.chdir(training_folder_path)
        allImages = sorted(os.listdir("."))

        os.chdir(outputDir)

        workbook = xlsxwriter.Workbook("CTandDD_Features.xlsx")
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', 'Label', bold)
        worksheet.write('B1', 'Mean', bold)
        worksheet.write('C1', 'Median', bold)
        worksheet.write('D1', 'Mode', bold)
        worksheet.write('E1', 'Midrange', bold)
        worksheet.write('F1', 'Minimum', bold)
        worksheet.write('G1', 'Q1', bold)
        worksheet.write('H1', 'Q3', bold)
        worksheet.write('I1', 'Maximum', bold)
        worksheet.write('J1', 'Variance', bold)
        worksheet.write('K1', 'MeanDeviation', bold)
        worksheet.write('L1', 'Skewness', bold)
        worksheet.write('M1', 'CoefficientOfVariation', bold)

        row = 1
        column = 0

        messagebox.showinfo("Extraction Message",
                            "You will be notified after the Extraction. "
                            "\nTo start the Extraction please click on OK Button or Close the window!")

        for eachImage in allImages:
            os.chdir(training_folder_path)
            image = cv2.imread(eachImage, cv2.IMREAD_GRAYSCALE)
            imageIntensityArray = np.array(image, dtype='int64')

            label = eachImage.split('.')
            label_main = label[0] + "." + label[1]

            mean = np.mean(imageIntensityArray)
            median = np.median(imageIntensityArray)

            count = []
            for j in range(0, len(image)):
                count.append(0)

            for i in range(0, len(image)):
                for k in range(0, len(image)):
                    if image[i][k] == k:
                        count[k] += 1

            n = np.max(count)
            mode = []
            for i in range(0, len(count)):
                if count[i] == n:
                    mode.append(i)

            mode1 = int(mode[0])

            min = np.min(imageIntensityArray)
            max = np.max(imageIntensityArray)
            midrange = (min + max) / 2

            minimum = np.min(imageIntensityArray)
            q1 = np.percentile(imageIntensityArray, 25)
            q3 = np.percentile(imageIntensityArray, 75)
            maximum = np.max(imageIntensityArray)
            variance = np.var(imageIntensityArray)
            mean_deviation = mad(imageIntensityArray)
            skewness = stats.skew(imageIntensityArray, axis=None)
            coefficient_of_variation = stats.variation(imageIntensityArray, axis=None)

            os.chdir(outputDir)
            worksheet.write(row, column, label_main)
            worksheet.write(row, column + 1, mean)
            worksheet.write(row, column + 2, median)
            worksheet.write(row, column + 3, mode1)
            worksheet.write(row, column + 4, midrange)
            worksheet.write(row, column + 5, minimum)
            worksheet.write(row, column + 6, q1)
            worksheet.write(row, column + 7, q3)
            worksheet.write(row, column + 8, maximum)
            worksheet.write(row, column + 9, variance)
            worksheet.write(row, column + 10, mean_deviation)
            worksheet.write(row, column + 11, skewness)
            worksheet.write(row, column + 12, coefficient_of_variation)

            print("Feature Extracting, Please wait.")

            row += 1

        workbook.close()
        messagebox.showinfo("Features Extraction Message", "Features extracted successfully")


def lbp_histogram(image):
    radius = 1
    no_points = 8 * radius
    lbp = local_binary_pattern(image, no_points, radius, method='uniform')
    x = itemfreq(lbp.ravel())
    hist = x[:, 1] / sum(x[:, 1])
    return hist


def extract_lbp_feature_onclick():
    global outputDir
    if training_folder_path == "":
        print("Path is not selected, please select first.")
        messagebox.showinfo("Error Message", "Path is not selected, please select first.")
    else:
        os.chdir(training_folder_path)
        allImages = sorted(os.listdir("."))
        print(training_folder_path)

        os.chdir(outputDir)
        workbook = xlsxwriter.Workbook("LBP_Feature.xlsx")
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', 'Label', bold)
        worksheet.write('B1', 'A', bold)
        worksheet.write('C1', 'B', bold)
        worksheet.write('D1', 'C', bold)
        worksheet.write('E1', 'D', bold)
        worksheet.write('F1', 'E', bold)
        worksheet.write('G1', 'F', bold)
        worksheet.write('H1', 'G', bold)
        worksheet.write('I1', 'H', bold)
        worksheet.write('J1', 'I', bold)
        worksheet.write('K1', 'J', bold)

        row = 1
        column = 0

        messagebox.showinfo("Extraction Message", "You will be notified after the Extraction.\nTo start the "
                                                  "Extraction please click on OK Button or Close the window!")
        # Code For LBP
        for eachImage in allImages:
            os.chdir(training_folder_path)
            print(eachImage)
            label = eachImage.split('.')
            label_main = label[0] + "." + label[1]

            image = cv2.imread(eachImage, cv2.IMREAD_GRAYSCALE)
            hist = lbp_histogram(image)

            worksheet.write(row, column, label_main)
            worksheet.write(row, column + 1, hist[0])
            worksheet.write(row, column + 2, hist[1])
            worksheet.write(row, column + 3, hist[2])
            worksheet.write(row, column + 4, hist[3])
            worksheet.write(row, column + 5, hist[4])
            worksheet.write(row, column + 6, hist[5])
            worksheet.write(row, column + 7, hist[6])
            worksheet.write(row, column + 8, hist[7])
            worksheet.write(row, column + 9, hist[8])
            worksheet.write(row, column + 10, hist[9])
            row += 1

        os.chdir(outputDir)
        workbook.close()
        print("Features Extracted and Stored in Database successfully.")
        messagebox.showinfo("Features Extraction Message", "Features extracted successfully")


def load_feature_data_onclick():
    global total_cols
    global labelList
    global meanList
    global medianList
    global modeList
    global midrangeList
    global load_features_file
    global minimum_list
    global q1_list
    global q3_list
    global maximum_list
    global variance_list
    global mean_deviation_list
    global skewness_list
    global cov_list
    global total_cols
    global hist_list

    load_features_file = filedialog.askopenfilename()
    if load_features_file != "":
        sheet = pd.read_excel(load_features_file)
        df = pd.DataFrame(sheet)
        total_cols = len(df.columns)
        print(total_cols)
    else:
        print("Please Select a File.")

    if total_cols == 5:
        if load_features_file != "":
            df = pd.read_excel(load_features_file)
            labelList = df.iloc[:, 0]
            meanList = df.iloc[:, 1]
            medianList = df.iloc[:, 2]
            modeList = df.iloc[:, 3]
            midrangeList = df.iloc[:, 4]
            messagebox.showinfo("Features Data Loader Message", "Features Data Loaded Successfully")
        else:
            print("No Features Data File selected.")
            messagebox.showinfo("Error Message", "No Features Data File is selected, Please Select First.")

    elif total_cols == 10:
        if load_features_file != "":
            df = pd.read_excel(load_features_file)
            labelList = df.iloc[:, 0]
            minimum_list = df.iloc[:, 1]
            q1_list = df.iloc[:, 2]
            medianList = df.iloc[:, 3]
            q3_list = df.iloc[:, 4]
            maximum_list = df.iloc[:, 5]
            variance_list = df.iloc[:, 6]
            mean_deviation_list = df.iloc[:, 7]
            skewness_list = df.iloc[:, 8]
            cov_list = df.iloc[:, 9]

            messagebox.showinfo("Features Data Loader Message", "Features Data Loaded Successfully")

        else:
            print("No Features Data File selected.")
            messagebox.showinfo("Error Message", "No Features Data File is selected, Please Select First.")

    elif total_cols == 13:
        if load_features_file != "":
            df = pd.read_excel(load_features_file)
            labelList = df.iloc[:, 0]
            meanList = df.iloc[:, 1]
            medianList = df.iloc[:, 2]
            modeList = df.iloc[:, 3]
            midrangeList = df.iloc[:, 4]
            minimum_list = df.iloc[:, 5]
            q1_list = df.iloc[:, 6]
            q3_list = df.iloc[:, 7]
            maximum_list = df.iloc[:, 8]
            variance_list = df.iloc[:, 9]
            mean_deviation_list = df.iloc[:, 10]
            skewness_list = df.iloc[:, 11]
            cov_list = df.iloc[:, 12]
            messagebox.showinfo("Features Data Loader Message", "Features Data Loaded Successfully")
        else:
            print("No Features Data File selected.")
            messagebox.showinfo("Error Message", "No Features Data File is selected, Please Select First.")

    else:
        if load_features_file != "":
            df = pd.read_excel(load_features_file)
            labelList = df.iloc[:, 0]
            for i in range(1, 11):
                hist.append(df.iloc[i, 1:])

            messagebox.showinfo("Features Data Loader Message", "Features Data Loaded Successfully")
        else:
            print("No Features Data File selected.")
            messagebox.showinfo("Error Message", "No Features Data File is selected, Please Select First.")


def load_query_image_folder_onclick():
    global total_cols
    global mean_test_list
    global median_test_list
    global mode_test_list
    global midrange_test_list
    global minimum_test_list
    global q1_test_list
    global q3_test_list
    global maximum_test_list
    global variance_test_list
    global mean_deviation_test_list
    global skewness_test_list
    global cov_test_list
    global label_test_list
    global hist_test

    test_folder_path = filedialog.askdirectory()

    if test_folder_path == "":
        print("Please Select Folder")
        messagebox.showinfo("Error Message", "Please Select Test Image Folder First.")
    else:
        if total_cols == 5:
            os.chdir(test_folder_path)
            allTestImages = sorted(os.listdir("."))

            for test_image in allTestImages:
                label = test_image

                image_data = cv2.imread(test_image, cv2.IMREAD_GRAYSCALE)
                testImageDataArray = np.array(image_data, dtype='int64')

                meanTestImage = np.mean(testImageDataArray)
                medianTestImage = np.median(testImageDataArray)

                count = []
                for j in range(0, len(image_data)):
                    count.append(0)

                for i in range(0, len(image_data)):
                    for k in range(0, len(image_data)):
                        if image_data[i][k] == k:
                            count[k] += 1

                n = np.max(count)
                mode = []
                for i in range(0, len(count)):
                    if count[i] == n:
                        mode.append(i)

                mode1 = int(mode[0])

                minTest = np.min(testImageDataArray)
                maxTest = np.max(testImageDataArray)
                midrangeTestImage = (minTest + maxTest) / 2

                label_test_list.append(label)
                mean_test_list.append(meanTestImage)
                median_test_list.append(medianTestImage)
                mode_test_list.append(mode1)
                midrange_test_list.append(midrangeTestImage)

                print("New Image:\nMean:", meanTestImage, "Median:", medianTestImage, "Midrange:", midrangeTestImage)

        elif total_cols == 10:
            os.chdir(test_folder_path)
            allTestImages = sorted(os.listdir("."))

            for test_image in allTestImages:

                image = cv2.imread(test_image, cv2.IMREAD_GRAYSCALE)
                imageIntensityArray = np.array(image, dtype='int64')

                minimum = np.min(imageIntensityArray)
                q1 = np.percentile(imageIntensityArray, 25)
                median = np.median(imageIntensityArray)
                q3 = np.percentile(imageIntensityArray, 75)
                maximum = np.max(imageIntensityArray)
                variance = np.var(imageIntensityArray)
                mean_deviation = mad(imageIntensityArray)
                skewness = stats.skew(imageIntensityArray, axis=None)
                coefficient_of_variation = stats.variation(imageIntensityArray, axis=None)

                label_test_list.append(test_image)
                minimum_test_list.append(minimum)
                q1_test_list.append(q1)
                median_test_list.append(median)
                q3_test_list.append(q3)
                maximum_test_list.append(maximum)
                variance_test_list.append(variance)
                mean_deviation_test_list.append(mean_deviation)
                skewness_test_list.append(skewness)
                cov_test_list.append(coefficient_of_variation)
                print("Extracting Test Image, Please Wait!!")

        elif total_cols == 13:
            os.chdir(test_folder_path)
            allTestImages = sorted(os.listdir("."))

            for test_image in allTestImages:
                image_data = cv2.imread(test_image, cv2.IMREAD_GRAYSCALE)
                testImageDataArray = np.array(image_data, dtype='int64')

                meanTestImage = np.mean(testImageDataArray)
                medianTestImage = np.median(testImageDataArray)

                count = []
                for j in range(0, len(image_data)):
                    count.append(0)

                for i in range(0, len(image_data)):
                    for k in range(0, len(image_data)):
                        if image_data[i][k] == k:
                            count[k] += 1

                n = np.max(count)
                mode = []
                for i in range(0, len(count)):
                    if count[i] == n:
                        mode.append(i)

                mode1 = int(mode[0])

                minTest = np.min(testImageDataArray)
                maxTest = np.max(testImageDataArray)
                midrangeTestImage = (minTest + maxTest) / 2

                minimum = np.min(testImageDataArray)
                q1 = np.percentile(testImageDataArray, 25)
                q3 = np.percentile(testImageDataArray, 75)
                maximum = np.max(testImageDataArray)
                variance = np.var(testImageDataArray)
                mean_deviation = mad(testImageDataArray)
                skewness = stats.skew(testImageDataArray, axis=None)
                coefficient_of_variation = stats.variation(testImageDataArray, axis=None)

                label_test_list.append(test_image)
                mean_test_list.append(meanTestImage)
                median_test_list.append(medianTestImage)
                mode_test_list.append(mode1)
                midrange_test_list.append(midrangeTestImage)
                minimum_test_list.append(minimum)
                q1_test_list.append(q1)
                q3_test_list.append(q3)
                maximum_test_list.append(maximum)
                variance_test_list.append(variance)
                mean_deviation_test_list.append(mean_deviation)
                skewness_test_list.append(skewness)
                cov_test_list.append(coefficient_of_variation)
                print("Feature Extracting")
                print(skewness)
        else:
            if test_folder_path == "":
                print("Path is not selected, please select first.")
                messagebox.showinfo("Error Message", "Path is not selected, please select first.")
            else:
                os.chdir(test_folder_path)
                allImages = sorted(os.listdir("."))

                messagebox.showinfo("Extraction Message", "You will be notified after the Extraction.\nTo start the "
                                                          "Extraction please click on OK Button or Close the window!")
                # Code For LBP
                for eachImage in allImages:
                    print(eachImage)
                    label_test_list.append(eachImage)

                    image = cv2.imread(eachImage, cv2.IMREAD_GRAYSCALE)
                    hist = lbp_histogram(image)
                    hist_test.append(hist)

                    print("Extracting Test Image, Please Wait!!")

    messagebox.showinfo("Success Message", "Image Folder Selection Successfull")


def euclidean_onclick():
    global total_cols
    global mean_test_list
    global median_test_list
    global mode_test_list
    global midrange_test_list
    global minimum_test_list
    global q1_test_list
    global q3_test_list
    global maximum_test_list
    global variance_test_list
    global mean_deviation_test_list
    global skewness_test_list
    global cov_test_list
    global label_test_list
    global hist_test
    global hist
    global outputDir

    if total_cols == 5:
        os.chdir(outputDir)

        workbook = xlsxwriter.Workbook("CT_ED_final.xlsx")
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', 'TestImageName', bold)
        worksheet.write('B1', 'ObjectType', bold)

        row = 1
        column = 0

        for tLabel, tMean, tMed, tMod, tMid in zip(label_test_list, mean_test_list, median_test_list, mode_test_list, midrange_test_list):

            minimumDistance = 999

            index = 0
            minIndex = 0

            for mean, median, mode, midrange in zip(meanList, medianList, modeList, midrangeList):
                eD = np.sqrt((tMean - mean) ** 2 + (tMed - median) ** 2 + (tMod - mode) ** 2 + (tMid - midrange) ** 2)
                if eD <= minimumDistance:
                    minimumDistance = eD
                    minIndex = index
                index += 1

            os.chdir(outputDir)
            worksheet.write(row, column, tLabel)
            worksheet.write(row, column + 1, labelList[minIndex])

            row += 1
            print("Recognizing, Please wait.")

        workbook.close()
        messagebox.showinfo("Recognition", "Recognition successfully Done.")

    elif total_cols == 10:
        os.chdir(outputDir)

        workbook = xlsxwriter.Workbook("DD_ED_final.xlsx")
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', 'TestImageName', bold)
        worksheet.write('B1', 'ObjectType', bold)

        row = 1
        column = 0
        for tLabel, tMin, tQ1, tMed, tQ3, tMax, tVar, tMeanDev, tSkewness, tCov in zip(label_test_list,
                                                                                       minimum_test_list,
                                                                                       q1_test_list, median_test_list,
                                                                                       q3_test_list, maximum_test_list,
                                                                                       variance_test_list,
                                                                                       mean_deviation_test_list,skewness_test_list,
                                                                                       cov_test_list):

            minimumDistance = 999

            index = 0
            minIndex = 0

            for mi, q1, med, q3, ma, v, md, s, cov in zip(minimum_list, q1_list, medianList, q3_list,
                                                          maximum_list, variance_list, mean_deviation_list,
                                                          skewness_list,
                                                          cov_list):
                eD = np.sqrt((tMin - mi) ** 2 + (tQ1 - q1) ** 2 +
                             (tMed - med) ** 2 + (tQ3 - q3) ** 2 +
                             (tMax - ma) ** 2 +
                             (tVar - v) ** 2 + (tMeanDev - md) ** 2 +
                             (tSkewness - s) ** 2 + (tCov - cov) ** 2)

                if eD <= minimumDistance:
                    minimumDistance = eD
                    minIndex = index
                index += 1

            os.chdir(outputDir)
            worksheet.write(row, column, tLabel)
            worksheet.write(row, column + 1, labelList[minIndex])

            row += 1
            print("Recognizing, Please wait.")

        workbook.close()
        messagebox.showinfo("Recognition", "Recognition successfully Done.")

    elif total_cols == 13:
        os.chdir(outputDir)

        workbook = xlsxwriter.Workbook("CT_DD_ED_final.xlsx")
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', 'TestImageName', bold)
        worksheet.write('B1', 'ObjectType', bold)

        row = 1
        column = 0
        for tLabel, tMean, tMed, tMod, tMid, tMin, tQ1, tQ3, tMax, tVar, tMeanDev, tSkewness, tCov in zip(label_test_list,
                mean_test_list, median_test_list, mode_test_list, midrange_test_list, minimum_test_list,q1_test_list,
                                                                                                          q3_test_list, maximum_test_list,
                                                                                                          variance_test_list, mean_deviation_test_list,skewness_test_list,
                                                                                                          cov_test_list):

            minimumDistance = 999
            index = 0
            minIndex = 0

            for mean, med, mode, mid, mi, q1, q3, ma, v, md, s, cov in zip(meanList, medianList, modeList, midrangeList,
                                                                           minimum_list, q1_list, q3_list,
                                                          maximum_list, variance_list, mean_deviation_list,
                                                          skewness_list,cov_list):

                eD = np.sqrt(
                    (tMean - mean) ** 2 + (tMed - med) ** 2 + (tMod - mode) ** 2 +
                    (tMid - mid) ** 2 + (tMin - mi) ** 2 +
                    (tQ1 - q1) ** 2 + (tQ3 - q3) ** 2 + (tMax - ma) ** 2 +
                    (tVar - v) ** 2 + (tMeanDev - md) ** 2 +
                    (tSkewness - s) ** 2 + (tCov - cov) ** 2)

                if eD <= minimumDistance:
                    minimumDistance = eD
                    minIndex = index
                index += 1

            os.chdir(outputDir)
            worksheet.write(row, column, tLabel)
            worksheet.write(row, column + 1, labelList[minIndex])

            row += 1
            print("Recognizing, Please wait.")

        workbook.close()
        messagebox.showinfo("Recognition", "Recognition successfully Done.")

    else:
        os.chdir(outputDir)

        workbook = xlsxwriter.Workbook("LBP_ED_final.xlsx")
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', 'TestImageName', bold)
        worksheet.write('B1', 'ObjectType', bold)
        row = 1
        column = 0
        mainIndex = 0
        for ht in hist_test:
            minimumDistance = 999
            index = 0
            minIndex = 0
            for h in hist:
                ed = (ht[0] - h[0])**2 + (ht[1] - h[1]) **2 + (ht[2]-h[2])**2 + (ht[3]-h[3])**2 + (ht[4]-h[4])**2+\
                      (ht[5] - h[5]) ** 2 +(ht[6]-h[6])**2+(ht[7]-h[7])**2+(ht[8]-h[8])**2+ (ht[9]-h[9])**2
                if ed < minimumDistance:
                    minimumDistance = ed
                    minIndex = index
                index += 1
            print("Recognizing, Please wait.")
            os.chdir(outputDir)
            worksheet.write(row, column, label_test_list[mainIndex])
            worksheet.write(row, column + 1, labelList[minIndex])
            row += 1
            mainIndex += 1

        workbook.close()
        messagebox.showinfo("Recognition", "Recognition successfully Done.")


def correlation_onclick():
    global total_cols
    global mean_test_list
    global median_test_list
    global mode_test_list
    global midrange_test_list
    global minimum_test_list
    global q1_test_list
    global q3_test_list
    global maximum_test_list
    global variance_test_list
    global mean_deviation_test_list
    global skewness_test_list
    global cov_test_list
    global label_test_list
    global hist
    global hist_test
    global  outputDir

    if total_cols == 5:
        os.chdir(outputDir)

        workbook = xlsxwriter.Workbook("CT_CR_final.xlsx")
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', 'TestImageName', bold)
        worksheet.write('B1', 'ObjectType', bold)

        row = 1
        column = 0
        n = 4

        for tLabel, tMean, tMed, tMod, tMid in zip(label_test_list, mean_test_list, median_test_list, mode_test_list,
                                                   midrange_test_list):
            index = 0
            max_index = 0
            max_corelation = -999
            for mean, median, mode, midrange in zip(meanList, medianList, modeList, midrangeList):

                aibi = mean * tMean + median * tMed + mode * tMod + midrange * tMid

                A_mean2 = np.mean([mean, median, mode, midrange])

                sigma2_A = np.std([mean, median, mode, midrange])

                B_mean2 = np.mean([tMean, tMed, tMod, tMid])

                sigma2_B = np.std([tMean, tMed, tMod, tMid])

                corelation = (aibi - n * A_mean2 * B_mean2) / (n * sigma2_A * sigma2_B)

                if corelation > max_corelation:
                    max_corelation = corelation
                    max_index = index

                index += 1
            print("Recognizing Please Wait..")
            os.chdir(outputDir)
            worksheet.write(row, column, tLabel)
            worksheet.write(row, column + 1, labelList[max_index])

            row += 1
        workbook.close()
        messagebox.showinfo("Recognition Message", "Image Recognized Successfully")

    elif total_cols == 10:
        os.chdir(outputDir)

        workbook = xlsxwriter.Workbook("DD_CR_final.xlsx")
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', 'TestImageName', bold)
        worksheet.write('B1', 'ObjectType', bold)

        row = 1
        column = 0
        n = 9

        for tLabel, tMin, tQ1, tMed, tQ3, tMax, tVar, tMeanDev, tSkewness, tCov in zip(label_test_list,
                                                                                       minimum_test_list,
                                                                                       q1_test_list, median_test_list,
                                                                                       q3_test_list,
                                                                                       maximum_test_list,
                                                                                       variance_test_list,
                                                                                       mean_deviation_test_list,
                                                                                       skewness_test_list,
                                                                                       cov_test_list):
            index = 0
            max_index = 0
            max_corelation = -999
            for mi, q1, med, q3, ma, v, md, s, cov in zip(minimum_list, q1_list, medianList, q3_list,
                                                          maximum_list, variance_list, mean_deviation_list,
                                                          skewness_list,
                                                          cov_list):
                aibi = mi * tMin + q1 * tQ1 + med * tMed + \
                       q3 * tQ3 + ma * tMax + v * tVar + \
                       md * tMeanDev + s * tSkewness + cov * tCov

                A_mean2 = np.mean([mi, q1, med, q3, ma, v, md, s, cov])

                sigma2_A = np.std([mi, q1, med, q3, ma, v, md, s, cov])

                B_mean2 = np.mean([tMin, tQ1, tMed, tQ3, tMax, tVar, tMeanDev, tSkewness, tCov])

                sigma2_B = np.std([tMin, tQ1, tMed, tQ3, tMax, tVar, tMeanDev, tSkewness, tCov])

                corelation = (aibi - n * A_mean2 * B_mean2) / (n * sigma2_A * sigma2_B)

                if corelation > max_corelation:
                    max_corelation = corelation
                    max_index = index

                index += 1

            print("Recognizing Please Wait..")
            os.chdir(outputDir)
            worksheet.write(row, column, tLabel)
            worksheet.write(row, column + 1, labelList[max_index])

            row += 1
        workbook.close()
        messagebox.showinfo("Recognition Message", "Image Recognized Successfully")

    elif total_cols == 13:
        os.chdir(outputDir)

        workbook = xlsxwriter.Workbook("CT_DD_CR_final.xlsx")
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', 'TestImageName', bold)
        worksheet.write('B1', 'ObjectType', bold)

        row = 1
        column = 0
        n = 12

        for tLabel, tMean, tMed, tMod, tMid, tMin, tQ1, tQ3, tMax, tVar, tMeanDev, tSkewness, tCov in \
                zip(label_test_list, mean_test_list,median_test_list, mode_test_list, midrange_test_list,
                    minimum_test_list, q1_test_list, q3_test_list,maximum_test_list, variance_test_list,
                    mean_deviation_test_list,skewness_test_list,cov_test_list):
            index = 0
            max_index = 0
            max_corelation = -999
            for mean, med, mod, mid, mi, q1, q3, ma, v, md, s, cov in zip(meanList, medianList, modeList, midrangeList,
                                                                          minimum_list, q1_list, q3_list,
                                                                          maximum_list, variance_list,
                                                                          mean_deviation_list,
                                                                          skewness_list, cov_list):
                aibi = mean* tMean + med * tMed + mod * tMod + mid * tMid+ mi * tMin + q1 * tQ1 + med * tMed +\
                       q3 * tQ3 + ma * tMax + v * tVar + md * tMeanDev + s * tSkewness + cov * tCov

                A_mean2 = np.mean([mean, med, mod, mid, mi, q1, q3, ma, v, md, s, cov])

                sigma2_A = np.std([mean, med, mod, mid, mi, q1, q3, ma, v, md, s, cov])

                B_mean2 = np.mean([tMean, tMed, tMod, tMid, tMin, tQ1, tQ3, tMax, tVar, tMeanDev, tSkewness, tCov])

                sigma2_B = np.std([tMean, tMed, tMod, tMid, tMin, tQ1, tQ3, tMax, tVar, tMeanDev, tSkewness, tCov])

                corelation = (aibi - n * A_mean2 * B_mean2) / (n * sigma2_A * sigma2_B)

                if corelation > max_corelation:
                    max_corelation = corelation
                    max_index = index

                index += 1
            print("Recognizing Please Wait..")
            os.chdir(outputDir)
            worksheet.write(row, column, tLabel)
            worksheet.write(row, column + 1, labelList[max_index])

            row += 1
        workbook.close()
        messagebox.showinfo("Recognition Message", "Image Recognized Successfully")

    else:
        os.chdir(outputDir)

        workbook = xlsxwriter.Workbook("LBP_CR_final.xlsx")
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', 'TestImageName', bold)
        worksheet.write('B1', 'ObjectType', bold)
        row = 1
        column = 0
        n = 10

        mainIndex = 0
        for ht in hist_test:
            max_corelation = -999
            index = 0
            max_index = 0
            for h in hist:
                aibi = h[0] * ht[0] +h[1] * ht[1] +h[2] * ht[2] +h[3] * ht[3] +h[4] * ht[4] +h[5] * ht[5] +h[6] * ht[6]+\
                       h[7] * ht[7] + h[8] * ht[8] + h[9] * ht[9]
                A_mean2 = np.mean(h)
                sigma2_A = np.std(h)
                B_mean2 = np.mean(ht)
                sigma2_B = np.std(ht)

                corelation = (aibi - n * A_mean2 * B_mean2) / (n * sigma2_A * sigma2_B)

                if corelation > max_corelation:
                    max_corelation = corelation
                    max_index = index
                index += 1
            print("Recognizing, Please wait.")
            os.chdir(outputDir)
            worksheet.write(row, column, label_test_list[mainIndex])
            worksheet.write(row, column + 1, labelList[max_index])
            row += 1
            mainIndex += 1
        print("Recognizing Completed!")
        workbook.close()
        messagebox.showinfo("Recognition", "Recognition successfully Done.")


def decision_tree_onclick():
    global total_cols
    global mean_test_list
    global median_test_list
    global mode_test_list
    global midrange_test_list
    global minimum_test_list
    global q1_test_list
    global q3_test_list
    global maximum_test_list
    global variance_test_list
    global mean_deviation_test_list
    global skewness_test_list
    global cov_test_list
    global label_test_list
    global hist
    global hist_test
    global outputDir

    if total_cols == 5:
        x_train = []
        x_label = []
        y_test = []
        for l, mean, med, mod, mid in zip(labelList, meanList, medianList, modeList, midrangeList):
            x_label.append(l)
            x_train.append([mean, med, mod, mid])
        print(x_train)
        print(x_label)

        for tmean, tmed, tmod, tmid in zip(mean_test_list, median_test_list, mode_test_list, midrange_test_list):
            y_test.append([tmean, tmed, tmod, tmid])
        print(y_test)

        c = tree.DecisionTreeClassifier()
        c.fit(x_train, x_label)
        objectclass = c.predict(y_test)
        print(objectclass)

        os.chdir(outputDir)

        workbook = xlsxwriter.Workbook("CT_DT_final.xlsx")
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', 'TestImageName', bold)
        worksheet.write('B1', 'ObjectType', bold)

        row = 1
        column = 0

        for l, type in zip(label_test_list, objectclass):
            worksheet.write(row, column, l)
            worksheet.write(row, column + 1, type)
            print("Recognizing, Please Wait!")
            row += 1

        print("Recognition Completed!")
        workbook.close()
        messagebox.showinfo("Recognition", "Recognition successfully Done.")

    elif total_cols == 10:
        x_train = []
        x_label = []
        y_test = []
        for l, mi, q1, med, q3, ma, v, md, s, cov in zip(labelList, minimum_list, q1_list, medianList, q3_list,
                                                         maximum_list, variance_list, mean_deviation_list,
                                                         skewness_list, cov_list):
            x_label.append(l)
            x_train.append([mi, q1, med, q3, ma, v, md, s, cov])

        for tMin, tQ1, tMed, tQ3, tMax, tVar, tMeanDev, tSkewness, tCov in zip(minimum_test_list,
                                                                               q1_test_list, median_test_list,
                                                                               q3_test_list,
                                                                               maximum_test_list,
                                                                               variance_test_list,
                                                                               mean_deviation_test_list,
                                                                               skewness_test_list,
                                                                               cov_test_list):
            y_test.append([tMin, tQ1, tMed, tQ3, tMax, tVar, tMeanDev, tSkewness, tCov])

        c = tree.DecisionTreeClassifier()
        c.fit(x_train, x_label)
        objectclass = c.predict(y_test)
        print(objectclass)
        print(label_test_list)

        os.chdir(outputDir)

        workbook = xlsxwriter.Workbook("DD_DT_final.xlsx")
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', 'TestImageName', bold)
        worksheet.write('B1', 'ObjectType', bold)

        row = 1
        column = 0

        for l, type in zip(label_test_list, objectclass):
            worksheet.write(row, column, l)
            worksheet.write(row, column + 1, type)
            print("Recognizing, Please Wait!")
            row += 1
            print(l)
            print(type)

        print("Recognition Completed!")
        workbook.close()
        messagebox.showinfo("Recognition", "Recognition successfully Done.")

    elif total_cols == 13:
        x_train = []
        x_label = []
        y_test = []
        for l, mean, med, mod, mid, mi, q1, q3, ma, v, md, s, cov in zip(labelList, meanList, medianList, modeList,
                                                                         midrangeList, minimum_list, q1_list,
                                                                         q3_list, maximum_list, variance_list,
                                                                         mean_deviation_list, skewness_list, cov_list):
            x_label.append(l)
            x_train.append([mean, med, mod, mid, mi, q1, q3, ma, v, md, s, cov])

        for tMean, tMed, tMod, tMid, tMin, tQ1, tQ3, tMax, tVar, tMeanDev, tSkewness, tCov in zip(
                mean_test_list, median_test_list, mode_test_list, midrange_test_list,
                minimum_test_list, q1_test_list, q3_test_list, maximum_test_list,variance_test_list,
                mean_deviation_test_list,skewness_test_list, cov_test_list):

            y_test.append([tMean, tMed, tMod, tMid, tMin, tQ1, tQ3, tMax, tVar, tMeanDev, tSkewness, tCov])

        c = tree.DecisionTreeClassifier()
        c.fit(x_train, x_label)
        objectclass = c.predict(y_test)
        print(objectclass)
        print(label_test_list)

        os.chdir(outputDir)

        workbook = xlsxwriter.Workbook("CT_DD_DT_final.xlsx")
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', 'TestImageName', bold)
        worksheet.write('B1', 'ObjectType', bold)

        row = 1
        column = 0

        for l, type in zip(label_test_list, objectclass):
            worksheet.write(row, column, l)
            worksheet.write(row, column + 1, type)
            print("Recognizing, Please Wait!")
            row += 1
            print(l)
            print(type)

        print("Recognition Completed!")
        workbook.close()
        messagebox.showinfo("Recognition", "Recognition successfully Done.")

    else:
        c = tree.DecisionTreeClassifier()

        x_train = []
        x_label = []
        y_test = []
        for l, h in zip(labelList, hist):
            x_train.append(h)
            x_label.append(l)

        for ht in hist_test:
            y_test.append(ht)

        c.fit(x_train, x_label)
        objectclass = c.predict(y_test)
        print(objectclass)
        print(label_test_list)

        os.chdir(outputDir)

        workbook = xlsxwriter.Workbook("LBP_DT_final.xlsx")
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', 'TestImageName', bold)
        worksheet.write('B1', 'ObjectType', bold)

        row = 1
        column = 0

        for l, type in zip(label_test_list, objectclass):
            worksheet.write(row, column, l)
            worksheet.write(row, column + 1, type)
            print("Recognizing, Please Wait!")
            row += 1

        print("Recognition Completed!")
        workbook.close()
        messagebox.showinfo("Recognition", "Recognition successfully Done.")


def main():
    root = tk.Tk()
    root.title("Object Recognition")
    root.geometry("1080x480")

    leftframe = tk.Frame(root, padx=20, pady=20, height=470, width=205)
    leftframe.pack(side='left')

    middleframe = tk.Frame(root, padx=20, pady=20, height=470, width=205)
    middleframe.pack(side='left')

    middleframe2 = tk.Frame(root, padx=20, pady=20, height=470, width=205)
    middleframe2.pack(side='left')

    rightframe = tk.Frame(root, padx=20, pady=20, height=470, width=205)
    rightframe.pack(side='left')

    lti_button = tk.Button(leftframe, text="Load Training images \n(Browse Training Image Folder)", height=3,
                           width=25, padx=10, pady=10, command=load_training_images_onclick)

    ct_button = tk.Button(leftframe, text="Extract CT Feature \nand store in Database", height=3,
                          width=25, padx=10, pady=10, command=extract_ct_feature_onclick)

    dd_button = tk.Button(leftframe, text="Extract DD Feature \nand store in Database", padx=10, pady=10,
                          height=3, width=25, command=extract_dd_feature_onclick)

    ctdd_button = tk.Button(leftframe, text="Extract CT+DD Feature \nand store in Database", padx=10, pady=10,
                            height=3, width=25, command=extract_ctdd_feature_onclick)

    lbp_button = tk.Button(leftframe, text="Extract LBP Feature \nand store in Database", padx=10, pady=10,
                           height=3, width=25, command=extract_lbp_feature_onclick)

    lti_button.pack()
    ct_button.pack()
    dd_button.pack()
    ctdd_button.pack()
    lbp_button.pack()

    lti_button.configure(background='cyan')
    ct_button.configure(background='green')
    dd_button.configure(background='blue')
    ctdd_button.configure(background='yellow')
    lbp_button.configure(background='gray')

    lfd_button = tk.Button(middleframe, text="Load Feature Data \n (Browse Training Feature\n Data File)", height=3,
                           width=25, padx=10, pady=10, command=load_feature_data_onclick)

    lfd_button.pack(side='top')
    lfd_button.configure(background='white')

    lqi_button = tk.Button(middleframe2, text="Load Query Images \n (Browse Query Image Folder)", height=3,
                           width=25, padx=10, pady=10, command=load_query_image_folder_onclick)

    lqi_button.pack(side='top')
    lqi_button.configure(background='white')

    obj_euclidean_button = tk.Button(rightframe, text="Show Object Types \n using Euclidean", height=3,
                                     width=25, padx=10, pady=10, command=euclidean_onclick)

    obj_correlation_button = tk.Button(rightframe, text="Show Object Types \n using Correlation", height=3,
                                       width=25, padx=10, pady=10, command=correlation_onclick)

    obj_decision_tree_button = tk.Button(rightframe, text="Show Object Types \n using Decision Tree", padx=10, pady=10,
                                         height=3, width=25, command=decision_tree_onclick)

    obj_euclidean_button.pack()
    obj_correlation_button.pack()
    obj_decision_tree_button.pack()

    obj_euclidean_button.configure(background='gray')
    ct_button.configure(background='green')
    obj_decision_tree_button.configure(background='blue')

    root.mainloop()


if __name__ == '__main__':
    main()

