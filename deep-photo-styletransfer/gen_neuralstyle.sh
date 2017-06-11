#!/usr/bin/zsh

th neuralstyle_seg.lua -content_image examples/input/in5.png -style_image examples/style/tar5.png -content_seg examples/segmentation/in5.png -style_seg examples/segmentation/tar5.png -index 5 -num_iterations 1000 -save_iter 100 -print_iter 1 -serial examples/new_tmp_results 
# -backend cudnn -cudnn_autotune
# -backend cudnn -cudnn_autotune
# -gpu 0
