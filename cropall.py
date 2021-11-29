from PIL import Image
import os.path
import sys


def crop():
    path = '/home/james/programming/auto-download/screenshots/'
    dirs = os.listdir(path)

    for item in dirs:
        print("sus")
        fullpath = os.path.join(path, item)
        if os.path.isfile(fullpath):
            im = Image.open(fullpath)
            f, e = os.path.splitext(fullpath)
            print(item)
            imcrop = im.crop((447, 179, 1903, 1080))
            imcrop.save(f+'.png', 'PNG', quality=100)


crop()
