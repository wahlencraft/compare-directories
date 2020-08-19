import os

class ComparePaths:
    """Find all files in one directory that is missing in another."""

    def __init__(self, main_path, comp_path):
        self.main_path = main_path
        self.comp_path = comp_path
        # Walk the paths
        main_list = self.get_files(self.main_path)
        comp_list = self.get_files(self.comp_path)

        print(main_list, "\n\n", comp_list)
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
            elif comp == main:
                # comp and main has the same name
                if comp.size != main.size:
                    self.changed.append(comp)
                comp = comp_list.pop()
                main = main_list.pop()
        print("Not found:\n", self.not_found)
        print("\nDifferent size:\n", self.changed)

    @staticmethod
    def get_files(path):
        """Find all files in a path, return sorted list."""
        lst = []
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                lst.append(File(filename, dirpath))
        return sorted(lst)

    @staticmethod
    def split(path, lst=None):
        """Split a path to a list."""
        if lst == None:
            lst = []
        if path in ("/", "\\", ""):
            return lst
        new_path, base = os.path.split(path)
        lst.insert(0, base)
        return ComparePaths.split(new_path, lst)

class File:
    """Store data for a file, is comparable."""

    def __init__(self, filename, dirpath):
        self.name = filename
        self.folder = os.path.basename(dirpath)
        self.size = os.path.getsize(os.path.join(dirpath, filename))
        self.dirpath = dirpath

    def __lt__(self, other):
        if not isinstance(other, File):
            return TypeError(f"Cant compare File to {type(other)}")
        return self.name < other.name

    def __eq__(self, other):
        if not isinstance(other, File):
            return TypeError(f"Cant compare File to {type(other)}")
        return self.name == other.name


    def __repr__(self):
        return f"File({self.name}, {self.dirpath})"

    def __str__(self):
        return self.name



if __name__ == "__main__":
    import cProfile

    test_path_1 = "/media/albin/HDD/Documents/Ämnen (old)"
    test_path_2 = "/media/albin/HDD/Documents/Ämnen"
    cProfile.run("ComparePaths(test_path_2, test_path_1)")
