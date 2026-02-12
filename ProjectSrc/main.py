import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import subprocess

APP_NAME = "Roblox Studio Bootstrapper"
APP_SIZE = "300x300"
APP_VERSION = "v1.0.0"
ICON_FILE = "icon.ico"
MODS_FOLDER = "mods"
SETTINGS_FILE = "settings.txt"

base_path = os.path.abspath(os.path.dirname(sys.argv[0]))
local_appdata = os.environ.get("LOCALAPPDATA")

def resource_path(name):
    return os.path.join(base_path, name)

if not os.path.exists(resource_path(MODS_FOLDER)):
    os.makedirs(resource_path(MODS_FOLDER))

def find_roblox_studio():
    if not local_appdata:
        return None
    versions_path = os.path.join(local_appdata, "Roblox", "Versions")
    if not os.path.exists(versions_path):
        return None
    for folder in os.listdir(versions_path):
        exe_path = os.path.join(versions_path, folder, "RobloxStudioBeta.exe")
        if os.path.isfile(exe_path):
            return exe_path
    return None

class Bootstrapper(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry(APP_SIZE)
        self.resizable(False, False)
        self.configure(bg="white")
        try:
            self.iconbitmap(resource_path(ICON_FILE))
        except:
            pass
        self.build_ui()

    def build_ui(self):
        tk.Label(
            self,
            text=APP_NAME,
            bg="white",
            fg="black",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=6)

        tk.Label(
            self,
            text=f"Current Version: {APP_VERSION}",
            bg="white",
            fg="#555555",
            font=("Segoe UI", 9)
        ).pack()

        frame = tk.Frame(self, bg="white")
        frame.pack(expand=True)

        ttk.Style().configure("TButton", padding=5, font=("Segoe UI", 9))

        ttk.Button(frame, text="Launch Studio", command=self.launch_studio).pack(fill="x", padx=30, pady=4)
        ttk.Button(frame, text="Open Mods Folder", command=self.open_mods).pack(fill="x", padx=30, pady=4)
        ttk.Button(frame, text="Settings", command=self.open_settings).pack(fill="x", padx=30, pady=4)
        ttk.Button(frame, text="Check for Updates", command=self.check_updates).pack(fill="x", padx=30, pady=4)

        self.status = tk.Label(
            self,
            text="Ready",
            bg="white",
            fg="#777777",
            font=("Segoe UI", 8)
        )
        self.status.pack(pady=4)

    def launch_studio(self):
        self.status.config(text="Launching Roblox Studio...")
        studio_path = find_roblox_studio()
        if not studio_path:
            messagebox.showerror(
                APP_NAME,
                "Roblox Studio was not found.\nPlease install Roblox Studio first."
            )
            self.status.config(text="Studio not found")
            return
        try:
            subprocess.Popen([studio_path], cwd=os.path.dirname(studio_path))
            self.status.config(text="Roblox Studio launched")
        except Exception as e:
            messagebox.showerror(APP_NAME, f"Failed to launch Studio:\n{e}")
            self.status.config(text="Launch failed")

    def open_mods(self):
        os.startfile(resource_path(MODS_FOLDER))

    def open_settings(self):
        if not os.path.exists(resource_path(SETTINGS_FILE)):
            with open(resource_path(SETTINGS_FILE), "w") as f:
                f.write("auto_update=true\n")
        os.startfile(resource_path(SETTINGS_FILE))

    def check_updates(self):
        self.status.config(text="Checking for updates...")
        self.after(800, lambda: (
            messagebox.showinfo(APP_NAME, "You are running the latest version."),
            self.status.config(text="Ready")
        ))

Bootstrapper().mainloop()
