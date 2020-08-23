import os

DEBUG = False

class ComparePaths:
    """Find all files in one directory that is missing in another."""

    def __init__(self, main_path, comp_path):
        self.main_path = main_path
        self.comp_path = comp_path
        # Walk the paths
        main_list = self.get_files(self.main_path)
        comp_list = self.get_files(self.comp_path)

        if DEBUG:
            print("Main list:", main_list)
            print("\nComp list:", comp_list)
        # Find files in comp_list that isn't in main_list
        comp = comp_list.pop()
        main = main_list.pop()
        self.not_found = []
        self.changed = []
        print()
        print(comp, main)
        while comp_list:
            if comp < main:
                # comp is before in the que
                if main_list:
                    main = main_list.pop()
                else:
                    # main_list is empty
                    self.not_found.append(comp)
                    self.not_found += comp_list
                    comp_list = []
            elif comp > main:
                # comp is after in the que, comp was missed
                self.not_found.append(comp)
                comp = comp_list.pop()
            elif comp.name == main.name:
                # comp and main has the same name
                if comp.size != main.size:
                    self.changed.append((main, comp))
                if main_list:
                    comp = comp_list.pop()
                    main = main_list.pop()
                else:
                    # main_list is empty
                    comp_list = []

    @staticmethod
    def split(path, lst=None):
        """Split a path to a list."""
        empty = ("/", "\\", "")
        if lst == None:
            lst = []
        if path in empty:
            return lst
        new_path, base = os.path.split(path)
        if base in empty:
            return [new_path] + lst
        lst.insert(0, base)
        return ComparePaths.split(new_path, lst)

    def get_files(self, path):
        """Find all files in a path, return sorted list."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path {path} does not exist")
        lst = []
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                lst.append(File(filename, dirpath, self.main_path))
        return sorted(lst)

class File:
    """Store data for a file, is comparable."""

    def __init__(self, filename, dirpath, main_path):
        self.name = filename
        self.folder = os.path.basename(dirpath)
        self.size = os.path.getsize(os.path.join(dirpath, filename))
        self.dirpath = dirpath
        self.long_name = os.path.join(self.folder, self.name)
        self.full_name = os.path.join(self.dirpath, self.name)
        self.main_path = main_path  # Needed for self.move()

    def __lt__(self, other):
        if not isinstance(other, File):
            return TypeError(f"Cant compare File to {type(other)}")
        return self.name < other.name

    def __eq__(self, other):
        if not isinstance(other, File):
            return TypeError(f"Cant compare File to {type(other)}")
        if self.__repr__ == other.__repr__:
            return True
        else:
            return False


    def __repr__(self):
        return f"File({self.name}, {self.dirpath})"

    def __str__(self):
        return self.name

    def get_size(self):
        """Get size as a string with appropirate unit."""
        units = ("B", "KB", "MB", "GB", "TB")
        for i, unit in enumerate(units):
            high = 10**(i*3)
            if self.size < high*1000:
                return f"{round(self.size/high, 3)} {unit}"

    def delete(self):
        """Delete a file permanently, use with caution."""
        print("REMOVE", self.full_name)
        os.remove(self.full_name)

    def move(self):
        """Move a file from comp to appropirate folder in main."""
        # Find the best place to place file
        longest_common = ""
        long = 0
        for dirpath, dirnames, filenames in os.walk(self.main_path):
            current_common = os.path.commonpath([dirpath, self.full_name])
            cur_len = len(ComparePaths.split(current_common))
            if cur_len > long or (cur_len == long and \
               os.path.basename(self.dirpath) == os.path.basename(dirpath)):
                long = cur_len
                longest_common = dirpath
        # Move file
        new_path = os.path.join(longest_common, self.name)
        if os.path.isfile(new_path):
            os.remove(new_path)
            print("REMOVE", new_path)
        print("RENAME", self.full_name, new_path)
        os.rename(self.full_name, new_path)



if __name__ == "__main__":
    path = "D:\Documents"
    print(os.path.split(path))
    print(ComparePaths.split(path))
