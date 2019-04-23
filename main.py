from PIL import Image
import glob
import re
import os
import img2pdf

delimiter = '\\'

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
            progress = round(processed_files / files_found * 100, 1)
            print(str(progress) + r"% finished...")

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
    
    root_list = [f for f in glob.glob(root + "**/*", recursive=True) if os.path.isdir(f) == False]

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
        return root_list

def get_image_type(im_dir = ''):
    #get the file extension of the given directory including the .

    file_extension = os.path.splitext(im_dir)[1]

    if file_extension == '.jpg' or file_extension == '.png' or file_extension == '.gif':
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
        with open(bytes(pdf_to_save, 'utf-8'), "wb") as f:
            try:
                #write all the iamges to the pdf
                f.write(bytes(img2pdf.convert([i for i in list_of_files]), 'utf-8'))
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

    