import os, sys, getopt

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"i:")
    except getopt.GetoptError:
        print("make_folder_image.py -i <image_folder>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-i":
            if os.path.exists(arg):
                make_folder(arg)

def make_folder(image_directory):
    img_list = os.listdir(image_directory)
    for img in img_list:
        if img.split(".")[-1] == "png":
            new_dir = image_directory +"/" + img.split(".png")[0]
            os.mkdir(new_dir)
            os.rename(image_directory + "/" + img, new_dir + "/" + img)

if __name__ == "__main__":
    main(sys.argv[1:])
