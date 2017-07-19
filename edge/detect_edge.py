import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage import io
from skimage.color import rgb2gray
from skimage import feature
from skimage.filters import roberts, sobel, scharr, prewitt
import scipy.misc
import os

cwd = os.getcwd()
input_dir = cwd + "/in"
if not os.path.exists(input_dir):
    input_dir = os.filedialog.askfilenamedirectory()

mid_dir = cwd + "/mid"
if not os.path.exists(mid_dir):
    os.makedirs(mid_dir)
    
images = os.listdir(input_dir)

for image in images:
    image_name = image.split(".")[0]
    im = rgb2gray(io.imread(input_dir + "/" + image))

    #edges1 = feature.canny(im)
    edges2 = feature.canny(im, sigma=2)
    #edges3 = roberts(im)
    #edges4 = sobel(im)
    #edges5 = scharr(im)
    #edges6 = prewitt(im)

    scipy.misc.imsave(mid_dir + "/" + image_name + '.png', edges2)
 
"""
fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(nrows=1, ncols=6, figsize=(10,5),
                                    sharex=True, sharey=True)

ax1.imshow(edges1, cmap=plt.cm.gray)
ax1.axis('off')
ax1.set_title('default sigma', fontsize=20)

ax2.imshow(edges2, cmap=plt.cm.gray)
ax2.axis('off')
ax2.set_title('$\sigma=3$', fontsize=20)

ax3.imshow(edges3, cmap=plt.cm.gray)
ax3.axis('off')
ax3.set_title('Roberts', fontsize=20)

ax4.imshow(edges3, cmap=plt.cm.gray)
ax4.axis('off')
ax4.set_title('Sobel', fontsize=20)

ax5.imshow(edges3, cmap=plt.cm.gray)
ax5.axis('off')
ax5.set_title('Scharr', fontsize=20)

ax6.imshow(edges3, cmap=plt.cm.gray)
ax6.axis('off')
ax6.set_title('Prewitt', fontsize=20)

fig.tight_layout()
"""

#plt.show()


