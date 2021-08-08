import os
# import img2pdf
from PIL import Image
from PIL import ImageFile
import natsort
import re
ImageFile.LOAD_TRUNCATED_IMAGES = True
print('Creating PDF')
dirname = 'files/BIOLOGY/BIOLOGY M PART 1 (Textbook-Concepts and Sample Questions)' + '/'
title = 'BIOLOGY M PART 1 (Textbook-Concepts and Sample Questions)'
imgs = []
# for fname in sorted(os.listdir(dirname)):
#     print(fname)
#     if not fname.endswith('.png'):
#         continue
#     path = os.path.join(dirname, fname)
#     if os.path.isdir(path):
#         continue
#     im = Image.open(path)

#     if im.mode == 'RGBA':
#         print('Converting!')
#         im = im.convert('RGB')
#     imgs.append(im)
# imgs[0].save(dirname + title + '.pdf', save_all=True,
#              quality=100, append_images=imgs[1:])
# # for img in imgs:
# # img.convert('RGB')
# # with open(path + '.pdf', 'wb') as f:
# #     f.write(img2pdf.convert(imgs))
print(sorted(os.listdir(dirname)))


def sorted_alphanumeric(data):
    def convert(text): return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9+])', key)]
    return sorted(data, key=alphanum_key)


print(sorted_alphanumeric(os.listdir(dirname)))

arr = os.listdir(dirname)  # .sort(key=lambda f: int(re.sub('\D', '', f)))
print(natsort.natsorted((arr)))
