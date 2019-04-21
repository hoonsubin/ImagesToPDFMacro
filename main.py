from fpdf import FPDF
from PIL import Image
import glob
import re
import os

def make_all_pdf(in_dir = '', out_dir = ''):
    #check if the given path has a \ at the end
    if in_dir[-1] != '\\':
        in_dir += '\\'
    
    #gets the path name from root of all the sub-directories and its childs in the given root directory
    dirs = [dI for dI in glob.glob(in_dir + r"**\*", recursive=True) if os.path.isdir(dI)]
    #add the root directroy as well
    #dirs.append(in_dir)

    files_found = len(dirs)
    processed_files = 0

    for i in dirs:
        if make_pdf('', i, i) == True:
            processed_files += 1
            progress = round(processed_files / files_found * 100, 1)
            print(str(progress) + r"% finished...")
    
    print("Converted " + str(processed_files) + " files!")


def make_pdf(out_name, in_dir = '', out_dir = ''):
    #get all the files in the given directory
    list_of_files = [f for f in glob.glob(in_dir + "**/*", recursive=True) if os.path.isdir(f) == False]
    if len(list_of_files) > 0:
        #sort the list alphanumerically
        

        if (in_dir):
            in_dir += "/"
        
        files_to_convert = []

        for image_file in list_of_files:
            #supported file extensions are: jpg, png, gif
            filename, file_extension = os.path.splitext(image_file)
            if file_extension == '.jpg' or file_extension == '.png' or file_extension == '.gif':
                files_to_convert.append(image_file)
        
        if len(files_to_convert) > 0:
            
            sorted_image_list = sort_alphanum(files_to_convert)

            cover = Image.open(sorted_image_list[0])
            width, height = cover.size

            pdf = FPDF(unit = "pt", format = [width, height])

            for page in sorted_image_list:
                pdf.add_page()
                pdf.image(page, 0, 0)

            pdf.output(out_dir + out_name + ".pdf", "F")

            return True
        else:
            return False
    else:
        return False

def sort_alphanum(list_to_sort):
    convert = lambda text: int(text) if text.isdigit() else text  
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]  
    return sorted(list_to_sort, key = alphanum_key)

if __name__ == "__main__":
    opening_info = '''
    this software is to convert all images into pdfs
    so what the fuck
    '''
    
    print(opening_info)

    root_dir = input("Input root directory: ")
    save_to_dir = input("Input where to save all the PDFs: ")

    make_all_pdf(root_dir, root_dir)