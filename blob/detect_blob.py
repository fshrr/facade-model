from math import sqrt, pi
from skimage import io
from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import os
from tkinter import filedialog
from shutil import move

def create_out_folder_cwd():
    """
    Make an out folder in the current directory and /out/image and
    /out/locations folders.
    """
    cwd = os.getcwd()
    new_dir = cwd + "/out"
    im_dir = new_dir + "/image"
    loc_dir = new_dir + "/location"
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
        if not os.path.exists(im_dir):
            os.mkdir(im_dir)
        if not os.path.exists(loc_dir):
            os.mkdir(loc_dir)

def create_image_points_folder():
    """
    Create an image_points folder in the parent directory if not existing and
    return its absolute path.
    """
    cwd = os.getcwd()
    os.chdir("..")
    parent_folder = os.getcwd()
    os.chdir(cwd)
    if not os.path.exists(parent_folder + "/image_points"):
        os.mkdir(parent_folder + "/image_points")
    return parent_folder + "/image_points"

def check_image(image_list):
    """
    Check if the image is a png. If not, remove it from the image_list.

    @params image_list list of string image names
    """
    for image in image_list[:]:
        if image.split(".")[-1] != "png":
            image_list.remove(image)

def find_images(image_directory):
    """
    Return a list of image file names in a directory of images.

    @params image_directory path to image directory
    @return the list of image file names
    """
    im_list = os.listdir(image_directory)
    print(im_list)
    check_image(im_list)
    return im_list

def process_all_images(image_list, img_dir, output_dir, w_ratio=0.05, l_ratio=0.05, dev=0.25, thr=0.075):
    """
    Saves a list of x,y,radius points in a text file in the current directory
    /out/locations and ../image_points folders.

    NOTE THAT IMAGES with "_raw" WILL BE REMOVED!

    @params image_list a list of image names
    @params img_dir path to image directories
    @params output_dir path to /out folder in cwd
    @params w_ratio the ratio of the minimum window width to image width
    @params l_ratio the ratio of the minimum window length to image length
    @params dev the standard deviation of window size
    @params thr the threshold at which a blob is detected

    Please read the skimage blob_log function for details of the optional parameters.
    """
    image_points_folder = create_image_points_folder()
    for image_file in image_list:
        image_loc = img_dir + "/" + image_file
        image = io.imread(image_loc)
        image_gray = rgb2gray(image)

        width, length = image.shape[0:2]
        avg_area = ( width * w_ratio ) * ( length * l_ratio )
        avg_radius = sqrt( avg_area / pi )
        avg_dev = avg_radius * dev

        min_sigma = (avg_radius - avg_dev) / sqrt(2)
        max_sigma = (avg_radius + avg_dev) / sqrt(2)

        blobs_log = blob_log(image_gray, min_sigma=min_sigma, max_sigma=max_sigma, num_sigma=10, threshold=thr)
        blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)

        loc_dir = os.getcwd() + "/out/location"
        # make a txt file in /out/location
        with open(loc_dir + "/" + image_file.split(".png")[0] + ".txt", "w") as file:
            for blob in blobs_log:
                file.write(str(blob[0]) + " " + str(blob[1]) + " " + str(blob[2]) + "\n")

        name_without_png = image_file.split(".png")[0]
        name_without_raw = name_without_png.split("_raw")[0]

        with open(image_points_folder + "/" + name_without_raw + ".txt", "w") as file:
            for blob in blobs_log:
                file.write(str(blob[0]) + " " + str(blob[1]) + " " + str(blob[2]) + "\n")

        save_plot([blobs_log], image_file, image)

def process_all_images_of_in_folder(input_dir, output_dir, w_ratio=0.05, l_ratio=0.05, dev=0.25, thr=0.075):
    """
    Processes all images of the input folder input_dir and outputs them in output_dir.
    Precondition: input_dir only contains folders.

    @params image_list a list of image names
    @params img_dir path to image directories
    @params output_dir path to /out folder in cwd
    @params w_ratio the ratio of the minimum window width to image width
    @params l_ratio the ratio of the minimum window length to image length
    @params dev the standard deviation of window size
    @params thr the threshold at which a blob is detected
    """
    subdirs = os.listdir(input_dir)
    for folder_name in subdirs:
        print(subdirs)
        img_dir = input_dir + "/" + folder_name
        img_list = find_images(img_dir)
        image_to_ndarray = process_all_images(img_list, img_dir, output_dir, w_ratio, l_ratio, dev, thr)

def save_plot(blobs_list, image_file, image):
    """
    Saves images with circles around detected blob centers inside the
    /out/image folder of the current working directory.

    @params blobs_list a list of blob points
    @params image_file the image file name
    @params image the image ndarray
    """
    colors = ['yellow', 'lime', 'red']
    titles = ['Laplacian of Gaussian', 'Difference of Gaussian',
              'Determinant of Hessian']

    sequence = zip(blobs_list, colors, titles)

    fig, axes = plt.subplots(1, 3, figsize=(9, 3), sharex=True, sharey=True,
                            subplot_kw={'adjustable': 'box-forced'})

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
    plt.savefig(os.getcwd() + "/out/image" + "/" + image_file)

def find_segmentation_images_folder():
    """
    Precondition: the segmentation_images exists.
    Return the segmentation_images folder.

    @return the segmentation_images folder.
    """
    cwd = os.getcwd()
    os.chdir("../segmentation_images")
    segmentation_images_folder = os.getcwd()
    os.chdir(cwd)
    return segmentation_images_folder

def main(w_ratio=0.05, l_ratio=0.05, dev=0.25, thr=0.075):
    """
    Run the main script.

    """

    os.chdir(os.getcwd() + "/blob")

    input_folder = find_segmentation_images_folder()
    output_folder = os.getcwd() + "/out"

    # Default ranges of window sizes (hyperparameters)
    w_ratio = 0.05
    l_ratio = 0.05
    dev = 0.25 #average deviance ratio of radius
    thr = 0.075

    create_out_folder_cwd()
    process_all_images_of_in_folder(input_folder, output_folder, w_ratio, l_ratio, dev, thr)

    os.chdir("..")

if __name__ == "__main__":
    main()
