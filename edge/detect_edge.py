import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage import io
from skimage.color import rgb2gray
from skimage import feature
from skimage.filters import roberts, sobel, scharr, prewitt
import scipy.misc
import os

def return_input_folder_location():
    """
    Return the input folder location. If "input_images" does not exist in the
    parent folder of the edge folder, then ask the user for an input folder.
    Else, return the input folder absolute path of the input_images folder.
    """
    os.chdir("..")
    input_dir = os.getcwd() + "/input_images"
    if not os.path.exists(input_dir):
        input_dir = os.filedialog.askfilenamedirectory()
        return input_dir
    else:
        os.chdir("input_images")
        input_dir = os.getcwd()
        return input_dir

def create_intermediate_folder():
    cwd = os.getcwd()
    mid_dir = cwd + "/mid"
    if not os.path.exists(mid_dir):
        os.makedirs(mid_dir)

def detect_edges(input_dir, method=6, sigma=2):
    """
    Detect edges using an edge detection method.
    The default method is prewitt.

    1. Default skimage Canny
    2. Canny w/ sigma=2
    3. Roberts
    4. Sobel
    5. Scharr
    6. Prewitt

    Note that Prewitt is default because it currently works best with facades.

    @params input_dir : String
    @params method : int
    @params sigma : float or int
    """
    images = os.listdir(input_dir)

    def edge_method(method_num, im, sigma=2):
        return {
            1:feature.canny(im),
            2:feature.canny(im, sigma=2),
            3:roberts(im),
            4:sobel(im),
            5:scharr(im),
            6:prewitt(im)
        }

    for image in images:
        image_name = image.split(".")[0]
        im = rgb2gray(io.imread(input_dir + "/" + image))

        if method is int and 1 <= method <=6:
            scipy.misc.imsave(mid_dir + "/" + image_name + '.png', edge_method(6,im,sigma))

if __name__ == "__main__":
    create_intermediate_folder()
    input_folder_location = return_input_folder_location()
    detect_edges(input_folder_location)
