from fpdf import FPDF
from PIL import Image
import glob
import re
import os
import img2pdf

def make_all_pdf(in_dir = '', out_dir = ''):
    #check if the given path has a \ at the end
    if out_dir[-1] != '/':
        out_dir += '/'
    
    #gets the path name from root of all the sub-directories and its childs in the given root directory
    dirs = get_all_dirs(in_dir)

    files_found = len(dirs)
    processed_files = 0

    print("Found " + str(files_found) + " folders!")

    for i in dirs:
        if make_pdf(i, out_dir) == True:
            processed_files += 1
            progress = round(processed_files / files_found * 100, 1)
            print(str(progress) + r"% finished...")
        else:
            #if an error happens
            continue
    
    print("Converted " + str(processed_files) + " files!")

def get_all_dirs(root_dir = ''):
    if (root_dir):
        root_dir += "/"
    return [dir for dir in glob.glob(root_dir + "**/*", recursive=True) if os.path.isdir(os.path.join(root_dir, dir)) == True]

def get_all_images(root = ''):

    if (root):
        root += "/"
    
    root_list = [f for f in glob.glob(root + "**/*", recursive=True) if os.path.isdir(f) == False]
    if len(root_list) > 0:
        list_of_images = []

        for image_file in root_list:
            #supported file extensions are: jpg, png, gif
            filename, file_extension = os.path.splitext(image_file)
            if file_extension == '.jpg' or file_extension == '.png' or file_extension == '.gif':
                list_of_images.append(image_file)
        
        if len(list_of_images) > 0:
            return sort_alphanum(list_of_images)
        
    else:

        return root_list

def make_pdf(in_dir = '', out_dir = ''):
    if (in_dir):
        in_dir += "/"
    
    if (out_dir):
        out_dir += "/"

    #get all the files in the given directory
    list_of_files = get_all_images(in_dir)

    if len(list_of_files) > 0:
        try:

            pdf_name = list_of_files[0].split('\\')[-2]
            print("Converting " + pdf_name)

            with open(out_dir + pdf_name + ".pdf", "wb") as f:
                for image in list_of_files:
                    f.write(img2pdf.convert(image))
            '''
            cover = Image.open(list_of_files[0])
            width, height = cover.size

            pdf = FPDF(unit = "pt", format = [width, height])

            for current_image in list_of_files:
                #add an empty page
                pdf.add_page()
                #add the image with the same scale as the cover
                pdf.image(current_image, 0, 0, width, height)
            pdf.output(out_dir + pdf_name + ".pdf", "F")
            '''
            return True
        except:
            print("Error while processing " + str(in_dir))
            return False
    else:
        return False

def sort_alphanum(list_to_sort):
    convert = lambda text: int(text) if text.isdigit() else text  
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]  
    return sorted(list_to_sort, key = alphanum_key)

def make_img2pdf(in_dir = '', out_dir = ''):
    if out_dir[-1] != '/':
        out_dir += '/'
    
    list_of_images = get_all_images(in_dir)

    if len(list_of_images) > 0:
        pdf_name = list_of_images[0].split('\\')[-2]
        print("Converting " + pdf_name)
        with open(out_dir + pdf_name + ".pdf", "wb") as f:
            f.write(img2pdf.convert([i for i in list_of_images]))

    
    print("end")
    


if __name__ == "__main__":
    opening_info = '''
    this software is to convert all folders with multiple images into multiple pdfs
    input root directory of folders to convert
    and then input the directory in which you want to save all those files
    '''
    
    print(opening_info)

    root_dir = input("Input root directory: ")
    save_to_dir = input("Input where to save all the PDFs: ")

    make_all_pdf(root_dir, save_to_dir)

    #make_img2pdf(root_dir, save_to_dir)

