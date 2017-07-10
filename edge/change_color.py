from PIL import Image
import os
from tkinter import filedialog

# Hyperparameters
mod = "Mod"
new_scale = 255 # Define the feature color
black = 0
scale_threshold = [10, 20, 30, 40]

# Find folder directory
cwd = os.getcwd()
input_dir = cwd + "/mid"
new_dir = cwd + "/out"
if not os.path.exists(new_dir):
    os.makedirs(new_dir)

images = os.listdir(input_dir)
for file in images[:]:
    if not(file.endswith(".png")):
           images.remove(file)

# Make output directory


for image in images:
    new_image_dir = new_dir + "/" + image.split(".")[0]
    if not os.path.exists(new_image_dir):
        os.makedirs(new_image_dir)

# Loop
for image in images:
    picture = Image.open(input_dir + "/" + image)
    new_image_dir = new_dir + "/" + image.split(".")[0]
    # Get the size of the image
    width, height = picture.size
    for scale_value in scale_threshold:
    # Process every pixel
        picture = Image.open(input_dir + "/" + image)
        for x in range(width):
           for y in range(height):
               #print(picture.getpixel((x,y)))
               grey_value = picture.getpixel((x,y))
               if grey_value > scale_value:
                   picture.putpixel( (x,y), new_scale)
               else:
                   picture.putpixel( (x,y), black)

        picture.save(new_image_dir + "/" + image.split(".")[0] + mod
                 + str(scale_value) + ".png", "png")
