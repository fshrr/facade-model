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

    @return the input_images path
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
    """
    Create a intermediate folder in the current working directory if none
    exists and return it.

    @return the intermediate directory path
    """
    cwd = os.getcwd()
    mid_dir = cwd + "/mid"
    if not os.path.exists(mid_dir):
        os.makedirs(mid_dir)
    return mid_dir

def create_output_edge_image_folder(image_list, output_dir):
    """
    Create image folders in the edge_images folder.

    @params image_list a list of image names
    @params output_dir the output directory
    """
    new_image_dir = output_dir
    for image in image_list:
        new_image_dir = output_dir + "/" + image.split(".")[0]
        if not os.path.exists(new_image_dir):
            os.mkdir(new_image_dir)

def create_edge_images_folder():
    """
    Create the edge_images folder in the parent directory if not exists.

    @return the path to edge_images
    """
    cwd = os.getcwd()
    os.chdir("..")
    parent_folder = os.getcwd()
    os.chdir(cwd)
    if not os.path.exists(parent_folder + "/edge_images"):
        os.mkdir(parent_folder + "/edge_images")
    return parent_folder + "/edge_images"

def detect_edges(input_dir, mid_dir, method=6, sigma=2):
    """
    Detect edges using an edge detection method and save it to the intermediate
    folder. The default method is prewitt.

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
        print("reached")
        return {
            1:feature.canny(im),
            2:feature.canny(im, sigma=2),
            3:roberts(im),
            4:sobel(im),
            5:scharr(im),
            6:prewitt(im)
        }[method_num]

    edge_images_folder = create_edge_images_folder()
    create_output_edge_image_folder(images,edge_images_folder)

    for image in images:
        image_name = image.split(".")[0]
        im = rgb2gray(io.imread(input_dir + "/" + image))
        print(isinstance(method, int))
        if isinstance(method, int) and 1 <= method <=6:
            edge_im = edge_method(6,im,sigma)
            scipy.misc.imsave(mid_dir + "/" + image_name + '.png', edge_im)
            scipy.misc.imsave(edge_images_folder + "/" + image_name + "/" + image_name + '.png', edge_im)

if __name__ == "__main__":
    intermediate_folder = create_intermediate_folder()
    input_folder_location = return_input_folder_location()
    detect_edges(input_folder_location, intermediate_folder)
