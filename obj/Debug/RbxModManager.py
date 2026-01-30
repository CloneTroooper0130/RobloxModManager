import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import shutil
import os
import sys
from PIL import Image, ImageTk

INTRO_DURATION = 2500
PROGRESS_STEPS = 100

class RobloxModManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Roblox Mod Manager")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        self.intro_frame = tk.Frame(root)
        self.main_frame = tk.Frame(root)

        self.progress_value = 0

        self.create_intro()
        self.create_main_ui()

        self.intro_frame.pack(fill="both", expand=True)
        self.update_progress()

    # ---------- INTRO SCREEN ----------
    def create_intro(self):
        # Path handling for EXE or script
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(sys.argv[0]))

        image_path = os.path.join(base_path, "intro.png")

        # Load PNG safely
        image = Image.open(image_path)
        image = image.resize((500, 220), Image.LANCZOS)
        self.intro_image = ImageTk.PhotoImage(image)

        tk.Label(self.intro_frame, image=self.intro_image).pack()

        # Green progress bar
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Green.Horizontal.TProgressbar",
            troughcolor="#dddddd",
            background="#4CAF50",
            thickness=12
        )

        self.progress = ttk.Progressbar(
            self.intro_frame,
            style="Green.Horizontal.TProgressbar",
            orient="horizontal",
            length=400,
            mode="determinate",
            maximum=100
        )
        self.progress.pack(pady=15)

    def update_progress(self):
        step_time = INTRO_DURATION // PROGRESS_STEPS
        if self.progress_value < 100:
            self.progress_value += 1
            self.progress["value"] = self.progress_value
            self.root.after(step_time, self.update_progress)
        else:
            self.show_main()

    def show_main(self):
        self.intro_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)

    # ---------- MAIN UI ----------
    def create_main_ui(self):
        self.original_path = tk.StringVar()
        self.new_texture_path = tk.StringVar()

        tk.Label(
            self.main_frame,
            text="Roblox Mod Manager",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        tk.Label(self.main_frame, text="Original Texture File:").pack()
        tk.Entry(
            self.main_frame,
            textvariable=self.original_path,
            width=60
        ).pack()
        tk.Button(
            self.main_frame,
            text="Browse",
            command=self.select_original
        ).pack(pady=5)

        tk.Label(self.main_frame, text="New Texture File:").pack()
        tk.Entry(
            self.main_frame,
            textvariable=self.new_texture_path,
            width=60
        ).pack()
        tk.Button(
            self.main_frame,
            text="Browse",
            command=self.select_new
        ).pack(pady=5)

        tk.Button(
            self.main_frame,
            text="Apply Mod",
            command=self.apply_mod,
            bg="#6fa8dc",
            fg="white",
            width=20
        ).pack(pady=15)

    # ---------- LOGIC ----------
    def select_original(self):
        path = filedialog.askopenfilename(title="Select Original Texture")
        if path:
            self.original_path.set(path)

    def select_new(self):
        path = filedialog.askopenfilename(title="Select New Texture Image")
        if path:
            self.new_texture_path.set(path)

    def apply_mod(self):
        original = self.original_path.get()
        new_texture = self.new_texture_path.get()

        if not original or not new_texture:
            messagebox.showerror("Error", "Please select both files.")
            return

        try:
            backup = original + ".backup"
            if not os.path.exists(backup):
                shutil.copy2(original, backup)

            shutil.copy2(new_texture, original)

            messagebox.showinfo(
                "Success",
                "Texture replaced successfully!"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()

    # ---------- Window Icon ----------
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))

    icon_path = os.path.join(base_path, "applogo.ico")  # or "applogo.png"
    try:
        img = Image.open(icon_path)
        tk_icon = ImageTk.PhotoImage(img)
        root.iconphoto(False, tk_icon)
    except Exception as e:
        print("Could not set window icon:", e)

    app = RobloxModManager(root)
    root.mainloop()
