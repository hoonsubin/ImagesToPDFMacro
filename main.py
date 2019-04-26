# The MIT License (MIT)
# Copyright (c) 2019 Hoon Kim
#
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the Software 
# is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT
# OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from PIL import Image
import glob
import re
import os
import img2pdf
import sys

delimiter = '\\'

opening_info = '''
this software is to convert all folders with multiple images into multiple pdfs
input root directory of folders to convert
and then input the directory in which you want to save all those files
'''

def make_all_pdf(in_dir = '', out_dir = ''):
    #check if the given path has a \ at the end
    if out_dir[-1] != delimiter:
        out_dir += delimiter
    
    #gets the path name from root of all the sub-directories and its childs in the given root directory
    dirs = get_all_dirs(in_dir)

    files_found = len(dirs)
    processed_files = 0
    finished_files = 0

    print("Found " + str(files_found) + " folders!")

    file = open(out_dir + "error_log.txt", "w", encoding = 'utf-8')
    
    for i in dirs:
        try:
            if make_pdf(i, out_dir) == True:
                finished_files += 1
                
            else:
                #if an error happens just continue on to the next folder
                continue
            
            #calculate how far the progress is
            processed_files += 1
            #progress = round(processed_files / files_found * 100, 1)
            progress_bar(processed_files, files_found, status="converting images...")
            #print(str(progress) + r"% finished...")

        except Exception as e:
            log = "[Error]directory: " + i + "\n" + "message: " + str(e) + "\n"
            file.write(log)
            continue
    
    file.close()
    print("Converted " + str(finished_files) + " files!")


def get_all_dirs(root_dir = ''):
    if root_dir[-1] != delimiter:
        root_dir += delimiter
    
    #get the list of all the dirs and its childerens
    dirs = [dir for dir in glob.glob(root_dir + "**/*", recursive=True) if os.path.isdir(os.path.join(root_dir, dir)) == True]

    if len(dirs) > 0:
        return dirs
    else:
        return dirs.append(root_dir)

def get_all_images(root = ''):
    if root[-1] != delimiter:
        root += delimiter
    
    root_list = [f for f in glob.glob(root + "**/*", recursive=False) if os.path.isdir(os.path.join(f)) == False]
    
    root_list = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(root):
        for file in f:
                root_list.append(os.path.join(r, file))

    if len(root_list) > 0:
        list_of_images = []

        for image_file in root_list:
            #supported file extensions are: jpg, png, gif
            file_extension = get_image_type(image_file)

            #check if the file type is correct
            if file_extension == '.jpg' or file_extension == '.gif' or file_extension == '.png':
                list_of_images.append(image_file)

            '''
            elif file_extension == '.png':
                #get rid of alpha channel
                image = Image.open(image_file)
                image_rgb = image.convert('RGB')
                image_rgb.save(image_file, "PNG")
                list_of_images.append(image_file)
            '''

        if len(list_of_images) > 0:
            return sort_alphanum(list_of_images)
        
    else:
        print("no images found in " + root)
        return root_list

def get_image_type(im_dir = ''):
    
    file_extension = os.path.splitext(im_dir)[1]

    image_exts = ['.jpg', '.png', '.gif']

    #check the file extension and return it if it is one of those
    if file_extension in image_exts:
        return file_extension
    else:
        return 'na'

def make_pdf(in_dir = '', out_dir = ''):

    if in_dir[-1] != delimiter:
        in_dir += delimiter

    if out_dir[-1] != delimiter:
        out_dir += delimiter

    #get all the files in the given directory
    list_of_files = get_all_images(in_dir)

    if len(list_of_files) > 0:
        #assign the full directory and the name of the saved pdf
        pdf_to_save = out_dir + list_of_files[0].split('\\')[-2] + ".pdf"
        
        #open a pdf file as a byte to add images
        with open(pdf_to_save, "wb") as f:
            try:
                pdf = img2pdf.convert(list_of_files)
                #write all the iamges to the pdf
                f.write(pdf)
                print("[Debug]Saved pdf " + list_of_files[0].split('\\')[-2] + "\n")
                #return true to say that it has been finished
                return True

            except Exception as e:
                #when an error happens, remove the saved pdf file, and raise the error
                f.close()
                os.remove(pdf_to_save)
                print("[Error]error while processing " + pdf_to_save + "\n[Error Message]" + str(e))
                raise Exception(e)
    
    else:
        return False
        

def sort_alphanum(list_to_sort):
    convert = lambda text: int(text) if text.isdigit() else text  
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]  
    return sorted(list_to_sort, key = alphanum_key)

def progress_bar(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

if __name__ == "__main__":
    
    print(opening_info)

    root_dir = input("Input root directory: ")
    save_to_dir = input("Input where to save all the PDFs: ")

    make_all_pdf(root_dir, save_to_dir)
    

    