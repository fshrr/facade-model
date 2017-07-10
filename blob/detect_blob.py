import cv2
import numpy as np
import os

# setup args... for cmd line

# Open a directory in os

dir = ""

# for every image, detect blobs
i = 0
for image in ...
    im = cv2.imread("".png, cv2.IMREAD_GREYSCALE)

    detector = cv2.SimpleBlobDetector()
    win_points = detector.detect(im)

    # Draw image with win_points
    im_points = cv2.drawKeypoints(im, win_points, np.array([]), (0,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imwrite("" + str(i), im_points)
    # Save points in a txt file
    
    with open("points_" + str(i) + ".txt", "w") as f:
        for _ in win_points:
	    f.write("" + "\n")
    
    
        
