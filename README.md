# Compare Directories
Compare two similar directories and find missing/changed files.
## Usage
Run the front.py file. Fill in file paths in the two entry boxes and press load. The program will search through both paths.

The idea is that the user wants to keep the first directory and delete the second one. So the program finds files in the second directory that is not present in the first, but not the other way around. If the reverse is desired, the user can simply press the 'swap' button. The program will also show all files that was found in both directories but has been changed (has different sizes).

The user can then remove or move the files found by pressing buttons. Move will put the files from the second directory in a similar place in the first directory.
