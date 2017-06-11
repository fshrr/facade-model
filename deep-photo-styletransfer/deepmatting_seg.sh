#!/usr/bin/zsh

th deepmatting_seg.lua -content_image trials/input/in$1.png -style_image trials/style/tar5.png -init_image trials/results_tmp/out5\_t_1000.png -content_seg trials/input_seg/in5.seg.png -style_seg trials/style_seg/tar5.seg.png -index 5 -num_iterations 1000 -save_iter 100 -print_iter 1 -gpu 0 -serial trials/results_final -f_radius 15 -f_edge 0.01 -backend cudnn -cudnn_autotune
/opt/torch/install/bin/luajit: deepmatting_seg.lua:15: '=' expected near 'local'
