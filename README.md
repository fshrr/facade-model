Window Segmentation and Polygonal Approximation

Structure of Pipeline:

1. input_images -> edge detection and KITTI segmentation -> edge_images + segmentation_images
2. segmentation_images -> blob detection on segmentation -> image_points
3. edge_images + image_points -> floodfill + polygon approximation -> output_shapes

Need:

run_program.py to start Pipeline
polygon approximation scripts
python to .exe
