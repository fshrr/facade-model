ICG Graz50 facade dataset

This is a dataset of rectified facade images and semantic labels.
The goal of the annotation is to study the layout of the facades.

It contains 50 images of various architectural styles such as
Classicism, Biedermeier, Historicism (neo-renaissance and
neo-baroque), Art Nouveau and as well as various modern styles. 
It portrays a wider range of complex facade layouts than other datasets.

The images are generated automatically after extracting a piecewise planar geometry 
from about 30 perspective images each. The view is orthographic however the 
piecewise planar geometry is only an approximation, which leads to 
artifacts during the image blending.

The facade images in the ICG Graz50 are labeled in multiple classes: 

labels_used - wall, door, window, sky - are used in the publication (see below)
labels_full - shop, balcony, roof - are NOT used due to too little training data

where the wall class is very coarse and covers mostly all background
which is not window or door, including sky and void areas of the image.

At the time of publication, the performance was the following:

	Window Wall Door Sky | Global Class IoU
MAP	60 	66  57   80 	66 65 43
Our	60 	84  41   91 	78 69 58

The protocol is to use 30 images for training and 20 for testing.

The dataset is used for facade layout study as the facade is mostly 
segmented out clean. Hence the goal is not to label all classes as best as possible
yet to understand the types of layout of different architectural styles.

If you use the ICG Graz50 dataset, please cite:

Irregular lattices for complex shape grammar facade parsing. CVPR 2012, Providence, USA. 
H. Riemenschneider, U. Krispel, W. Thaller, M. Donoser, S. Havemann, D. Fellner, H. Bischof.
http://www.vision.ee.ethz.ch/~rhayko/paper/cvpr2012_complex_facades_hayko.pdf

Contact: hayko@vision.ee.ethz.ch


