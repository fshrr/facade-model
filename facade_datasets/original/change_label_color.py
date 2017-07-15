from PIL import Image
import os
from tkinter import filedialog

# Hyperparameters
filename = "tmp"
new_color = (0,0,0) # Define the non-feature color
feat_color = (200,50,50) # Set at windows being red

# Find folder directory 
directory = filedialog.askdirectory()
images = os.listdir(directory)
for file in images[:]:
    if not(file.endswith(".png")):
           images.remove(file)

# Make output directory
new_dir = directory + "/out"
if not os.path.exists(new_dir):
    os.makedirs(new_dir)

# Loop
c = 1
for image in images:

    picture = Image.open(directory + "/" + image)

    # Get the size of the image
    width, height = picture.size

    # Process every pixel
    for x in range(width):
       for y in range(height):
           red, green, blue = picture.getpixel((x,y))
           # Anything with R < 200 or G < 50 or B < 50 is non-feature
           # Change this for different colored labels
           if red < feat_color[0] or green > feat_color[1] or blue > feat_color[2]:
               picture.putpixel( (x,y), new_color)

    c += 1
    picture.save(new_dir + "/" + filename + str(c) + ".png", "png")
