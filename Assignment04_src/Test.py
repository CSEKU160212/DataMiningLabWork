import numpy as np
from skimage import io, color
from skimage.feature import local_binary_pattern
from scipy.spatial.distance import euclidean
import os

def lbp_histogram(color_image):
    img = color.rgb2gray(color_image)
    patterns = local_binary_pattern(img, 8, 1)
    hist, _ = np.histogram(patterns, bins=np.arange(2**8 + 1), density=True)
    return hist

os.chdir('/home/cseku160212/PycharmProjects/DataMining/ZuBuD/png-ZuBuD')
each = 'object0001.view03.png'
couscous = io.imread(each)
knitwear = io.imread('object0001.view04.png')
unknown = io.imread('object0001.view05.png')

couscous_feats = lbp_histogram(couscous)
knitwear_feats = lbp_histogram(knitwear)
unknown_feats = lbp_histogram(unknown)

print(euclidean(unknown_feats, couscous_feats))

print(euclidean(unknown_feats, knitwear_feats))
