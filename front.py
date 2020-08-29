import tkinter as tk
import tkinter.font as tkfont
import os
import back

DEBUG = True


class Windows(tk.Tk):
    """Backend for window management."""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.title("Scan v. 2.0")
        self.frames = {}

        # Fonts
        self.default_font = tkfont.nametofont("TkDefaultFont")
        self.default_font.configure(size=11)
        self.large_font = tkfont.Font(family="Segoe UI", size=20,
                                      weight="bold")
        self.small_font = tkfont.Font(family="Segoe UI", size=10,
                                      weight="normal")

        self.create_frames(ComparePathsWindow)

        self.mainloop()

    def create_frames(self, *frames):
        """Create new frames and put them in the dictionary self.frames."""
        for frame_name in frames:
            frame = frame_name(self.container, self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, cont):
        """Show the frame of class cont."""
        frame = self.frames[cont]
        frame.tkraise()


class ComparePathsWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Comparing paths", font=controller.large_font) \
            .pack()

        paths = tk.Frame(self)
        entry_width = 50
        tk.Label(paths, text="Main path").grid(row=0, column=0)
        tk.Label(paths, text="Path to compare").grid(row=0, column=2)
        self.left_path = tk.Entry(paths, width=entry_width,
                                  font=controller.default_font)
        self.right_path = tk.Entry(paths, width=entry_width,
                                   font=controller.default_font)
        self.left_path.grid(row=1, column=0, padx=(10, 0))
        self.right_path.grid(row=1, column=2)
        tk.Button(paths, text="Swap", command=self.swap, width=5) \
            .grid(row=1, column=1, padx=5)
        self.load_str = tk.StringVar(value="Load")
        tk.Button(paths, textvariable=self.load_str,
                  command=self.load, width=5) \
            .grid(row=1, column=3, padx=(5, 0))
        paths.pack()

    @staticmethod
    def open_file(file):
        """Wrapper for opening a back.File file."""
        def func(path=file.full_name):
            os.startfile(path)
        return func

    def load(self):
        """Compare the paths and show the result."""
        self.load_str.set("Reload")
        paths = []
        for entry in (self.left_path, self.right_path):
            path = entry.get()
            if not os.path.exists(path):
                entry.config(foreground="red")
            else:
                entry.config(foreground="black")
                paths.append(path)
        if len(paths) != 2:
            return
        compare_paths = back.ComparePaths(paths[0], paths[1])
        try:
            self.bottom_container.destroy()
        except AttributeError:
            pass

        self.bottom_container = tk.Frame(self)

        bottom_head = tk.Frame(self.bottom_container)
        found_both_msg = f"Found {compare_paths.found_in_both} identical files"
        tk.Label(bottom_head, text=found_both_msg) \
            .pack(side="left", padx=100)
        tk.Button(bottom_head, text="Apply", command=self.apply) \
            .pack(side="right")
        bottom_head.pack(fill="both")

        bottom_body = tk.Frame(self.bottom_container)
        bottom_canvas = tk.Canvas(bottom_body)
        scrollbar = tk.Scrollbar(bottom_body, orient="vertical",
                                 command=bottom_canvas.yview)
        bottom = tk.Frame(bottom_canvas)
        bottom.bind("<Configure>",
                    lambda e: bottom_canvas.configure(
                        scrollregion=bottom_canvas.bbox("all"))
                    )
        bottom_canvas.create_window((0, 0), window=bottom, anchor="nw")
        bottom_canvas.configure(yscrollcommand=scrollbar.set)

        indent = (10, 0)
        width = 10
        m_len = self.controller.default_font.measure("m")
        label_width = m_len*30
        self.delete_buttons = {}
        self.to_delete = []
        self.keep_buttons = {}
        self.to_move = []
        # Missing files
        tk.Label(bottom, text="Missing files (from main):",
                 font=self.controller.large_font) \
            .grid(row=0, column=0, sticky="w", columnspan=2)
        i = 0  # Dont crash if compare_paths.not_found empty
        for i, file in enumerate(compare_paths.not_found, start=1):
            tk.Label(bottom, text=file.long_name, wraplength=label_width) \
                .grid(row=i, column=0, columnspan=2, sticky="w", padx=indent)
            tk.Button(bottom, text="Open",
                      command=self.open_file(file)) \
                .grid(row=i, column=2, sticky="we")
            self.keep_buttons[i] = tk.Button(bottom, text="Move",
                                             width=width,
                                             command=self.keep(file, i))
            self.keep_buttons[i].grid(row=i, column=4, sticky="we", padx=indent)
            self.delete_buttons[i] = tk.Button(bottom, text="Delete",
                                               command=self.add_to_delete(file, i))
            self.delete_buttons[i].grid(row=i, column=5, sticky="we")
        # Changed files
        tk.Label(bottom, text="Changed files:",
                 font=self.controller.large_font) \
                 .grid(row=i+1, column=0, sticky="w")
        for j, files in enumerate(compare_paths.changed, start=i+2):
            main, comp = files
            tk.Label(bottom, text=main, wraplength=label_width) \
                .grid(row=j, column=0, padx=indent, sticky="w")
            tk.Label(bottom, text=f"{main.get_size()}/{comp.get_size()}") \
                .grid(row=j, column=1)
            tk.Button(bottom, text="Open main",
                      command=self.open_file(main)) \
                .grid(row=j, column=2, sticky="we")
            tk.Button(bottom, text="Open other",
                      command=self.open_file(comp)) \
                .grid(row=j, column=3, sticky="we")
            self.keep_buttons[j] = {}
            self.keep_buttons[j]["main"] = tk.Button(bottom,
                                                     text="Keep main",
                                                     command=self.keep(files, j, "main"))
            self.keep_buttons[j]["main"].grid(row=j, column=4, padx=indent, sticky="we")
            self.keep_buttons[j]["comp"] = tk.Button(bottom, text="Keep other",
                                                     command=self.keep(files, j, "comp"))
            self.keep_buttons[j]["comp"].grid(row=j, column=5, sticky="we")
            self.delete_buttons[j] = tk.Button(bottom, text="Delete both",
                                               command=self.add_to_delete(files, j))
            self.delete_buttons[j].grid(row=j, column=6, sticky="we")
        for i in range(4):
            bottom.grid_columnconfigure(i, weight=1)
        bottom_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y", pady=5)
        bottom_body.pack(fill="both", expand=True)
        self.bottom_container.pack(fill="both", expand=True)

    def add_to_delete(self, files, id, check_row=True):
        """Mark a file for deletion, wrapper.

        If the file already is in the list, remove it from the list.
        The buttons relief will also change as an indicator of if it has been
        pressed.
        """
        def func(self=self, files=files, id=id, check_row=check_row):
            if check_row:
                # Check if any other button with same id is clicked.
                keep = self.keep_buttons[id]
                if isinstance(keep, dict):
                    for type_str in ("main", "comp"):
                        button = keep[type_str]
                        if button["relief"] == "sunken":
                            self.keep(files, id, type_str)()
                else:
                    if keep["relief"] == "sunken":
                        self.keep(files, id)()
            # Click this button
            button = self.delete_buttons[id]
            if isinstance(files, back.File):
                files = [files]
            if button["relief"] == "sunken":
                button["relief"] = "raised"
                for file in files:
                    i = self.to_delete.index(file)
                    del self.to_delete[i]
            else:
                self.delete_buttons[id]["relief"] = "sunken"
                for file in files:
                    self.to_delete.append(file)
            if DEBUG:
                print("\nM", self.to_move)
                print("D", self.to_delete)
        return func

    def apply(self):
        """Apply all changes requested by the user, delete and remove files."""
        def yes(root, self=self):
            for file in self.to_delete:
                file.delete()
            for file in self.to_move:
                file.move()
            self.load()
            root.destroy()

        font = ("Segoe UI", 11)
        num_of_files = len(self.to_delete + self.to_move)
        if num_of_files == 0:
            return
        popup = tk.Tk()
        msg = "This will delete/move {} file(s). Are you sure?"
        tk.Label(popup, text=msg.format(num_of_files), font=font) \
            .grid(row=0, column=0, columnspan=2)
        tk.Button(popup, text="Yes", font=font, command=lambda: yes(popup)) \
            .grid(row=1, column=0, sticky="we")
        tk.Button(popup, text="No", default="active", font=font,
                  command=popup.destroy) \
            .grid(row=1, column=1, sticky="we")

    def keep(self, files, id, type_=None):
        """Keep this file and remove alternetives, wrapper.

        Arguments:
        * files: A back.File instance, or a list of two
        * id: A number uniqe for every row
        * type_: None, 'main' or 'comp'. Is the file that this button
                 represents from main or comp. None if only one version
                 avalible (comp)."""

        def func(self=self, files=files, id=id, type_=type_):
            if type_ is None:
                button = self.keep_buttons[id]
            else:
                if type_ == "main":
                    other_type = "comp"
                elif type_ == "comp":
                    other_type = "main"
                button = self.keep_buttons[id][type_]
                other_button = self.keep_buttons[id][other_type]
                if other_button["relief"] == "sunken":
                    # Button must be unclicked
                    click(self, other_button, files, other_type)
            if self.delete_buttons[id]["relief"] == "sunken":
                # Button must be unclicked
                self.add_to_delete(files, id, check_row=False)()
            # Click this button
            click(self, button, files, type_)
            if DEBUG:
                print("\nM", self.to_move)
                print("D", self.to_delete)

        def click(self, button, files, type_):
            if type_ is None:
                comp = files
            else:
                main, comp = files
            if button["relief"] == "raised":
                # The button has not been pressed before
                button["relief"] = "sunken"
                if type_ == "main":
                    # Delete comp
                    self.to_delete.append(comp)
                elif type_ == "comp" or type_ is None:
                    # Move comp to main path
                    self.to_move.append(comp)
            elif button["relief"] == "sunken":
                button["relief"] = "raised"
                if type_ == "main":
                    i = self.to_delete.index(comp)
                    del self.to_delete[i]
                elif type_ == "comp" or type_ is None:
                    i = self.to_move.index(comp)
                    del self.to_move[i]

        return func

    def swap(self):
        """Swap the text of the two entrys."""
        self.load_str.set("Load")
        old_left = self.left_path.get()
        old_right = self.right_path.get()
        self.left_path.delete(0, "end")
        self.right_path.delete(0, "end")
        self.left_path.insert(0, old_right)
        self.right_path.insert(0, old_left)


if __name__ == "__main__":
    Windows()
