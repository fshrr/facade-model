#from KittiSeg import run_segmentation
from floodfill import floodfill
from edge import detect_edge
from blob import detect_blob
import os
from appJar import gui
import time

def run_app(app_win_width=0.05, app_win_length=0.05, min_ignore=0.0, max_ignore=255.0):

    # run segmentation


    # run edge detection
    detect_edge.main()
    print("end of edge script!" + os.getcwd())

    # run blob detection

    detect_blob.main()
    print("end of blob script!" + os.getcwd())

    # run floodfill (and convex hull / approximate polygon)

    floodfill.main(min_ignore,max_ignore)
    print("end of floodfill script!" + os.getcwd())

# handle button events
def press(button):
    if button == "Cancel":
        app.stop()
    else:
        app_win_width = app.getEntry("Approx. Proportion of Window Width: ")
        app_win_length = app.getEntry("Approx. Proportion of Window Length: ")
        min_ignore = app.getEntry("Min bound for Pixel Value to Ignore: ")
        max_ignore = app.getEntry("Max bound for Pixel Value to Ignore: ")
        norm_dev_blob = app.getEntry("Standard Deviation for Blob Size: ")
        thr_blob = app.getEntry("Threshold for Blob Detection: ")
        max_width_flood = app.getEntry("Max Window Width Proportion for FloodFilling: ")
        max_length_flood = app.getEntry("Max Window Length Proportion for FloodFilling: ")
        edge_num = app.getEntry("Edge Detection Method Number: ")
        canny_sigma = app.getEntry("OPTIONAL: Deviation (Edge Detection Method Number = 2): ")

        if check_param(app_win_width, app_win_length, min_ignore, max_ignore,
            norm_dev_blob, thr_blob, max_width_flood, max_length_flood, edge_num, canny_sigma):
            print("run app!")
            app.disableButton("Submit")
            # start running the app

            run_app(app_win_width, app_win_length, min_ignore, max_ignore)

            #re-enable after app has run
            app.enableButton("Submit")
        else:
            app.errorBox("Error!", "Try again, check the following preconditions: \n" +
                "Approx. Proportion of Window Width must be between 0 and 1:" + str(app_win_width) + " \n" +
                "Approx. Proportion of Window Length must be between 0 and 1:" + str(app_win_length) + " \n" +
                "Min bound for Pixel Value to Ignore must be between 0 <= x < 255: " + str(min_ignore) + "\n" +
                "Max bound for Pixel Value to Ignore must be between 0 < x <= 255: " + str(max_ignore) + "\n" +
                "Standard Deviation for Blob Size: " + "default: 0.25 rule: 0 <= x <= 1" + "\n" +
                "Threshold for Blob Detection: " + "default: 0.075 rule: 0 <= x <= 1, lower detects smaller" + "\n" +
                "Max Window Width Proportion for FloodFilling: " + "default: 0.25 rule: 0 < x <= 1" + "\n" +
                "Max Window Length Proportion for FloodFilling: " + "default: 0.25 rule: 0 < x <= 1" + "\n" +
                "Edge Detection Method Number: " + "default: 6.0 rule: canny=1, canny_sigma=2, roberts=3, sobel=4, scharr=5, prewitt=6" + "\n" +
                "OPTIONAL: Deviation (Edge Detection Method Number = 2)" + "default: 2 rule: x >= 0" + "\n")

def check_param(app_win_width, app_win_length, min_ignore, max_ignore,
    norm_dev_blob, thr_blob, max_width_flood, max_length_flood, edge_num, canny_sigma):
    if not 0.0 < app_win_width <= 1.0:
        return False
    if not 0.0 < app_win_length <= 1.0:
        return False
    if not 0.0 <= min_ignore < 255.0:
        return False
    if not 0.0 < max_ignore <= 255.0:
        return False
    if not 0 <= norm_dev_blob <= 1:
        return False
    if not 0 <= thr_blob <= 1:
        return False
    if not 0 < max_width_flood <= 1:
        return False
    if not 0 < max_length_flood <= 1:
        return False
    if not 1 <= edge_num <= 6:
        return False
    if not 0 <= canny_sigma:
        return False
    else: # Param satisfy preconditions for scripts
        return True

def setDefault(button):
    app.setEntry("Approx. Proportion of Window Width: ",0.05)
    app.setEntry("Approx. Proportion of Window Length: ",0.05)
    app.setEntry("Min bound for Pixel Value to Ignore: ",0.0)
    app.setEntry("Max bound for Pixel Value to Ignore: ",255.0)
    app.setEntry("Standard Deviation for Blob Size: ",0.25)
    app.setEntry("Threshold for Blob Detection: ",0.075)
    app.setEntry("Max Window Width Proportion for FloodFilling: ",0.25)
    app.setEntry("Max Window Length Proportion for FloodFilling: ",0.25)
    app.setEntry("Edge Detection Method Number: ",6.0)
    app.setEntry("OPTIONAL: Deviation (Edge Detection Method Number = 2): ",2)

def setup_gui(app):

    # create a GUI variable called app
    app.setResizable(canResize=True)
    app.setBg("white")
    app.setFont(14, "arial")

    # add & configure widgets - widgets get a name, to help referencing them later
    app.addLabel("title", "Window Segmentation and Shape Approximation")
    app.setLabelBg("title", "white")
    app.setLabelFg("title", "black")

    app.addLabelNumericEntry("Approx. Proportion of Window Width: ")
    app.addLabelNumericEntry("Approx. Proportion of Window Length: ")
    app.addLabelNumericEntry("Min bound for Pixel Value to Ignore: ")
    app.addLabelNumericEntry("Max bound for Pixel Value to Ignore: ")
    app.addLabelNumericEntry("Standard Deviation for Blob Size: ")
    app.addLabelNumericEntry("Threshold for Blob Detection: ")
    app.addLabelNumericEntry("Max Window Width Proportion for FloodFilling: ")
    app.addLabelNumericEntry("Max Window Length Proportion for FloodFilling: ")
    app.addLabelNumericEntry("Edge Detection Method Number: ")
    app.addLabelNumericEntry("OPTIONAL: Deviation (Edge Detection Method Number = 2): ")

    app.setEntryDefault("Approx. Proportion of Window Width: ","default: 0.05 rule: 0 <= x <= 1")
    app.setEntryDefault("Approx. Proportion of Window Length: ","default: 0.05 rule: 0 <= x <= 1")
    app.setEntryDefault("Min bound for Pixel Value to Ignore: ","default: 0.0 rule: 0 <= x < 255")
    app.setEntryDefault("Max bound for Pixel Value to Ignore: ","default: 255.0 rule: 0 < x <= 255")
    app.setEntryDefault("Standard Deviation for Blob Size: ","default: 0.25 rule: 0 <= x <= 1")
    app.setEntryDefault("Threshold for Blob Detection: ","default: 0.075 rule: 0 <= x <= 1, lower detects smaller")
    app.setEntryDefault("Max Window Width Proportion for FloodFilling: ","default: 0.25 rule: 0 < x <= 1")
    app.setEntryDefault("Max Window Length Proportion for FloodFilling: ","default: 0.25 rule: 0 < x <= 1")
    app.setEntryDefault("Edge Detection Method Number: ", "default: 6.0 rule: canny=1, canny_sigma=2, roberts=3, sobel=4, scharr=5, prewitt=6")
    app.setEntryDefault("OPTIONAL: Deviation (Edge Detection Method Number = 2): ", "default: 2 rule: x >= 0")

    # link the buttons to the function called press
    app.addButtons(["Submit", "Cancel"], press)
    app.addButtons(["Default"], setDefault)

if __name__ == "__main__":

    app = gui("Login Window", "1280x720")
    setup_gui(app)
    # start the GUI
    text = "Window Segmentation and Shape Approximation"
    app.showSplash(text, fill='white', stripe='black', fg='white', font=44)
    app.go()
