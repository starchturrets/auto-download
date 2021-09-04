import os
import shutil
import re
import ocrmypdf
import natsort
import os.path


def main():
    dir_main = '/home/james/programming/auto-download/files'
    new_dir = '/home/james/programming/auto-download/new-pdfs'
    print('CONVERT ZEH PLANETARY DEFENCE FORCE FOR TEH EMPEROR')

    def folder(dir):
        print('converting all files inside a folder')
        name = str(dir).rsplit('/', 1)
        name = name[len(name) - 1]
        print(name)
        # os.chdir(dir_main)
        if os.path.exists(os.path.join(new_dir, name)) == False:
            os.makedirs(os.path.join(new_dir, name))
        # os.chdir(dir)
        for filename in os.listdir(dir):
            print(filename)
            # print('Simulating conversion...')
            ocrmypdf.ocr(filename, new_dir + '/' +
                         name + '/' + filename)
    directories = [os.path.abspath(x[0]) for x in os.walk(dir_main)]
    directories.remove(os.path.abspath(dir_main))

    for directory in directories:
        os.chdir(directory)
        folder(directory)


main()
