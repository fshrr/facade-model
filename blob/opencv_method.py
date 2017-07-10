# Standard imports
import cv2
import numpy as np
 
# Read image
im = cv2.imread("blob.png", cv2.IMREAD_GRAYSCALE)

# Set parameters
params = cv2.SimpleBlobDetector_Params()
"""
# Color
params.filterByColor = True
params.blobColor = 50

# Change thresholds
params.minThreshold = 150
params.maxThreshold = 200
"""
# Filter by Area.
params.filterByArea = True
params.minArea = 400
"""
# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.01
"""
# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.001
"""
# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01
"""

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create(params)
   
# Detect blobs.
keypoints = detector.detect(im)
    
# Draw detected blobs as red circle
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
     
# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
try:
    print(keypoints)
    print(keypoints[0].pt)
except:
    print("no points")
    

cv2.waitKey(0)
