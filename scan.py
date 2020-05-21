import os
import sys
from os.path import join, getsize
dir2 = "/home/albin/Documents"
dir1 = "/home/albin/Documents2"

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
        if root in (dir1, dir2):
            # Highest level will always have different names
            save[i]["root"] = dirfiles
        elif folder_name(root) in save[i].keys():
            # Avoid dublicate names
            save[i][root] = dirfiles
        else:
            save[i][folder_name(root)] = dirfiles
        if 'CVS' in dirs:
            dirs.remove('CVS')  # don't visit CVS directories

# Compare dictonarys
total_log = []
for folder1 in save[0].keys():
    files1 = save[0][folder1]
    folder_log = []
    if folder1 in save[1].keys():
        # Compare files in folders
        files2 = save[1][folder1]
        for name1, size1 in files1:
            found = False
            for name2, size2 in files2:
                if name1 == name2 and size1 == size2:
                    found = True
                    break
                elif name1 == name2:
                    folder_log.append(f" Fil {name1} har modifierats")
                    found = True
                    break
            if not found:
                folder_log.append(f" Fil {name1} fanns inte på {dir2}")
    else:
        folder_log.append(f" Mapp {folder1} ({len(files1)} filer) från {dir1} saknas på {dir2}")
    if folder_log: #  Don't list folders where nothing is wrong
        total_log.append(folder1 + "\n" + "\n".join(folder_log))

msg = "\n".join(total_log)
if msg:
    print(msg)
else:
    print(f"Inga filer på {folder1} saknades på {folder2}")
