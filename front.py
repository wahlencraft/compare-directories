import tkinter as tk
import os
from back import ComparePaths

class Windows(tk.Tk):
    """Backend for window management."""
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
        self.left_path.insert(0, "/media/albin/HDD/Documents/Ämnen")
        self.right_path.insert(0, "/media/albin/HDD/Documents/Ämnen (old)")
        self.left_path.grid(row=1, column=0)
        self.right_path.grid(row=1, column=2)
        tk.Button(paths, text="Swap", command=self.swap) \
            .grid(row=1, column=1)
        tk.Button(paths, text="Reload", command=self.reload) \
            .grid(row=1, column=3)
        paths.pack()

    def reload(self):
        pass

    def swap(self):
        """Swap the text of the two entrys."""
        old_left = self.left_path.get()
        old_right = self.right_path.get()
        self.left_path.delete(0, "end")
        self.right_path.delete(0, "end")
        self.left_path.insert(0, old_right)
        self.right_path.insert(0, old_left)



if __name__ == "__main__":
    Windows()
