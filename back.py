import os

class ComparePaths:
    """Find all files in one directory that is missing in another."""

    def __init__(self, main_path, comp_path):
        self.main_path = main_path
        self.comp_path = comp_path
        # Find basepath
        lst1 = self.split(main_path)
        lst2 = self.split(comp_path)
        # while True:
        #     if lst1[0]

        # Walk the main path
        main_list = []
        for dirpath, dirnames, filenames in os.walk(self.main_path):
            for filename in filenames:
                main_list.append(self.get_data(filename, dirpath))

    def get_data(filename, dirpath):
        """Create a dictonary with all data needed for this file."""
        data = {"name": filename}
        return data

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

if __name__ == "__main__":
    test_path_1 = "/home/albin/Documents/text.txt"
    print(ComparePaths.split(test_path_1))
