# Preprocess.py

import cv2
import numpy as np
import math

# Module level variables ##########################################################################
GAUSSIAN_FILTER_SIZE = (5, 5)
ADAPTIVE_THRESH_BLOCK_SIZE = 19
ADAPTIVE_THRESH_WEIGHT = 9

###################################################################################################

#Function that does the preprocessing
def preprocess(imgOriginal):
    #el preprocessing fel ANPL, bybd2 b 5twat t2reban sabta
    #l image btt7awel l grayscale, bnzwed el contrasr, bn3ml averaging mask ye3ml blurr,
    #and lastly bn3ml threshold lel image, y3ne btt7awel binary, b7es l pixel ta5ud ya 0 ya 1 as values

    imgGrayscale = extractValue(imgOriginal)

    imgMaxContrastGrayscale = maximizeContrast(imgGrayscale)
    height, width = imgGrayscale.shape
    imgBlurred = np.zeros((height, width, 1), np.uint8)
    imgBlurred = cv2.GaussianBlur(imgMaxContrastGrayscale, GAUSSIAN_FILTER_SIZE, 0)
    imgThresh = cv2.adaptiveThreshold(imgBlurred, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)

    #return image in gray scale, and thresholded
    return imgGrayscale, imgThresh
# end function

###################################################################################################


def extractValue(imgOriginal):

    #bn-extract m3lumat zy e height wel width w 3dd el channels
    height, width, numChannels = imgOriginal.shape
    #bn3ml intianlization,zy array of el height wel width, w kol pixel leha 3dd el channels l gebnnaah foo2
    imgHSV = np.zeros((height, width, numChannels), np.uint8)

    #bn7awel el color format BGR lel HSV w dh feeh 3 channels (hue, saturation, value)
    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

    #b3den bnfsel el 3 channles el fato dool 3an b3d, w nrg3 channel el value
    imgHue, imgSaturation, imgValue = cv2.split(imgHSV)
    return imgValue
# end function


def maximizeContrast(imgGrayscale):
    #bn-extract m3lumat zy el height wel width
    height, width = imgGrayscale.shape

    #initialization, array of height, width, pizel is only one channel, all zeroes
    imgTopHat = np.zeros((height, width, 1), np.uint8)
    imgBlackHat = np.zeros((height, width, 1), np.uint8)

    #Before doing any morphological transformations, lazm n n7aded el structuring element
    #here 7dednah b rectangle
    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    #el top hat : difference between an input image and its opening
    #el black hat:  difference between the closing and its input image
    #More info here:https://docs.opencv.org/2.4/doc/tutorials/imgproc/opening_closing_hats/opening_closing_hats.html
    imgTopHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_TOPHAT, structuringElement)
    imgBlackHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_BLACKHAT, structuringElement)

    #Hena bngama3 el input image el fel grayscale, + el tophat, then  - el Blackhat
    imgGrayscalePlusTopHat = cv2.add(imgGrayscale, imgTopHat)
    imgGrayscalePlusTopHatMinusBlackHat = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)

    return imgGrayscalePlusTopHatMinusBlackHat
# end function










