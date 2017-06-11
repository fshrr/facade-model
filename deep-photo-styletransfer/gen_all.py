import os
import math

# number of GPUs available
numGpus = 1

# number of image pairs to process
numImgs = 5

N = int(math.ceil(float(numImgs)/numGpus))
for j in range(1, numGpus + 1):
	cmd = ''

	for i in range(1, N + 1):
		idx = (1) * numGpus + j
		if idx <= numImgs:
			print('working on image pair index = ' + str(idx))

			part1_cmd = ' th neuralstyle_seg.lua -content_image trials/input/in'+str(idx)+'.png -style_image trials/style/tar'+str(idx)+'.png -content_seg trials/input_seg/in'+str(idx)+'.seg.png -style_seg trials/style_seg/tar'+str(idx)+'.seg.png -index '+str(idx)+' -num_iterations 1000 -save_iter 100 -print_iter 1 -gpu '+str(j-1)+' -serial trials/results_tmp'

			part2_cmd = ' th deepmatting_seg.lua -content_image trials/input/in'+str(idx)+'.png -style_image trials/style/tar'+str(idx)+'.png -init_image trials/results_tmp/out'+str(idx)+'\_t_1000.png -content_seg trials/input_seg/in'+str(idx)+'.seg.png -style_seg trials/style_seg/tar'+str(idx)+'.seg.png -index '+str(idx)+' -num_iterations 1000 -save_iter 100 -print_iter 1 -gpu '+str(j-1)+' -serial trials/results_final -f_radius 15 -f_edge 0.01'

			cmd = cmd + part1_cmd + part2_cmd

	cmd = cmd[1:len(cmd)-1]
	print(cmd)
	os.system(cmd)
