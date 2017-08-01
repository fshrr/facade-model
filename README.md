# Window Segmentation and Shape Approximation From 2D Facade Image

## Pipeline Structure:

1. input_images -> edge detection and KITTI segmentation -> edge_images + segmentation_images
2. segmentation_images -> blob detection on segmentation -> image_points
3. edge_images + image_points -> floodfill + polygon approximation + vectorization -> output_shapes + output_vectors

## Usage

#### Make image name subdirectories for PNG images in any folder

In terminal, enter: 

`python make_folder_image.py -i "folder path that contains images"`

#### Running the entire process

Add all images that are to be processed into the input\_images folder.

In terminal, run: 

`python run_all.py` 

## Pipeline Details
 
#### 01 Edge Detection 
 
The pipeline takes an user input of an image (.png) to run edge detection algorithms and outputs a set of images with varying thresholds. Prewitt edge detection algorithm is used for this process due to its ability to pick up more details of the façade when compared to other methods such as Canny edge detection.

#### 02 Window Segmentation Using Kittiseg
 
Window segmentation takes the same user input of an image and applies a Convolutional Neural Network called Kittiseg to output a semantic segmentation of windows and doors. Whereas Kittiseg was initially trained with a dataset of road images for segmenting roads, for this pipeline a combination of multiple datasets of labelled facades (CMP_base, CMP_extended, Graz50, Etrims, LabelMeFacade) was used for training. The dataset contains 769 images for training and 120 images for testing. 

#### 03 Blob Detection on Segmentation Image

Kittiseg output images are raster images that stores pixel information (white for window, black for "non-window") in a 2 dimensional array where the length and width of the array correspond to the image dimensions in pixels. This makes it difficult to work with each detected window separately. In order to locate the location of each window in the Kittiseg output, blob detection algorithm from scikit image library is used and the center point of every detected window is stored in a text file (as a list of xy coordinates and radius).

#### 04 Floodfill 

Kittiseg window detection is not 100% accurate when segmenting windows from facade images, especially when it is a deep dream image. So in order to detect more potential windows, the xy coordinates and the radius from blob detection is mapped onto the edge detected images. Flood fill algorithm is then used to find a closed area around the xy coordinate in the edge detected image. Since some windows might not have created closed edge with edge detection, in order to avoid flood filling walls as windows, user inputs of hyperparameters (i.e. ratio of window area compared to image) are used to restrict the flood fill window size. When a flood fill of a significantly larger area (compared to user input) is detected, the Kittiseg blob that is located within the xy coordinate is used instead. Following the application of the flood fill algorithm, a raster output image is displayed of the window detected regions.


#### 05 Polygon Approximation and Vectorization

Outputs from both Kittiseg segmentation and floodfill result in blobs of irregular structure, making it more complex and difficult for vectorization. To simplify the window detected regions into more regular polygons, Approximate Polygons and Subdivide Polygons algorithms from Scikit Image are used. This results in polygons around the area of the detected windows where varying tolerance values control the flexibility of the polygon formation around a region. Given that polygon approximation outputs a set of coordinates for polygon vertices, svgwrite is then used to create vectors (in .svg) for each polygon.

## TODO:

2. KITTISeg to output segmentation images into image folders inside segmentation\_images. Not implemented atm.

5. Limit floodfill after x,y passes a certain point. Maybe? 

7. Rasteur image to vector? Not working atm.
