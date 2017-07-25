import skimage.io as io
import os
import numpy as np

# Hyperparameters
input_folder = os.getcwd() + "/in"
points_folder = os.getcwd() + "/points"

# Create in and out subdirectories if they do not exist where the script
# is located
def create_out_folder():
    cwd = os.getcwd()
    if !os.exists(cwd + "/out"):
        os.mkdir(cwd + "/out")


# Assume image is MxN array and 1,0s
# Assume output correct
# and returns a nested list of 0,1 that
# denotes the object selected with 1s.
# Modifies a list that's supplied
def floodfill(nest_list, selection_list, x, y):
    width, height = nest_list.shape();
    # Base case
    # If current pixel is 1 "white"
    # return and do nothing
    if  nest_list[x][y] == 1 or x >= width or y >= height or
        x < 0 or y < 0:
        return

    else: # Check adjacent neighbor is valid or the filling color
        selection_list[x][y] = 1

        # left
        floodfill(nest_list, selection_list, x-1, y)
        # right
        floodfill(nest_list, selection_list, x+1, y)
        # up
        floodfill(nest_list, selection_list, x, y+1)
        # down
        floodfill(nest_list, selection_list, x, y-1)

def check_image(image_list):
    for image in image_list[:]:
        if image.split(".")[-1] != "png":
            image_list.remove(image)

def find_images(image_directory):
    im_list = os.listdir(image_directory)
    check_image(im_list)
    return im_list

def import_points_for_image(text_file):
    points_list = []
    with open(text_file, 'r') as f:
        for line in f:
            if len(line.split(",")) == 2:
                points_list.append((line.split(",")[0], line.split(",")[1]))

def select_object(image_file, x, y):
    im_array = io.imread(image_file)
    mask = np.zeros(im_array.shape[0], im_array.shape[0])
    filled_mask = floodfill(image, mask, x, y)

def select_all_objects(image_file, points_list):
    mask = np.zeros(im_array.shape[0], im_array.shape[0])
    for points in points_list:
        mask += select_object(image_file, points[0], points[1])
    return mask

def process_all_images(image_list)
    list_of_selection_masks = []
    for image_file in im_list:
        img_points_list = import_points_for_image(points_folder + "/" image_file)
        img_mask = select_all_objects(image_file, img_points_list)
        list_of_selection_masks.append(img_mask)
    return list_of_selection_masks

def save_all_images(directory, ndarray_list):
    for ndarray in ndarray_list:
        io.imsave(directory + "/" + ndarray, "png")

if __name__ == "__main__":
    create_out_folder()
    img_list = find_images(input_folder)
    ndarray_list = process_all_images(img_list)
    save_all_images(cwd + "/out", ndarray_list)
