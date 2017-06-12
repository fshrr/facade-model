import os
import sys
import time
import datetime

################ VARIABLES TO MODIFY ################

# nested list of id. [input_id, style_id, output_id, num_iter, f_radius, f_edge, laplacian]
# test_cases = [[10, 10, 10.5, 1000, 15, 0.05], [10, 10, 10.4, 2000, 15, 0.05], [10, 10, 10.5, 1000, 50, 0.01], [10, 10, 10.6, 2000, 50, 0.01]]
test_cases = [[1056.0, 1057.0, 10560, 1000, 7, 0.01, 1056]]

# N=neuralstyle, D=deepmatting, B=both
test_type = ['B', 'B']
save_iter = 250
print_iter = 1
gpu_id = 0
# end the trial_folder dir with '/'
trial_folder = 'trials/'
# Chnage to True if images need to be imported from CMP or DPST database
import_image = False


################ SCRIPT RUNNING CODE STARTS HERE ################

def main():
    # logging
    file_name = 'trials/log.txt'
    log = open(file_name, 'a')

    # looping through all test cases
    for i in range(len(test_cases)):

        log.write('\n\n')

        # defining vars for each case
        input_id, style_id, output_id  = test_cases[i][0], test_cases[i][1], test_cases[i][2]
        num_iter, f_radius, f_edge  = test_cases[i][3], test_cases[i][4], test_cases[i][5]
        laplacian = test_cases[i][6]

        # importing images using import_image.sh. NOT ON by default.
        if (import_image == True):
            import_image_func(input_id, style_id, trial_folder)

        # logging
        start_time = time.time()
        log_info(log, start_time, input_id, style_id, output_id, num_iter, f_radius, f_edge)

        # Command strings for running neuralstyle and deepmatting. this looks disgusting.
        neuralstyle = 'th neuralstyle_seg.lua -index '+ str(output_id)+' -content_image '+trial_folder+'input/in'+str(input_id)+'.png -content_seg '+trial_folder+'input_seg/in'+str(input_id)+'.seg.png -style_image '+trial_folder+'style/tar'+str(style_id)+'.png -style_seg '+trial_folder+'style_seg/tar'+str(style_id)+'.seg.png -num_iterations '+str(num_iter)+' -save_iter '+str(save_iter)+' -print_iter '+str(print_iter)+' -gpu '+str(gpu_id)+' -serial '+trial_folder+'results_tmp -backend cudnn -cudnn_autotune'

        deepmatting = 'th deepmatting_seg.lua -index '+str(output_id)+' -laplacian '+str(laplacian)+' -init_image '+trial_folder+'results_tmp/out'+ str(output_id)+'_t_'+str(num_iter)+'.png -content_image '+trial_folder+'input/in'+str(input_id)+'.png -content_seg '+trial_folder+'input_seg/in'+str(input_id)+'.seg.png -style_image '+trial_folder+'style/tar'+str(style_id)+'.png -style_seg '+trial_folder+'style_seg/tar'+str(style_id)+'.seg.png -num_iterations '+str(num_iter)+' -save_iter '+str(save_iter)+' -print_iter 1 -gpu '+str(gpu_id)+' -serial trials/results_final -f_radius '+str(f_radius)+' -f_edge '+str(f_edge)+' -backend cudnn -cudnn_autotune'

        # running neuralstyle and recording time spent
        if ((test_type[i] == 'B') or (test_type[i] == 'N')):
            run_neuralstyle(neuralstyle, input_id, log, start_time)
        neuralstyle_time = time.time()
        log.write("neuralstyle-time: " + str(humanize_time(neuralstyle_time - start_time)) + '\n')

        # running deepmatting and recording time spent
        if ((test_type[i] == 'B') or (test_type[i] == 'D')):
            run_deepmatting(deepmatting, input_id, log, start_time)
        deepmatting_time = time.time()
        log.write("deepmatting-time: " + str(humanize_time(deepmatting_time - neuralstyle_time)) + '\n')

    log.close()


# th neuralstyle_seg.lua -content_image trials/input/in5.png -style_image trials/style/tar5.png -content_seg trials/input_seg/in5.seg.png -style_seg trials/style_seg/tar5.seg.png -index 5 -num_iterations 1000 -save_iter 100 -print_iter 1 -gpu 0 -serial trials/results_tmp -backend cudnn -cudnn_autotune

# th deepmatting_seg.lua -content_image trials/input/in5.png -style_image trials/style/tar5.png -init_image trials/results_tmp/out5\_t_1000.png -content_seg trials/input_seg/in5.seg.png -style_seg trials/style_seg/tar5.seg.png -index 5 -num_iterations 1000 -save_iter 100 -print_iter 1 -gpu 0 -serial trials/results_final -f_radius 15 -f_edge 0.01 -backend cudnn -cudnn_autotune

################ HELPER FUNCTIONS ################
def gen_laplacian():
    octave_cmd = "LD_PRELOAD=libnvblas.so octave gen_laplacian/gen_laplacian.m"

def import_image_func(input_id, style_id, trial_folder):
    print ("importing images...")
    # running the import script for all input and style images
    if (input_id < 1000):
        database = "DPST"
    elif (input_id >= 1000) and (input_id <= 3000):
        database = "CMP"
    else:
        print ("Dont know which database to use")
        quit()
    # import_image.sh command string
    import_cmd = trial_folder + "import_image.sh -D " + database + " -i " + str(input_id) + " -s " + str(style_id)
    print (import_cmd)
    import_return = os.system(import_cmd)
    # error handing for import_image.sh
    if (import_return != 0):
        error_prompt = input("\n Something went wrong in importing the files - \n" + str(input_id) + ", " + str(style_id) + "\n Want to continue? (y/n):")
        while (error_prompt not in ('y', 'n')):
            error_prompt = input("\n Type 'y' or 'n' please:")
        if (error_prompt == 'y'):
            pass
        elif (error_prompt == 'n'):
            print ("Gooodbye!")
            quit()

    print ("Done importing images")


def run_neuralstyle(neuralstyle, input_id, log, start_time):
    # running neuralstyle command
    print("running neuralstyle for input_id" + str(input_id) + "...")
    cmd_return = os.system(neuralstyle)
    if (cmd_return != 0):
        log.write("neuralstyle failed\n")
        error_prompt = input("\n Something went wrong in neuralstyle. Want to continue to deepmatting? (y/n):")
        while (error_prompt not in ('y', 'n')):
            error_prompt = input("\n Type 'y' or 'n' please:")
        if (error_prompt == 'y'):
            pass
        elif (error_prompt == 'n'):
            quit()
    else:
        log.write("neuralstyle successful\n")
        print("\n Completed neuralstyle for input_id" + str(input_id))

def run_deepmatting(deepmatting, input_id, log, start_time):
    # running deepmatting command
    print("\n Running deepmatting for input_id" + str(input_id) + "...")
    cmd_return = os.system(deepmatting)
    if (cmd_return != 0):
        log.write("deepmatting failed")
        print("\n Something went wrong in deepmatting. All hopes are lost!!! GOODBYE!")
        quit()
    else:
        print("Completed deepmatting for input_id" + str(input_id))
        log.write("deepmatting successful\n")

def log_info(log, start_time, input_id, style_id, output_id, num_iter, f_radius, f_edge):
    # logging the initial information
    log.write(datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S'))
    log.write("output_id = " + str(output_id) + '\n')
    log.write("input_id = " + str(input_id) + ", style_id = " + str(style_id) + '\n')
    log.write("num_iter = " + str(num_iter) + '\n')
    log.write("f_radius = " + str(f_radius) + ", f_edge = " + str(f_edge) + '\n')

def humanize_time(secs):
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return '%02d:%02d:%02d' % (hours, mins, secs)

if __name__ == '__main__':
    main()
