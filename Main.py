# Main.py

import os
import tkFileDialog
from Tkinter import *

import cv2

import DetectChars
import DetectPlates

# module level variables ##########################################################################
BLACK = (0.0, 0.0, 0.0)
WHITE = (255.0, 255.0, 255.0)
YELLOW = (0.0, 255.0, 255.0)
GREEN = (0.0, 255.0, 0.0)
RED = (0.0, 0.0, 255.0)


###################################################################################################
class UI(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self, parent)

        self.initUI()

    def initUI(self):
        self.master.title("Car plate detector")
        self.pack(fill=BOTH, expand=FALSE)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=15)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=15)

        lbl = Label(self, text='Car Plate detector', padx=60, pady=30, font=("Courier", 28))
        lbl.grid(pady=4, row=0, column=0, padx=5, columnspan=4)

        area = Text(self)
        area.insert(INSERT, 'Results:\n')
        area['state'] = DISABLED
        area.grid(row=1, column=0, columnspan=2, rowspan=4,
                  padx=5, sticky=E + W + S + N)
        self.area = area

        chooseButton = Button(self, activebackground='green', width=12, text='Choose photo',
                              command=choosePhotoCallback,
                              anchor=CENTER)
        chooseButton.grid(row=1, column=3)
        self.chooseButton = chooseButton

        closeButton = Button(self, activebackground='red', width=12, text='Close', command=closeApp, anchor=CENTER)
        closeButton.grid(row=2, column=3, pady=4)


############################################################################################################
def main():
    # Initialize tkinter to show GUI
    global app
    app = UI()



    KNNTraining_Sucessful = DetectChars.KNN_load_train()

    # If the training failed
    if not KNNTraining_Sucessful:
        # Print the error message in the System message section in the GUI application.
        # Error is due to failure in training the KNN
        ###########################################################
        ###########################################################
        appendText("Error: Training has failed \n")
        ###########################################################
        ###########################################################
        app.chooseButton.config(state=DISABLED)
        # Exit the main function, thus terminating the program
        return

    # add the GUI to the main looper
    app.mainloop()
    return


# end main

def choosePhotoCallback():
    path = tkFileDialog.askopenfilename(filetypes=[("Image File", '.jpg')])
    processPicture(path)


def closeApp():
    app.quit()


def appendText(text):
    app.area.config(state=NORMAL)
    app.area.insert(INSERT, text)
    app.area.config(state=DISABLED)


def processPicture(path):
    # Load the Image
    # el satr dh bydelo esm el sora, bel extension, el GUI lazm y supply esm el sora bel extension bardu.
    # cv2.imread(file name with extension)
    ##################################################################
    ##################################################################
    img_orig = cv2.imread(path)
    ##################################################################
    ##################################################################

    # If the image failed to load
    if img_orig is None:
        # Print the error message in the System message section in the GUI application.
        # Error is due to failure in loading the image, be it for any reason.
        ##############################################################
        ##############################################################
        appendText(" Error: Image failed to load \n")
        ##############################################################
        ##############################################################

        # Exit the main function, thus terminating the program.
        os.system("pause")
        return

    # Detect plates, then characters in that plate.
    possible_plates = DetectPlates.detect_plate(img_orig)
    # When thi function returns, we will have a list of all possible pplates, Now we pass that list to another function
    # That will detect chars in a certaon plate, refer to DetectChars.py File
    possible_plates = DetectChars.detect_PlateChar(possible_plates)

    # f there was no plate found
    if len(possible_plates) == 0:

        # Print the error message in the System message section in the GUI application.
        # Error is due to Failure in finding any Number Plates.
        #############################################################
        #############################################################
        appendText("No Plates has been found \n")
        #############################################################
        #############################################################


    # If Plates were found
    else:

        # Sort the plates in descending order, according to which one have the greatest number or characters.
        possible_plates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)

        # Assuming in the plate el sa7 hya aktr w7da feha charactrs detected.
        licPlate = possible_plates[0]

        # Print Result in the result section in the GUI application.
        # This line Prints the result 3la tool
        #########################################################################
        #########################################################################
        appendText('Licence plate found: ' + licPlate.strChars + '\n')
        #########################################################################
        #########################################################################

        # The folowing loop, bt-print all other possible results, law 3yzha tt7at eshta law mesh 3ayez bardu eshta, mesh 3aref leha lazma awy wla la
        #########################################################################
        #########################################################################
        # i = 1
        # while i < len(possible_plates):
        #  print(possible_plates[i].strChars)
        # i = i + 1
        #########################################################################
        #########################################################################

        # Show the original image, and the cropped licence plate
        # cv2.imshow("Original Image", img_orig)
        cv2.imshow("Extracted plate", licPlate.imgPlate)

        # Close the opened windows if a key is pressed.
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return


# end processPicture
###################################################################################################
if __name__ == "__main__":
    main()
