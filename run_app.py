#from KittiSeg import run_segmentation
from floodfill import floodfill
from edge import detect_edge
from blob import detect_blob
import os

#import pygame
# open settings.txt

#with open("settings.txt") as f:
# should we just do gui using pygame and have txt input boxes?



# run segmentation



# run edge detection

detect_edge.main()
print("end of edge script!" + os.getcwd())

# run blob detection

detect_blob.main()
print("end of blob script!" + os.getcwd())

# run floodfill (and convex hull / approximate polygon)

floodfill.main(20,255)
print("end of floodfill script!" + os.getcwd())

# display gui?

#
#print("end of script!" + os.getcwd())
