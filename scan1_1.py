import os
import sys
from sys import platform
from os.path import join, getsize
import argparse

def folder_name(path):
    """Get just name of folder intead of entire path."""
    if platform == 'linux':
        slash = '/'
    elif platform == 'win32':
        slash = '\\'
    if path[-1] == slash:
        return ""
    else:
        return folder_name(path[:-1]) + path[-1]

def readable_size(number):
    if 0 <= number < 1000:
        return "{} B".format(number)
    if 1000 <= number < 1000000:
        return "{} kB".format(round(number/1000, 2))
    if 1000000 <= number < 1000000000:
        return "{} MB".format(round(number/1000000, 2))
    if 1000000000 <= number:
        return "{} MB".format(round(number/1000000, 2))

def main():
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
        missing_folders = []
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
                        folder_log.append(f" Fil {name1} har modifierats ({readable_size(size1)}/{readable_size(size2)})")
                        found = True
                        break
                if not found:
                    folder_log.append(f" Fil {name1} ({readable_size(size1)}) saknas på {dir2}")
        else:
            missing_folders.append(f" {folder1} ({len(files1)} filer)")
        if folder_log: #  Don't list folders where nothing is wrong
            total_log.append("Mapp " + folder1 + "\n" + "\n".join(folder_log))
    if missing_folders:
        folder_msg = f"Mappar som saknas i {dir2}\n" + "\n".join(missing_folders)
    else:
        folder_msg = f"Inga mappar på {dir1} saknades på {dir2}"
    if total_log:
        files_msg = "Filer som saknas/har modifierats i {}\n{}".format(dir2, "\n".join(total_log))
    else:
        files_msg = f"Inga filer på {dir1} saknades på {dir2}"
    print(folder_msg)
    print(files_msg)
    print()

if __name__ == '__main__':
    f = open('message.txt')
    lines = f.readlines()
    f.close()
    print("".join(lines))
    while True:
        directories = input("Vilka sökvägar vill du jämföra? [sökvägar/f/q]: ")
        if directories == 'q':
            sys.exit()
        if directories == 'f':
            f = open("paths.txt")
            lst_of_dir = f.readlines()
            f.close()
            [print(f"({i+1}) {path}") for i, path in enumerate(lst_of_dir)]
            while True:
                inp = input("Vilka sökvägar vill du använda?: ")
                try:
                    directories = lst_of_dir[int(inp) - 1]
                    break
                except ValueError:
                    print("Ange en siffra")
                except IndexError:
                    print("Angiven siffra ej tilljänglig")
        directories = directories.split(" ")
        if len(directories) != 2:
            print("Du måste ange 2 sökvägar.")
            continue
        dir1, dir2 = directories
        if not os.path.exists(dir1):
            print(f"Sökvägen {dir1} finns inte")
        if not os.path.exists(dir2):
            print(f"Sökvägen {dir2} finns inte")
        if (not os.path.exists(dir1)) or (not os.path.exists(dir2)):
            continue
        if dir1 == dir2:
            print("Du måste ange olika sökvägar.")
            continue
        while True:
            inp = input(f"\nVill du jämföra {dir1} med {dir2}? [J/n/b]: ")
            if inp == 'n':
                break
            if inp == 'q':
                sys.exit()
            if inp == 'b':
                dir1, dir2 = dir2, dir1
                continue
            main()
