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
import tools
import os
import img2pdf
import sys
import traceback
import gc

delimiter = '\\'
supported_exts: list = ['.jpg', '.png', '.gif', '.jpeg']
opening_info ='''
this software will convert all images in folders as pdfs, folder by folder
input root directory of folders to convert
and then input the directory in which you want to save all those files
'''

#main function
def main():
    print(opening_info)

    root_dir = input("Input root directory: ")
    save_to_dir = input("Input where to save all the PDFs: ")

    make_all_pdf(root_dir, save_to_dir)

    exit(0)

def make_all_pdf(in_dir = '', out_dir = ''):
    #check if the given path has a \ at the end
    if out_dir[-1] != delimiter:
        out_dir += delimiter
    
    print("Searching directory...")

    #gets the path name from root of all the sub-directories and its childs in the given root directory
    #currently it cannot work with images in the root

    dirs: list = tools.get_all_dirs(in_dir)
    

    files_found = len(dirs)
    processed_files = 0
    finished_files = 0

    failed_Process = []

    print("Found " + str(files_found) + " folders!")

    file = open(out_dir + "error_log.txt", "w", encoding = 'utf-8')
    
    for i in dirs:
        try:
            #calculate how far the progress is
            processed_files += 1

            if make_pdf(i, out_dir) == True:
                finished_files += 1
                
            else:
                #if an error happens just continue on to the next folder
                continue
            #progress = round(processed_files / files_found * 100, 1)
            tools.progress_bar(processed_files, files_found, status="converting images...")

        except Exception as e:
            log = "[Error]directory: " + i + "\n" + str(traceback.format_exc()) + "\n"
            failed_Process.append(i.split(delimiter)[-1])
            file.write(log)
            print(log)
            continue
        
        except (KeyboardInterrupt, SystemExit):
            exit_program = input("wish to exit program? (yes, no)")
            if exit_program == "yes" or exit_program == "y":
                print("shutting down...")
                exit(0)
                
            elif exit_program == "no" or exit_program == "n":
                print("continuing process")
                continue
    
    file.write("=====================failed folders======================\n")

    for i in failed_Process:
        file.write(i + "\n")
    file.write("Total failed files: " + str(processed_files - finished_files))
    file.close()
    print("Converted " + str(finished_files) + " files!")
    
def make_pdf(in_dir = '', out_dir = ''):

    if in_dir[-1] != delimiter:
        in_dir += delimiter

    if out_dir[-1] != delimiter:
        out_dir += delimiter

    #get all the image files in the given directory
    list_of_files = tools.get_all_image_dirs(in_dir)

    if len(list_of_files) > 0:
        #assign the full directory and the name of the saved pdf
        pdf_to_save = out_dir + list_of_files[0].split(delimiter)[-2] + ".pdf"
        
        try:
            #open pdf datastream in the given directory
            f = open(pdf_to_save, "wb")
            #define the pdf file to save/write
            with f:
                img2pdf.convert(list_of_files, outputstream=f)
            

        except Exception as e:
            os.remove(pdf_to_save)
            raise Exception(e)
            return False
        
        #run the garbage collector to flush the opened output stream
        gc.collect()
        return True


'''
        print("[Debug]Opened " + pdf_to_save.split(delimiter)[-1])

        try:
            print(img2pdf.input_images(list_of_files[0]))
            print("[Debug]Converted images to pdf")
            #write all the iamges to the pdf
            f.write(img2pdf.convert(list_of_files))
            #print the successfully converted pdf file
            print("[Debug]Saved pdf " + pdf_to_save.split(delimiter)[-1])
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
'''        

#the main block
if __name__ == "__main__":
    main()
    
    

    