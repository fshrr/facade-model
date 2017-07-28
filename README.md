#Window Segmentation and Polygon Approximation

#Pipeline Structure:

1. input_images -> edge detection and KITTI segmentation -> edge_images + segmentation_images
2. segmentation_images -> blob detection on segmentation -> image_points
3. edge_images + image_points -> floodfill + polygon approximation -> output_shapes

#TODO:

1. polygon approximation scripts

2. KITTISeg to output segmentation images into image folders inside segmentation_images

3. run_program.py to start Pipeline

4. settings.txt to read from

5. limit floodfill after x,y passes a certain point

6. python to .exe

7. rhino rasteur image to vector?
