import tkinter as tk
import os

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

        self.create_frames(Home)

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

class Home(tk.Frame):
    """The home window."""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.msg = tk.StringVar()
        self.msg.set("Please input the paths you want to compare")
        tk.Label(self, textvar=self.msg).pack()

        path_input = tk.Frame(self)
        tk.Label(path_input, text="Main path:").grid(row=0, column=0)
        tk.Label(path_input, text="Path to compare:").grid(row=1, column=0)
        self.main_path_entry = tk.Entry(path_input)
        self.main_path_entry.grid(row=0, column=1)
        self.comp_path_entry = tk.Entry(path_input)
        self.comp_path_entry.grid(row=1, column=1)
        path_input.pack()

        tk.Button(self, text="Done", command=self.done).pack()

    def done(self):
        """Button click."""
        passed = True
        for entry in (self.main_path_entry, self.comp_path_entry):
            entry["foreground"] = "black"
            path = entry.get()
            if not os.path.exists(path):
                entry["foreground"] = "red"
                passed = False
                self.msg.set("Please make sure the paths exists")
        if passed:
            self.controller.main_path = self.main_path_entry.get()
            self.controller.comp_path = self.comp_path_entry.get()
            self.destroy()
            self.controller.create_frames(ComparePaths)
            self.controller.show_frame(ComparePaths)

class ComparePaths(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Comparing paths").pack()

if __name__ == "__main__":
    Windows()
