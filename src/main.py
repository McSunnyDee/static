import os
import shutil


def clone_directory(source, destination):
    print(source)
    print(destination)
    if os.path.exists(source) and not os.path.isfile(source):
        for file_or_folder in os.listdir(source):
            if os.path.isfile(file_or_folder):
                shutil.copy(os.path.join(source, file_or_folder), os.path.join(destination, file_or_folder))
            elif not os.path.isfile(file_or_folder):
                #os.mkdir(os.path.join(destination, file_or_folder))
                pass
'''
    #if a path exists
    if os.path.exists(source):
        #is file
        if os.path.isfile(source) and not os.path.exists(destination):
            shutil.copy(source, destination)
        #is directory
        else:
            #check the directory for more files and folders...
            print(os.listdir(source))
            for file_or_folder in os.listdir(source):
                source_file_or_folder = os.path.join(source, file_or_folder)
                destination_file_or_folder = os.path.join(destination, file_or_folder)
                if not os.path.isfile(file_or_folder):
                    return clone_directory(source_file_or_folder, destination_file_or_folder)
                shutil.copy(source_file_or_folder, destination_file_or_folder)
'''


def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
        os.mkdir("public")
    else: os.mkdir("public")

    #print(os.listdir("static"))
    clone_directory("static", "public")



main()