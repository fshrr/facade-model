# Window Segmentation and Shape Approximation

# Pipeline Structure:

1. input_images -> edge detection and KITTI segmentation -> edge_images + segmentation_images
2. segmentation_images -> blob detection on segmentation -> image_points
3. edge_images + image_points -> floodfill + polygon approximation -> output_shapes

# Make image name subdirectories for PNG images in any folder

In terminal, enter: python make_folder_image.py -i "folder path that contains images"

# Running the entire process

Add all images that are to be processed into the input_images folder.
In terminal, run: python run_all.py

# TODO:

2. KITTISeg to output segmentation images into image folders inside segmentation_images. Not implemented atm.

5. Limit floodfill after x,y passes a certain point. Maybe? 

7. Rasteur image to vector? Not working atm.
