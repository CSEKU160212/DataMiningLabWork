from scipy.stats import itemfreq
import os
import cv2

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from scipy import stats
import pandas as pd
from skimage import io, color
from skimage.feature import local_binary_pattern

testimages = []
training_folder_path = filedialog.askdirectory()
os.chdir(training_folder_path)
testimages = sorted(os.listdir("."))
#Code For LBP

for i in range(len(testimages)):
        image=testimages[i]
        im = cv2.imread(image)
        radius = 1
        no_points = 8 * radius
        # uniform LBP is Used
        lbp = local_binary_pattern(im, no_points, radius, method='uniform')
        x = itemfreq(lbp.ravel())
        # Normalize the histogram
        hist = x[:, 1] / sum(x[:, 1])
        x_train.append(hist)
