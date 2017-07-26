import skimage.io as io
import os
import numpy as np
import re
import sys
from collections import deque
import time
# Hyperparameters
input_folder = os.getcwd() + "/in"
points_folder = os.getcwd() + "/points"
output_folder = os.getcwd() + "/out"


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
# Create in and out subdirectories if they do not exist where the script
# is located
def create_out_folder():
    cwd = os.getcwd()
    if not os.path.exists(cwd + "/out"):
        os.mkdir(cwd + "/out")

def create_image_folders_in_out(in_dir, out_dir):
    """
    Assuming that the in folder contains directories of images, create the
    same folder in the out directory.
    """
    cwd = os.getcwd()
    # file list in cwd
    l = os.listdir(in_dir)
    for f in l:
        if os.path.isdir(in_dir + "/" + f) and not os.path.exists(out_dir + "/" + f):
            os.mkdir(out_dir + "/" + f)

def floodfill(nest_list, selection_list, x, y):
    """
    Assume image is MxN array and 1,0s and output correc, return a nested list
    of 0,1 where 1 denotes the object selected.
    Modifies a numpy array of zeroes supplied in the parameters.
    """
    width, height = nest_list.shape;
    # Base case
    # If current pixel is 1 "white"
    # return and do nothing
    if x >= width or y >= height or x < 0 or y < 0:
        return

    if nest_list[x][y] == 255:
        return

    else: # Check adjacent neighbor is valid or the filling color
        selection_list[x][y] = 255

        # left
        floodfill(nest_list, selection_list, x-1, y)
        # right
        floodfill(nest_list, selection_list, x+1, y)
        # up
        floodfill(nest_list, selection_list, x, y+1)
        # down
        floodfill(nest_list, selection_list, x, y-1)

def floodfill(nest_list, selection_list, x, y, min_ignore=0, max_ignore=255):
    """
    In the scenario when you use a sobel image directly, select the set of
    points such that its value is not between min_ignore and max_ignore.

    """
    # Base case
    # If current pixel is 1 "white"
    # return and do nothing

    queue = Queue()
    queue.enqueue((x,y))

    checklist_array = {}

    while not queue.isEmpty(): # Check adjacent neighbor is valid or the filling color
        a, b = queue.dequeue()
        selection_list[b,a] = 255
        checklist_array[(a,b)] = 1
        # print((a,b) in checklist_array)
        # Up
        if (a,b-1) not in checklist_array and check_valid(a,b-1,nest_list, min_ignore=0, max_ignore=255):
            #print("1")
            queue.enqueue((a, b-1))
            checklist_array[(a,b-1)] = 1
        # Down
        if (a,b+1) not in checklist_array and check_valid(a,b+1,nest_list, min_ignore=0, max_ignore=255):
            #print("2")
            queue.enqueue((a, b+1))
            checklist_array[(a,b+1)] = 1
        # Right
        if (a+1,b) not in checklist_array and check_valid(a+1,b,nest_list, min_ignore=0, max_ignore=255):
            #print("3")
            queue.enqueue((a+1, b))
            checklist_array[(a+1,b)] = 1
        # Left
        if (a-1,b) not in checklist_array and check_valid(a-1,b,nest_list, min_ignore=0, max_ignore=255):
            #print("4")
            queue.enqueue((a-1, b))
            checklist_array[(a-1,b)] = 1
        
        print(str(a) + "," + str(b))
        print("The queue size is: " + str(queue.size()))
       # time.sleep(5)
       # print(selection_list)

def check_valid(x, y, nest_list, min_ignore=0, max_ignore=255):

    height, width = nest_list.shape
    if (x < width and y < height and x >= 0 and y >= 0) and 0.0 <= nest_list[y][x] <= min_ignore:
        return True
    else:
        return False

def check_image(image_list):
    for image in image_list[:]:
        if image.split(".")[-1] != "png":
            image_list.remove(image)

def find_images(image_directory):
    im_list = os.listdir(image_directory)
    check_image(im_list)
    return im_list

def import_points_for_image(text_filename, points_folder):
    # retrive the part of the string i.e. greyscaleMod30 that contains
    # greyscale but does not have Mod30 . In other words, the regex
    # is "(" + text_filename + ""
    points_list = []
    points_folder_list = os.listdir(points_folder)
    for point_file_name in points_folder_list:

        if text_filename.startswith(point_file_name.split(".txt")[0]):
            print(text_filename)
            print(point_file_name.split(".txt")[0])
            with open(points_folder + "/" + point_file_name, 'r') as f:
                for line in f:
                    points_list.append((line.split(" ")[0], line.split(" ")[1]))
    return points_list

def select_object(image_file, x, y, min_ignore=0, max_ignore=255):
    im_array = io.imread(image_file)
    mask = np.zeros((im_array.shape[0], im_array.shape[1]), dtype=int)
    floodfill(im_array, mask, x, y, min_ignore=0, max_ignore=255)
    #print(np.nonzero(mask))
    return mask

def select_all_objects(image_file, points_list, min_ignore=0, max_ignore=255):
    im_array = io.imread(image_file)
    mask = np.zeros((im_array.shape[0], im_array.shape[1]), dtype=int)
    print(mask.shape)
    for points in points_list:
        # Note that the points are (y,x)
        
        new_object =  select_object(image_file, int(float(points[1])), int(float(points[0])), min_ignore=0, max_ignore=255)
        mask = mask + new_object
        print ("new object")
        print (new_object)
        print ("maask here")
        print(mask)
    #print(np.nonzero(mask))
    mask[mask>1] = 255
    print(mask)
    return mask

def process_all_images(image_list, img_dir, output_dir, points_folder, min_ignore=0, max_ignore=255):
    dict_of_selection_masks = {}

    for image_file in image_list:
        img_loc = img_dir + "/" + image_file
        img_points_list = import_points_for_image(image_file.split(".png")[0], points_folder)
        img_mask = select_all_objects(img_loc, img_points_list, min_ignore=0, max_ignore=255)
        dict_of_selection_masks[image_file] = img_mask

        image_name = image_file.split(".png")[0]

        output_dir_list = os.listdir(output_dir)
        for folder_name in output_dir_list:
            if image_name.startswith(folder_name):
                io.imsave(output_dir + "/" + folder_name + "/" + image_file, img_mask)
    return dict_of_selection_masks

def process_all_images_of_in_folder(input_dir, output_dir, points_folder, min_ignore=0, max_ignore=255):
    """
    Assumes that the in directory only contains folders.
    """
    subdirs = os.listdir(input_dir)
    for folder_name in subdirs:
        img_dir = input_dir + "/" + folder_name
        img_list = find_images(img_dir)
        image_to_ndarray = process_all_images(img_list, img_dir, output_dir, points_folder, min_ignore=0, max_ignore=255)

def save_all_images(directory, ndarray_dict):
    """
    Saves images given a directory and a dictionary of image file names to
    ndarray.
    """
    for ndarray in ndarray_dict.keys():
        io.imsave(directory + "/" + ndarray.split(".png")[0] + "/" + ndarray)

if __name__ == "__main__":
    # Hyperparameters
    input_folder = os.getcwd() + "/in"
    points_folder = os.getcwd() + "/points"
    output_folder = os.getcwd() + "/out"

    create_out_folder()
    create_image_folders_in_out(input_folder, output_folder)
    # list of directories where images are stored

    # list of images in that directory
    #img_list = find_images(input_folder)
    #ndarray_list = process_all_images(img_list)
    #save_all_images(cwd + "/out", ndarray_list)

    process_all_images_of_in_folder(input_folder, output_folder, points_folder, min_ignore=0.0, max_ignore=255.0)
