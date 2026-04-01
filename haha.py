"""
haha.py - Nelson Muntz prank popup.

Sits silently in the background and pops up a "HA HA!" GIF every
3–15 minutes (random).  The window has no title bar or close button;
it closes itself after one full GIF loop so the victim can't dismiss it.

Kill it the normal way: Task Manager -> End Task on "haha.exe"
(or "python.exe" when running as a script).
"""

import os
import random
import sys
import threading
import time
import tkinter as tk

from PIL import Image, ImageTk


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def resource_path(name: str) -> str:
    """Return absolute path to a bundled resource (works dev + PyInstaller)."""
    if hasattr(sys, "_MEIPASS"):           # PyInstaller temp folder
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, name)


# ---------------------------------------------------------------------------
# Auto-startup (Windows registry, no admin required)
# ---------------------------------------------------------------------------

def install_autostart() -> None:
    """Add this exe to HKCU Run so it starts automatically at Windows login.

    Uses HKEY_CURRENT_USER so no admin rights are needed.
    Only runs when launched as a compiled exe (not as a .py script).
    Safe to call every launch — it just overwrites the same value.
    """
    if sys.platform != "win32":
        return
    if not getattr(sys, "frozen", False):   # only when built by PyInstaller
        return
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE,
        )
        winreg.SetValueEx(key, "HaHa", 0, winreg.REG_SZ, f'"{sys.executable}"')
        winreg.CloseKey(key)
    except Exception:
        pass  # silently skip if registry write fails


# ---------------------------------------------------------------------------
# Sound
# ---------------------------------------------------------------------------

def play_sound() -> None:
    """Speak 'HA HA!' using the Windows built-in TTS voice."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("rate", 95)       # slow and obnoxious
        engine.setProperty("volume", 1.0)
        engine.say("HA   HA!")               # extra space = brief pause between HAs
        engine.runAndWait()
        engine.stop()
    except Exception:
        pass  # no sound is fine – visual prank still works


# ---------------------------------------------------------------------------
# Popup logic
# ---------------------------------------------------------------------------

def show_haha() -> None:
    """Open a borderless, always-on-top popup, play GIF once, then close."""
    gif_path = resource_path("haha.gif")

    root = tk.Tk()
    root.withdraw()            # hide the invisible root window

    popup = tk.Toplevel(root)
    popup.overrideredirect(True)           # no title bar, no close button
    popup.attributes("-topmost", True)     # always on top of everything
    popup.configure(bg="black")

    # Block every keyboard shortcut that might close the window
    for seq in ("<Alt-F4>", "<Control-w>", "<Control-F4>", "<Escape>"):
        popup.bind(seq, lambda e: "break")

    # Also intercept the WM_DELETE_WINDOW protocol (belt-and-suspenders)
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    # ---- Load GIF frames ----
    gif = Image.open(gif_path)
    frames: list[ImageTk.PhotoImage] = []
    durations: list[int] = []

    try:
        while True:
            frames.append(ImageTk.PhotoImage(gif.copy().convert("RGBA")))
            durations.append(gif.info.get("duration", 100))
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    if not frames:
        root.destroy()
        return

    # ---- Size & centre the popup ----
    w, h = gif.size
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    popup.geometry(f"{w}x{h}+{x}+{y}")

    label = tk.Label(popup, bd=0, bg="black")
    label.pack(fill="both", expand=True)

    # ---- Animate ----
    n = len(frames)

    def animate(idx: int = 0) -> None:
        label.configure(image=frames[idx])
        popup.after(durations[idx], animate, (idx + 1) % n)

    animate()
    popup.focus_force()

    # Fire sound in background so it doesn't block the animation
    threading.Thread(target=play_sound, daemon=True).start()

    # Auto-destroy after exactly one full loop
    one_loop_ms = sum(durations)
    popup.after(one_loop_ms, root.destroy)

    root.mainloop()


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

MIN_WAIT_SEC = 3 * 60    # 3 minutes
MAX_WAIT_SEC = 15 * 60   # 15 minutes
FIRST_SHOW_SEC = 10      # show quickly on first run so you know it's working


def main() -> None:
    # Register in Windows startup (no-op if not a compiled exe or not Windows)
    install_autostart()

    # First appearance – quick so you can verify it's running
    time.sleep(FIRST_SHOW_SEC)
    show_haha()

    while True:
        wait = random.uniform(MIN_WAIT_SEC, MAX_WAIT_SEC)
        time.sleep(wait)
        show_haha()


if __name__ == "__main__":
    main()
