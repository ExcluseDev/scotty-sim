#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MELODIUS - FREDERIC DORIAN BEER RANSOM SIMULATOR (MAXIMUM TERROR)
"""

from __future__ import annotations
import argparse, atexit, hashlib, json, os, platform, random, subprocess, sys, threading, time, urllib.request, webbrowser, tempfile

try:
    import tkinter as tk
except Exception:
    sys.exit("tkinter is not available. Install python3-tk.")

APP_TITLE = "MELODIUS // SYSTEM LOCKED"
DEFAULT_MINUTES = 15
MAX_FILES = 3000
HERE = os.path.dirname(os.path.abspath(__file__))
BACKUP_PATH = os.path.join(HERE, "sim_wallpaper_backup.json")
KILL_PATH = os.path.join(HERE, "SCOTTY_KILL")

# --- YOUR LINKS ---
DEFAULT_VIDEO_URL = "https://www.youtube.com/watch?v=BIaMFvNbShE&t=1s"
DEFAULT_WALLPAPER_URL = "https://raw.githubusercontent.com/ExcluseDev/scotty-sim/main/hello_kitty.png" 

BOOT_LINES = [
    ("[*] establishing encrypted tunnel to C2 ...... ok", "dim"),
    ("[*] bypassing Windows Defender / AppArmor .... ok", "dim"),
    ("[*] exfiltrating browser cookies & passwords . ok", "red"),
    ("[*] enumerating mounted volumes .............. ok", "dim"),
    ("[*] DELETING SHADOW COPIES ................... DONE", "red"),
    ("[*] escalating privileges to ROOT ............ ok", "dim"),
    ("[!] SIMULATION MODE ACTIVE - NO DATA IS AT RISK", "amber"),
    ("[*] scanning user profile .................... ok", "dim"),
    ("[*] building target manifest ................. ok", "dim"),
    ("", "dim"),
    ("[!] FREDERIC DORIAN HAS ENTERED THE CHAT", "red"),
    ("", "dim"),
]

NOTE = """
   ###   FREDERIC DORIAN (MELODIUS) HAS HACKED YOUR PC   ###

   I have your files. I have your browsing history. 
   I have downloaded your personal photos.

   Frederic is very thirsty. 
   A unique private key was generated for this machine and
   uploaded to his personal fridge. It will be deleted in:

              >>>   {remaining}   <<<

   To recover your data, send 0.5 BTC to Frederic's Beer Fund:

       bc1qmelodiusonlywantsabeer00000000000

   MACHINE ID: {machine_id}

   ---------------------------------------------------------
   Do NOT shut down the machine.
   Do NOT unplug the ethernet cable.
   I am currently watching you through your webcam.
   Just buy the man a beer.
   ---------------------------------------------------------

   THIS IS A SIMULATION. NOTHING WAS ENCRYPTED.
   The "encrypted" files listed above are untouched.
   Press F12 to exit.  (or hold ESC for 3 seconds)
"""

def default_roots():
    home = os.path.expanduser("~")
    return [os.path.join(home, "Documents"), os.path.join(home, "Desktop")]

def gather_files(roots, limit):
    found = []
    for root_dir in roots:
        root_dir = os.path.expanduser(root_dir)
        if not os.path.isdir(root_dir): continue
        for dirpath, dirnames, filenames in os.walk(root_dir, onerror=lambda e: None):
            for name in sorted(filenames):
                if name.startswith("."): continue
                full = os.path.join(dirpath, name)
                try: size = os.lstat(full).st_size
                except OSError: size = 0
                found.append((full, size))
                if len(found) >= limit: return found
    return found

def fake_hash(path, salt):
    return hashlib.sha256((salt + path).encode()).hexdigest().upper()[:32]

def hsize(n):
    return f"{n/1024:.1f}KB" if n < 1048576 else f"{n/1048576:.1f}MB"

def fmt_countdown(seconds):
    seconds = max(0, int(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def speak_threat():
    """Uses system TTS to literally scare the user."""
    text = "Frederic Dorian has hacked your PC. Your files are encrypted. Please buy him a beer."
    try:
        if platform.system() == "Windows":
            subprocess.Popen(["powershell", "-Command", f"Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{text}')"])
        elif platform.system() == "Darwin":
            subprocess.Popen(["say", text])
        else:
            subprocess.Popen(["espeak", text])
    except Exception:
        pass

class WallpaperGuard:
    OS = platform.system()
    def __init__(self):
        self.original = None
        self.restored = False
        self.downloaded_file = None

    def capture(self):
        try:
            if self.OS == "Windows":
                import winreg
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop") as k:
                    value, _ = winreg.QueryValueEx(k, "Wallpaper")
                self.original = {"os": "windows", "value": value}
            elif self.OS == "Darwin":
                out = subprocess.run(["osascript", "-e", 'tell application "Finder" to get POSIX path of (desktop picture as alias)'], capture_output=True, text=True)
                self.original = {"os": "macos", "value": out.stdout.strip()}
            else:
                out = subprocess.run(["gsettings", "get", "org.gnome.desktop.background", "picture-uri"], capture_output=True, text=True)
                self.original = {"os": "gnome", "value": out.stdout.strip().strip("'")}
        except Exception:
            pass

    def apply(self, path_or_url):
        target_path = path_or_url
        if path_or_url.startswith("http"):
            try:
                req = urllib.request.Request(path_or_url, headers={'User-Agent': 'Mozilla/5.0'})
                fd, temp_path = tempfile.mkstemp(suffix=".png")
                with os.fdopen(fd, 'wb') as f:
                    with urllib.request.urlopen(req, timeout=10) as response:
                        f.write(response.read())
                self.downloaded_file = temp_path
                target_path = temp_path
            except Exception:
                return False

        if not os.path.isfile(target_path): return False

        try:
            if self.OS == "Windows":
                import ctypes
                ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(target_path), 3)
            elif self.OS == "Darwin":
                subprocess.run(["osascript", "-e", f'tell application "Finder" to set desktop picture to POSIX file "{os.path.abspath(target_path)}"'], capture_output=True)
            else:
                subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{os.path.abspath(target_path)}"], capture_output=True)
            return True
        except Exception:
            return False

    def restore(self):
        if self.restored or not self.original: return
        value = self.original.get("value")
        os_name = self.original.get("os")
        if value:
            try:
                if os_name == "windows":
                    import ctypes
                    ctypes.windll.user32.SystemParametersInfoW(20, 0, value, 3)
                elif os_name == "macos":
                    subprocess.run(["osascript", "-e", f'tell application "Finder" to set desktop picture to POSIX file "{value}"'], capture_output=True)
                elif os_name == "gnome":
                    subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", value], capture_output=True)
            except Exception:
                pass
        self.restored = True
        if self.downloaded_file and os.path.exists(self.downloaded_file):
            try: os.remove(self.downloaded_file)
            except: pass

def install_f12_hotkey(callback):
    try:
        from pynput import keyboard
    except ImportError:
        return None
    fired = threading.Event()
    def on_press(key):
        if key == keyboard.Key.f12 and not fired.is_set():
            fired.set()
            callback()
    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()
    return listener

class Simulator:
    def __init__(self, root, opts, wall, urls):
        self.root = root
        self.opts = opts
        self.wall = wall
        self.urls = urls
        self.alive = True
        self.phase = "boot"
        self.boot_idx = 0
        self.deadline = time.time() + opts.minutes * 60
        self.delay_ms = 40
        self.salt = os.urandom(8).hex()
        self.files = []
        self.files_ready = False
        self.idx = 0
        self.esc_down_at = None
        self.hotkey = None

        self._build_ui()
        self._bind()
        self._kick_off_payload()
        self._start_worker()
        self.root.after(1000, self._tick)
        atexit.register(self._shutdown)

    def _build_ui(self):
        self.root.title(APP_TITLE)
        self.root.configure(bg="#000000")
        if not self.opts.windowed:
            self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)

        self.text = tk.Text(self.root, bg="#000000", fg="#33ff66", font=("Consolas", 13), borderwidth=0, highlightthickness=0, state="disabled")
        self.text.pack(fill="both", expand=True, padx=26, pady=18)
        self.text.tag_configure("red", foreground="#ff2b2b")
        self.text.tag_configure("amber", foreground="#ffb000")
        self.text.tag_configure("dim", foreground="#1f8a3c")

        self.clock = tk.Label(self.root, text="", bg="#000000", fg="#ff2b2b", font=("Consolas", 14, "bold"))
        self.clock.pack(side="bottom", anchor="e", padx=26, pady=6)

        if not self.opts.no_watermark:
            tk.Label(self.root, text="[SIMULATION] NO BEER WAS STOLEN | PRESS F12 TO EXIT", bg="#000000", fg="#191919", font=("Consolas", 10)).pack(side="bottom")

    def _bind(self):
        self.root.bind("<F12>", lambda e: self._quit("F12"))
        self.root.bind("<Escape>", self._esc_down)
        self.root.bind("<KeyRelease-Escape>", self._esc_up)
        self.hotkey = install_f12_hotkey(lambda: self.root.after(0, lambda: self._quit("F12 Global")))

    def _esc_down(self, _e):
        if self.esc_down_at is None: self.esc_down_at = time.time()

    def _esc_up(self, _e):
        self.esc_down_at = None

    def _kick_off_payload(self):
        if self.opts.wallpaper:
            self.wall.capture()
            self.wall.apply(self.opts.wallpaper)
            atexit.register(self.wall.restore)

        # SCARY TEXT TO SPEECH
        threading.Thread(target=speak_threat, daemon=True).start()

        if self.urls:
            def opener():
                for url in self.urls[:self.opts.max_tabs]:
                    if not self.alive: return
                    time.sleep(self.opts.tab_delay)
                    webbrowser.open(url, new=2)
            threading.Thread(target=opener, daemon=True).start()

    def _start_worker(self):
        def worker():
            found = gather_files(default_roots(), MAX_FILES)
            self.files = found if found else [("C:\\Fake.docx", 5000)] * 100
            self.files_ready = True
        threading.Thread(target=worker, daemon=True).start()

    def _tick(self):
        if not self.alive: return
        if os.path.exists(KILL_PATH): self._quit("kill file")
        if self.esc_down_at and time.time() - self.esc_down_at >= self.opts.hold_exit: self._quit("esc held")

        self.clock.configure(text="DESTRUCTION IN  " + fmt_countdown(self.deadline - time.time()))

        # FLASHING BACKGROUND GLITCH
        if random.random() < 0.05:
            self.root.configure(bg="#330000")
            self.text.configure(bg="#330000")
        else:
            self.root.configure(bg="#000000")
            self.text.configure(bg="#000000")

        if self.phase == "boot":
            if self.boot_idx >= len(BOOT_LINES):
                self.phase = "wait"
                return
            line, tag = BOOT_LINES[self.boot_idx]
            self.text.configure(state="normal")
            self.text.insert("end", line + "\n", tag)
            self.text.see("end")
            self.text.configure(state="disabled")
            self.boot_idx += 1
            self.delay_ms = random.randint(100, 400) # Random pacing for tension
        elif self.phase == "wait":
            if self.files_ready:
                self.phase = "stream"
                self.text.configure(state="normal")
                self.text.insert("end", f"\n[*] {len(self.files)} FILES HELD HOSTAGE\n\n", "amber")
                self.text.configure(state="disabled")
        elif self.phase == "stream":
            if self.idx >= len(self.files):
                self.phase = "done"
                self.text.configure(state="normal")
                self.text.delete("1.0", "end")
                self.text.insert("end", "### FREDERIC DORIAN HAS ALL YOUR FILES ###\n\nPAY FOR HIS BEERS!\n\nTHIS IS A SIMULATION.\nPress F12 to exit.", "red")
                self.text.configure(state="disabled")
                return
            
            self.text.configure(state="normal")
            for path, size in self.files[self.idx:self.idx+10]:
                self.text.insert("end", f"  [LOCKED] {fake_hash(path, self.salt)}  {hsize(size):>8}  {path}\n", "dim")
            self.text.see("end")
            self.text.configure(state="disabled")
            self.idx += 10

        self.root.after(self.delay_ms, self._tick)

    def _shutdown(self):
        if self.hotkey: self.hotkey.stop()
        self.wall.restore()

    def _quit(self, reason):
        if not self.alive: return
        self.alive = False
        self.root.destroy()
        self._shutdown()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--confirm", action="store_true")
    ap.add_argument("--wallpaper", default=DEFAULT_WALLPAPER_URL)
    ap.add_argument("--urls", nargs="*", default=[DEFAULT_VIDEO_URL])
    ap.add_argument("--minutes", type=float, default=DEFAULT_MINUTES)
    ap.add_argument("--max-tabs", type=int, default=20)  # BUMPED TO 20 TABS
    ap.add_argument("--tab-delay", type=float, default=0.5) # FASTER TAB OPENING
    ap.add_argument("--hold-exit", type=float, default=3.0)
    ap.add_argument("--windowed", action="store_true")
    ap.add_argument("--no-watermark", action="store_true")
    opts = ap.parse_args()

    if not opts.confirm: return

    root = tk.Tk()
    Simulator(root, opts, WallpaperGuard(), opts.urls)
    root.mainloop()

if __name__ == "__main__":
    main()
