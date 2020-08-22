import tkinter as tk
import os
from back import ComparePaths

class Windows(tk.Tk):
    """Backend for window management."""

    large_font = ("Courier Bold", 20)
    small_font = ("Courier", 10)

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.title("Scan V 2.0")
        self.frames = {}

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

        tk.Label(self, text="Comparing paths").pack()

        paths = tk.Frame(self)
        entry_width = 40
        tk.Label(paths, text="Main path").grid(row=0, column=0)
        tk.Label(paths, text="Path to compare").grid(row=0, column=2)
        self.left_path = tk.Entry(paths, width=entry_width)
        self.right_path = tk.Entry(paths, width=entry_width)
        # REMOVE, temporary for testing
        self.left_path.insert(0, "D:\Documents\Ämnen")
        self.right_path.insert(0, "D:\Documents\Ämnen (old)")
        self.left_path.grid(row=1, column=0)
        self.right_path.grid(row=1, column=2)
        tk.Button(paths, text="Swap", command=self.swap) \
            .grid(row=1, column=1)
        self.load_str = tk.StringVar(value="Load")
        tk.Button(paths, textvariable=self.load_str, command=self.load) \
            .grid(row=1, column=3)
        paths.pack()

    def load(self):
        """Start the commaparison."""
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
        compare_paths = ComparePaths(paths[0], paths[1])
        try:
            self.bottom.destroy()
        except AttributeError:
            pass
        self.bottom = tk.Frame(self)
        indent = (10, 0)
        # Missing files
        tk.Label(self.bottom, text="Missing files (in main):",
                 font=self.controller.large_font) \
                 .grid(row=0, column=0, sticky="w")
        for i, file in enumerate(compare_paths.not_found, start=1):
            tk.Label(self.bottom, text=file.long_name) \
                .grid(row=i, column=0, sticky="w", padx=indent)
            tk.Button(self.bottom, text="Open",
                      font=self.controller.small_font, pady=0,
                      command=self.open_file(file)).grid(row=i, column=1)
        # Changed files
        tk.Label(self.bottom, text="Changed files:",
                 font=self.controller.large_font) \
                 .grid(row=i+1, column=0, sticky="w")
        for j, (main, comp) in enumerate(compare_paths.changed, start=i+2):
            tk.Label(self.bottom, text=main) \
                .grid(row=j, column=0, padx=indent, sticky="w")
            tk.Label(self.bottom, text=f"{main.get_size()}/{comp.get_size()}") \
                .grid(row=j, column=1)
        self.bottom.pack(fill="both")

    def swap(self):
        """Swap the text of the two entrys."""
        old_left = self.left_path.get()
        old_right = self.right_path.get()
        self.left_path.delete(0, "end")
        self.right_path.delete(0, "end")
        self.left_path.insert(0, old_right)
        self.right_path.insert(0, old_left)

    @staticmethod
    def open_file(file):
        """Wrapper for opening a back.File file."""
        path = file.full_name
        def func(path=path):
            os.startfile(path)
        return func




if __name__ == "__main__":
    Windows()
