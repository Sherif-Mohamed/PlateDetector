# DetectPlates.py

import cv2
import numpy as np
import math
import Main
import random

import Preprocess
import DetectChars
import PossiblePlate
import PossibleChar

# module level variables
PLATE_WIDTH_PADDING_FACTOR = 1.3
PLATE_HEIGHT_PADDING_FACTOR = 1.5

###################################################################################################
def detect_plate(imgOriginalScene):
    possible_plates = []                   # this will be the return value

    # extracint values, like height, width, and number of hannels
    height, width, numChannels = imgOriginalScene.shape

    # Initialization
    GrayscaleScene = np.zeros((height, width, 1), np.uint8)
    ThreshScene = np.zeros((height, width, 1), np.uint8)
    imgContours = np.zeros((height, width, 3), np.uint8)

    cv2.destroyAllWindows()

    #First, calling the preprocess function
    GrayscaleScene, ThreshScene = Preprocess.preprocess(imgOriginalScene)



    # find all possible chars in the scene,
    # this function first finds all contours, then only includes contours that could be chars (without comparison to other chars yet)
    listOfPossibleCharsInScene = find_char(ThreshScene)
    #After this function returns we have a list of contous that are possibile to be characters.


    # This function find groups of matching chars
    # in the next steps each group of matching chars will attempt to be recognized as a plate
    listOfListsOfMatchingCharsInScene = DetectChars.findListOfListsOfMatchingChars(listOfPossibleCharsInScene)


    #For each group, extract the plate
    for listOfMatchingChars in listOfListsOfMatchingCharsInScene:
        possiblePlate = plate_extraction(imgOriginalScene, listOfMatchingChars)

        #if plate is foun, add it to the list
        if possiblePlate.imgPlate is not None:
            possible_plates.append(possiblePlate)


    return possible_plates
###################################################################################################

#This function finds possible characters using contours
def find_char(imgThresh):
    listOfPossibleChars = []
    intCountOfPossibleChars = 0

    #Creating a copy of the thresholded image
    imgThreshCopy = imgThresh.copy()

    #The following finds all the contours.
    #To remember contours: https://docs.opencv.org/3.1.0/d4/d73/tutorial_py_contours_begin.html
    imgContours, contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    #get height and width of  the thresholded image
    height, width = imgThresh.shape
    #intializing
    imgContours = np.zeros((height, width, 3), np.uint8)

    #loop i from 0 to the number of contours(contours is a list containing the contour's information in each entry, so we get it's length)
    for i in range(0, len(contours)):

        #refer to the file PossibleChar.py
        #it's constructor takes the contour
        possibleChar = PossibleChar.PossibleChar(contours[i])

        #check if the a contour is a possible character.
        if DetectChars.checkIfPossibleChar(possibleChar):
            #increment count
            intCountOfPossibleChars = intCountOfPossibleChars + 1

            #add to list of possible chars
            listOfPossibleChars.append(possibleChar)

    #When the loop finishes we have a list with all contours having a possibility of being a character.
    return listOfPossibleChars
# end function


###################################################################################################
def plate_extraction (imgOriginal, listOfMatchingChars):
    possiblePlate = PossiblePlate.PossiblePlate()           # this will be the return value

    # Sort chars from left to right, according to their X position
    listOfMatchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)

    # calculate the center point of the plate
    fltPlateCenterX = (listOfMatchingChars[0].intCenterX + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterX) / 2.0
    fltPlateCenterY = (listOfMatchingChars[0].intCenterY + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY) / 2.0

    ptPlateCenter = fltPlateCenterX, fltPlateCenterY

    # calculate plate width and height
    intPlateWidth = int((listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectX + listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectWidth - listOfMatchingChars[0].intBoundingRectX) * PLATE_WIDTH_PADDING_FACTOR)

    intTotalOfCharHeights = 0

    for matchingChar in listOfMatchingChars:
        intTotalOfCharHeights = intTotalOfCharHeights + matchingChar.intBoundingRectHeight
    # end for

    fltAverageCharHeight = intTotalOfCharHeights / len(listOfMatchingChars)

    intPlateHeight = int(fltAverageCharHeight * PLATE_HEIGHT_PADDING_FACTOR)

            # calculate correction angle of plate region
    fltOpposite = listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY - listOfMatchingChars[0].intCenterY
    fltHypotenuse = DetectChars.distanceBetweenChars(listOfMatchingChars[0], listOfMatchingChars[len(listOfMatchingChars) - 1])
    fltCorrectionAngleInRad = math.asin(fltOpposite / fltHypotenuse)
    fltCorrectionAngleInDeg = fltCorrectionAngleInRad * (180.0 / math.pi)

    # pack plate region center point, width and height, and correction angle into rotated rect member variable of plate
    possiblePlate.rrLocationOfPlateInScene = ( tuple(ptPlateCenter), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg )

    # final steps are to perform the actual rotation

    # get the rotation matrix for our calculated correction angle
    rotationMatrix = cv2.getRotationMatrix2D(tuple(ptPlateCenter), fltCorrectionAngleInDeg, 1.0)

    height, width, numChannels = imgOriginal.shape      # unpack original image width and height

    imgRotated = cv2.warpAffine(imgOriginal, rotationMatrix, (width, height))       # rotate the entire image

    imgCropped = cv2.getRectSubPix(imgRotated, (intPlateWidth, intPlateHeight), tuple(ptPlateCenter))

    # copy the cropped plate image into the applicable member variable of the possible plate
    possiblePlate.imgPlate = imgCropped

    return possiblePlate
# end function












