import os
import shutil
import sys

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
    if sys.argv[1]:
        basepath = sys.argv[1]
    else:
        basepath = "/"


    #if os.path.exists("public"):
    #    shutil.rmtree("public")
    if os.path.exists("docs"):
        shutil.rmtree("docs")
   
    #copy_files_recursively("static", "public")
    copy_files_recursively("static", "docs")

    #generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "docs", basepath)


main()