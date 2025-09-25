import os
import shutil

from text2html import generate_page, generate_pages_recursive


def copy_files_recursively(source, destination):
    if os.path.exists(source) and not os.path.isfile(source):
        if not os.path.exists(destination):
            os.mkdir(destination)
        for file_or_folder in os.listdir(source):
            if not os.path.isfile(os.path.join(source, file_or_folder)):
                os.mkdir(os.path.join(destination, file_or_folder))
                copy_files_recursively(os.path.join(source, file_or_folder), os.path.join(destination, file_or_folder))
            else: shutil.copy(os.path.join(source, file_or_folder), os.path.join(destination, file_or_folder))
    else: shutil.copy(source, destination)

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
   
    copy_files_recursively("static", "public")

    #generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")


main()