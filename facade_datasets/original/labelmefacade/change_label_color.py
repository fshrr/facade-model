from PIL import Image
import os
from tkinter import filedialog

# Hyperparameters
new_color = (0,0,0) # Define the non-feature color

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

for image in images:

    picture = Image.open(directory + "/" + image)
    picture = picture.convert('RGB')

    # Get the size of the image
    width, height = picture.size

    image_name = image.split(".")[0]
    
    # Process every pixel
    for x in range(width):
        for y in range(height):
            red, green, blue = picture.getpixel((x,y))
            if (red == 0 and green == 0 and blue == 128):
                picture.putpixel( (x,y), (255,0,0))
            else:
               picture.putpixel( (x,y), new_color)

    picture.save(new_dir + "/" + image_name + ".png", "png")
