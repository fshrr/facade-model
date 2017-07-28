from PIL import Image
import os

def create_out_folder():
    """
    Create and out folder in the current working directory and return its
    absolute path.
    """
    cwd = os.getcwd()
    new_dir = cwd + "/out"
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    return new_dir

def find_input_folder():
    """
    Find the input folder "/mid" in the current working directory and return its
    absolute path.
    """
    cwd = os.getcwd()
    input_dir = cwd + "/mid"
    if not os.path.exists(input_dir):
        input_dir = os.filedialog.askfilenamedirectory()
    return input_dir

def create_output_image_folder(image_list, output_dir):
    """
    Create an image directory for each image in the output_dir.

    @params image_list the list of image names
    @params output_dir the path to the output folder
    """
    new_image_dir = output_dir
    for image in image_list:
        new_image_dir = output_dir + "/" + image.split(".")[0]
        if not os.path.exists(new_image_dir):
            os.mkdir(new_image_dir)

def check_png(image_list):
    """
    Check if the image is a .png. Otherwise, remove it from the image_list.

    @params image_list a list of image names.
    """
    for file in image_list[:]:
        if not(file.endswith(".png")):
            image_list.remove(file)

def create_edge_images_folder():
    """
    Create an edge_images folder in the parent folder if it does not exist and
    return its absolute path.

    @return the path to edge_images folder
    """
    cwd = os.getcwd()
    os.chdir("..")
    parent_folder = os.getcwd()
    os.chdir(cwd)
    if not os.path.exists(parent_folder + "/edge_images"):
        os.mkdir(parent_folder + "/edge_images")
    return parent_folder + "/edge_images"

def threshold_image(input_dir, output_dir, above_value, below_value, threshold_list, mod="Mod"):
    """
    Threshold the images given a threshold in the threshold_list.
    If the value in the image is above the threshold, set its value to be
    above_value and if below, set to below_value.

    This method produces many images with different thresholds and renames them
    with original image name + "Mod" + threshold. The images are saved in both
    the out directory of the current working directory and the edge_images
    folder.

    @params input_dir the path to the input directory
    @params output_dir the path to the output directory
    @params above_value the value that replaces the pixel if its value is greater than threshold
    @params below_value the value that replaces the pixel if its value is less than threshold
    @params threshold_list the list of thresholds that are considered
    @params mod the string to add to the name after thresholding
    """
    images = os.listdir(input_dir)
    check_png(images)
    create_output_image_folder(images, output_dir)
    edge_images_folder = create_edge_images_folder()
    create_output_image_folder(images,edge_images_folder)
    # Loop for every pixel, and given a threshold, turn it black or white
    for image in images:
        picture = Image.open(input_dir + "/" + image)
        new_image_dir = output_dir + "/" + image.split(".")[0]
        edge_new_image_dir = edge_images_folder + "/" + image.split(".")[0]
        # Get the size of the image
        width, height = picture.size
        for threshold in threshold_list:
        # Process every pixel
            picture = Image.open(input_dir + "/" + image)
            for x in range(width):
               for y in range(height):
                   #print(picture.getpixel((x,y)))
                   grey_value = picture.getpixel((x,y))
                   if grey_value > threshold:
                       picture.putpixel( (x,y), above_value)
                   else:
                       picture.putpixel( (x,y), below_value)

            # Save to cwd /out folder
            picture.save(new_image_dir + "/" + image.split(".")[0] + mod
                     + str(threshold) + ".png", "png")
            # Save to edge_images folder in parent directory
            picture.save(edge_new_image_dir + "/" + image.split(".")[0] + mod
                     + str(threshold) + ".png", "png")

if __name__ == "__main__":
    # Hyperparameters

    above_thres_grayscale_value = 255 # Define the feature color
    below_thres_grayscale_value = 0
    thresholds = [10, 20, 30, 40]

    input_dir = find_input_folder()
    output_dir = create_out_folder()
    threshold_image(input_dir, output_dir, above_thres_grayscale_value, below_thres_grayscale_value, thresholds)
