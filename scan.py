import os
import sys
from os.path import join, getsize
dir1 = "/home/albin/Documents"
dir2 = "/home/albin/Documents2"

if dir1 == dir2:
    sys.exit("Du måste ange olika sökvägar")

def folder_name(path):
    """Get just name of folder intead of entire path."""
    if path[-1] == '/':
        return ""
    else:
        return folder_name(path[:-1]) + path[-1]

# Create dictonarys with filenames and filesizes
save = [{}, {}]
for i, dir in enumerate([dir1, dir2]):
    for root, dirs, files in os.walk(dir):
        dirfiles = []
        for name in files:
            size = getsize(join(root, name))
            dirfiles.append((name, size))
        save[i][folder_name(root)] = dirfiles
        if 'CVS' in dirs:
            dirs.remove('CVS')  # don't visit CVS directories
print(save)

# Compare dictonarys
for folder1 in save[0]:
    pass
