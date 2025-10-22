import tkinter as tk
from tkinter import messagebox
import requests
import os
import sys
import subprocess

# === SETTINGS ===
APP_NAME = "MyApp"
LOCAL_VERSION = "1.0.0"
VERSION_URL = "https://raw.githubusercontent.com/YourUser/YourRepo/main/version.txt"
UPDATE_URL = "https://github.com/YourUser/YourRepo/releases/latest/download/MyAppInstaller.exe"
DOWNLOAD_PATH = "MyAppInstaller.exe"


def get_latest_version():
    """Check the latest version number from the online file."""
    try:
        response = requests.get(VERSION_URL, timeout=5)
        if response.status_code == 200:
            return response.text.strip()
    except Exception as e:
        print(f"Error checking version: {e}")
    return None


def download_update():
    """Download and run the update file."""
    try:
        messagebox.showinfo("Updating", "Downloading the latest version...")
        response = requests.get(UPDATE_URL, stream=True)
        total = int(response.headers.get('content-length', 0))
        with open(DOWNLOAD_PATH, "wb") as f:
            for data in response.iter_content(1024):
                f.write(data)

        messagebox.showinfo("Update Complete", "Download finished. The installer will now run.")
        subprocess.Popen(DOWNLOAD_PATH, shell=True)
        sys.exit(0)

    except Exception as e:
        messagebox.showerror("Error", f"Update failed:\n{e}")


def main():
    latest = get_latest_version()
    if not latest:
        messagebox.showwarning("Update Check", "Could not check for updates.")
        return

    if latest != LOCAL_VERSION:
        root = tk.Tk()
        root.withdraw()  # Hide main window
        if messagebox.askyesno(
            f"{APP_NAME} Update",
            f"A new version ({latest}) is available!\n\n"
            f"You are running {LOCAL_VERSION}.\n\n"
            "Would you like to update now?"
        ):
            download_update()
        else:
            messagebox.showinfo("Reminder", "You can update later from the settings menu.")
    else:
        messagebox.showinfo("Up to Date", f"{APP_NAME} is up to date!")


if __name__ == "__main__":
    main()
