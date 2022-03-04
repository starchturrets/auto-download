from PIL import Image
import os.path
import sys


def crop():
    path = '/home/james/programming/auto-download/screenshots/test'
    dirs = os.listdir(path)
    for item in dirs:
        # print(item)
        fullpath = os.path.join(path, item)
        if os.path.isfile(fullpath):
            f, e = os.path.splitext(fullpath)
            im = Image.open(fullpath)
            width, height = im.size
            # print(item)
            imcrop = im.crop((310, 0, width, height))
            imcrop.save(f+'.png', 'PNG', quality=100)


crop()
