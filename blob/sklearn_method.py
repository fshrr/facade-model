from math import sqrt, pi
from skimage import io
from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import os
from tkinter import filedialog

#example of image cropping
#image = data.hubble_deep_field()[0:500, 0:500]
filename = "tmp"
im_format = ".png"

image = io.imread("tmp.png")
image_gray = rgb2gray(image)
width, length = image.shape[0:2]

# Default ranges of window sizes (hyperparameters)
w_ratio = 0.1
l_ratio = 1/10
dev = 0.25 #average deviance ratio of radius
thr = 0.075

avg_area = ( width * w_ratio ) * ( length * l_ratio )
avg_radius = sqrt( avg_area / pi )
avg_dev = avg_radius * dev

min_sigma = (avg_radius - avg_dev) / sqrt(2)
max_sigma = (avg_radius + avg_dev) / sqrt(2)

blobs_log = blob_log(image_gray, min_sigma=min_sigma, max_sigma=max_sigma, num_sigma=10, threshold=thr)

# Compute radii in the 3rd column.
blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)

"""
blobs_dog = blob_dog(image_gray, min_sigma=min_sigma, max_sigma=max_sigma, threshold=.005)
blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)

blobs_doh = blob_doh(image_gray, min_sigma=2min_sigma, max_sigma=max_sigma, num_sigma=10, threshold=.005)
"""

# blobs_list = [blobs_log, blobs_dog, blobs_doh]
blobs_list = [blobs_log]
colors = ['yellow', 'lime', 'red']
titles = ['Laplacian of Gaussian', 'Difference of Gaussian',
          'Determinant of Hessian']


sequence = zip(blobs_list, colors, titles)

fig, axes = plt.subplots(1, 3, figsize=(9, 3), sharex=True, sharey=True,
                        subplot_kw={'adjustable': 'box-forced'})

#fig, axes = plt.subplots(1, 1, figsize=(9, 3), sharex=True, sharey=True,
#                         subplot_kw={'adjustable': 'box-forced'})

ax = axes.ravel()

for idx, (blobs, color, title) in enumerate(sequence):
    ax[idx].set_title(title)
    ax[idx].imshow(image, interpolation='nearest')
    for blob in blobs:
        y, x, r = blob
        c = plt.Circle((x, y), r, color=color, linewidth=2, fill=False)
        ax[idx].add_patch(c)
    ax[idx].set_axis_off()

plt.tight_layout()
#plt.show()

# Define directory and make output dirs
defined = True
if defined:
    directory = "C:/Users/kevin/Desktop/projects/3d-facade-model/blob"
else: #not defined
    directory = filedialog.askdirectory()
    
new_dir = directory + "/out"
im_dir = new_dir + "/image"
loc_dir = new_dir + "/location"
if not os.path.exists(new_dir):
    os.mkdir(new_dir)
    if not os.path.exists(im_dir):
        os.mkdir(im_dir)
    if not os.path.exists(loc_dir):
        os.mkdir(loc_dir)

with open(loc_dir + "/" + filename + ".txt", "w") as file:
    for blob in blobs_log:   
        file.write(str(blob[0]/width) + " " + str(blob[1]/length) + " " + str(blob[2]) + "\n")

plt.savefig(im_dir + "/" + filename + im_format, bbox_inches='tight')

