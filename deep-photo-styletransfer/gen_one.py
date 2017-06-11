import os
import sys

# VARIABLES TO MODIFY
# end the trial_folder dir with '/'
trial_folder = 'trials/'
# nested list of id. [input_id, style_id, output_id, num_iter, f_radius, f_edge]
test_cases = [[10, 10, 10.1, 1000, 15, 0.01],[10, 10, 10.2, 2000, 15, 0.01]]
# PARAMETER VARIABLES
save_iter = 200
gpu_id = 0
# Chnage to True if needs to be imported.
import_image = False

# SCRIPT RUNNING CODE STARTS HERE
# logging
file_name = 'trials/log.txt'
log = open(file_name, 'a')

# looping through all test cases
for i in range(len(test_cases)):

    input_id, style_id, output_id  = test_cases[i][0], test_cases[i][1], test_cases[i][2]
    num_iter, f_radius, f_edge  = test_cases[i][3], test_cases[i][4], test_cases[i][5]

    # importing images using import_image.sh. NOT ON by default.
    if (import_image == True):
        print ("importing images...")
        # running the import script for all input and style images
        if (id < 1000):
            database = "DPST"
        elif (id >= 1000) and (id <= 3000):
            database = "CMP"
        else:
            print ("Dont know which database to use")
            quit()
        # import_image.sh command string
        import_cmd = trial_folder + "import_image.sh -D " + database + " -i " + input_id + " -s " + style_id
        import_return = os.system("import_cmd")
        # error handing for import_image.sh
        if (import_return != 0):
            error_prompt = input("\n Something went wrong in importing the files - \n" + input_id + ", " + output_id + "\n Want to continue? (y/n):")
            if (error_prompt == 'y'):
                break
            elif (error_prompt == 'n'):
                print ("Gooodbye!")
                quit()

        print ("Done importing images")

    # logging
    data and time
    log.write("output_id = " + output_id + '\n')
    log.write("input_id = " + input_id + ", style_id = ", + style_id + '\n')
    log.write("num_iter = " + num_iter + '\n')
    log.write("f_radius = " + f_radius + ", f_edge = ", + f_edge + '\n')

    # Command strings for running neuralstyle and deepmatting. this looks disgusting.
    neuralstyle = 'th neuralstyle_seg.lua -index '+ str(output_id)+' -content_image '+trial_folder+'input/in'+str(input_id)+'.png -content_seg '+trial_folder+'input_seg/in'+str(input_id)+'.seg.png -style_image '+trial_folder+'style/tar'+str(style_id)+'.png -style_seg '+trial_folder+'style_seg/tar'+str(style_id)+'.seg.png -num_iterations '+str(num_iter)+' -save_iter '+str(save_iter)+' -print_iter 1 -gpu '+str(gpu_id)+' -serial '+trial_folder+'results_tmp -backend cudnn -cudnn_autotune'

    deepmatting = ' th deepmatting_seg.lua -index '+str(output_id)+' -init_image '+trial_folder+'results_tmp/out'+ str(output_id)+'\_t_1000.png -content_image '+trial_folder+'input/in'+str(input_id)+'.png -content_seg '+trial_folder+'input_seg/in'+str(input_id)+'.seg.png -style_image '+trial_folder+'style/tar'+str(style_id)+'.png -style_seg '+trial_folder+'style_seg/tar'+str(style_id)+'.seg.png -num_iterations '+str(num_iter)+' -save_iter '+str(save_iter)+' -print_iter 1 -gpu '+str(gpu_id)+' -serial trials/results_final -f_radius '+str(f_radius)+' -f_edge '+str(f_edge)+' -backend cudnn -cudnn_autotune'

    # running neuralstyle command
    print("running neuralstyle for input_id" + str(input_id) + "...")
    cmd_return = os.system(neuralstyle)
    if (cmd_return != 0):
        log.write("neuralstyle failed")
        error_prompt = input("\n Something went wrong in neuralstyle. Want to continue to deepmatting? (y/n):")
        if (error_prompt == 'y'):
            pass
        elif (error_prompt == 'n'):
            quit()
    log.write("neuralstyle successful")
    print("\n Completed neuralstyle for input_id" + str(input_id))

    # running deepmatting command
    print("\n Running deepmatting for input_id" + str(input_id) + "...")
    cmd_return = os.system(deepmatting)
    if (cmd_return != 0):
        log.write("neuralstyle failed")
        print("\n Something went wrong in deepmatting. All hopes are lost!!! GOODBYE!")
        quit()
    print("Completed deepmatting for input_id" + str(input_id))
    log.write("neuralstyle successful")

    #logging results
    log.write('\n\n')
# th neuralstyle_seg.lua -content_image trials/input/in5.png -style_image trials/style/tar5.png -content_seg trials/input_seg/in5.seg.png -style_seg trials/style_seg/tar5.seg.png -index 5 -num_iterations 1000 -save_iter 100 -print_iter 1 -gpu 0 -serial trials/results_tmp -backend cudnn -cudnn_autotune

# th deepmatting_seg.lua -content_image trials/input/in5.png -style_image trials/style/tar5.png -init_image trials/results_tmp/out5\_t_1000.png -content_seg trials/input_seg/in5.seg.png -style_seg trials/style_seg/tar5.seg.png -index 5 -num_iterations 1000 -save_iter 100 -print_iter 1 -gpu 0 -serial trials/results_final -f_radius 15 -f_edge 0.01 -backend cudnn -cudnn_autotune
