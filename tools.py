import sys
import os
import main
import glob
import re

delimiter = main.delimiter


# sort the list of texts in alphanumeric order
def sort_alphanum(list_to_sort):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(list_to_sort, key=alphanum_key)


# console progress bar
def progress_bar(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


def get_image_type(im_dir=''):
    file_extension = os.path.splitext(im_dir)[1]

    # check the file extension and return it if it is one of those
    if file_extension in main.supported_exts:
        return file_extension
    else:
        return 'na'


# function that gets all the directories and its child
def get_all_dirs(root_dir=''):
    if root_dir[-1] != delimiter:
        root_dir += delimiter

    # get the list of all the dirs and its childerens
    dirs = [dir for dir in glob.glob(root_dir + "**/*", recursive=True) if os.path.isdir(dir) == True]

    if len(dirs) <= 0:
        dirs.append(root_dir)

    return dirs


def get_all_image_dirs(root=''):
    if root[-1] != delimiter:
        root += delimiter

    root_list = [f for f in glob.glob(root + "**/*", recursive=False) if os.path.isdir(f) == False]

    root_list = []
    # r=root, d=directories, f = files
    for r, _, f in os.walk(root):
        for file in f:
            root_list.append(os.path.join(r, file))

    if len(root_list) > 0:
        list_of_images = []

        for image_file in root_list:
            # supported file extensions are: jpg, png, gif
            file_extension = get_image_type(image_file)

            if file_extension in main.supported_exts:
                list_of_images.append(image_file)

        if len(list_of_images) > 0:
            return sort_alphanum(list_of_images)

    else:
        print("no images found in " + root)
        return root_list
