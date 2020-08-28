from os import walk

f = []
for (dirpath, dirnames, filenames) in walk('./files'):
    f.extend(filenames)
    break

print(f)
