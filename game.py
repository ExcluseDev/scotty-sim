import os
import getpass
import ctypes
import subprocess
import time

def get_username():
    """Tries to get the actual Windows username."""
    try:
        return getpass.getuser()
    except Exception:
        return "Friend"

def set_wallpaper(image_path):
    """Sets the Windows desktop wallpaper."""
    try:
        abs_path = os.path.abspath(image_path)
        # Windows API: SPI_SETDESKWALLPAPER (20), SPIF_UPDATEINIFILE (1) | SPIF_SENDCHANGE (2)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)
    except Exception as e:
        print(f"Failed to change wallpaper: {e}")

def speak_text(text):
    """Uses Windows PowerShell to speak with a deep, slow voice."""
    # Rate -3 makes the voice deep and slow (range is -10 to 10)
    ps_command = f"Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.Rate = -3; $s.Speak('{text}');"
    subprocess.Popen(["powershell", "-WindowStyle", "Hidden", "-Command", ps_command])

def open_notepad_message(username):
    """Creates a text file and opens it in Notepad."""
    temp_dir = os.environ.get('TEMP', 'C:\\Windows\\Temp')
    file_path = os.path.join(temp_dir, "READ_ME.txt")
    
    message = f"""Hello, {username}.

I know who you are. 
I know what you do on this computer.

Let's play a game. 

You have 24 hours to figure out how to get your life back.
If you fail, I will delete everything you love.

Just kidding. You can close this.

But think about this: How did I get your name?
And how long have I been watching you?

See you soon, {username}.
"""
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(message)
    
    # Open Notepad
    subprocess.Popen(["notepad.exe", file_path])

if __name__ == "__main__":
    print("Initializing...")
    
    user = get_username()
    
    # 1. Change the wallpaper (Make sure creepy1.png is in the same folder!)
    if os.path.exists("creepy1.png"):
        set_wallpaper("creepy1.png")
    else:
        print("[!] Warning: creepy1.png not found. Wallpaper won't change.")
    
    # 2. Open the Notepad message
    open_notepad_message(user)
    
    # 3. Speak the audio
    # We tell it to wait a couple of seconds so the Notepad opens first
    time.sleep(1.5)
    speak_text(f"Hello {user}. I want to play a game.")
    
    print("Prank executed. Press Ctrl+C in this window to exit cleanly.")
    # Keep the script alive so the audio finishes
    time.sleep(10)