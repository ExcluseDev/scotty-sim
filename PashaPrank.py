import os
import tempfile
import subprocess
import webbrowser

# The entire scary HTML website encoded inside the Python script
HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>⚠️ CRITICAL SYSTEM ALERT ⚠️</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;700&display=swap');
        body, html { margin: 0; padding: 0; width: 100%; height: 100%; background-color: #050505; color: #fff; font-family: 'Segoe UI', sans-serif; overflow: hidden; user-select: none; }
        .bg-flash { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-color: #ff0000; z-index: -2; opacity: 0; pointer-events: none; animation: flashAnim 0.15s infinite alternate; }
        @keyframes flashAnim { 0% { opacity: 0; } 100% { opacity: 0.15; } }
        #intro-screen { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; text-align: center; z-index: 10; position: relative; }
        #scareware-window { display: none; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 800px; max-width: 95%; background: #1a1a1a; border: 3px solid #ff0000; border-radius: 8px; box-shadow: 0 0 50px rgba(255, 0, 0, 0.6); z-index: 100; flex-direction: column; }
        .window-header { background: linear-gradient(90deg, #cc0000, #ff0000); padding: 15px 20px; font-size: 24px; font-weight: bold; color: white; display: flex; align-items: center; gap: 15px; border-top-left-radius: 5px; border-top-right-radius: 5px; }
        .warning-icon { font-size: 32px; }
        .window-body { padding: 30px; }
        .window-body h2 { color: #ff3333; margin-top: 0; font-size: 28px; text-align: center; }
        .window-body p { font-size: 18px; line-height: 1.5; color: #ddd; }
        .threat-list { background: #000; border: 1px solid #333; padding: 15px; font-family: "Courier New", monospace; color: #33ff66; height: 120px; overflow: hidden; margin: 20px 0; font-size: 14px; }
        .action-buttons { display: flex; justify-content: center; gap: 20px; margin-top: 20px; }
        .btn { padding: 15px 30px; font-size: 18px; font-weight: bold; cursor: pointer; border-radius: 5px; border: none; text-transform: uppercase; }
        .btn-fix { background: #0078d7; color: white; }
        .btn-close { background: #333; color: white; }
        .recording-indicator { position: absolute; top: 20px; right: 20px; background: rgba(0, 0, 0, 0.8); border: 2px solid #ff0000; padding: 10px 20px; border-radius: 5px; display: none; align-items: center; gap: 10px; font-weight: bold; z-index: 200; }
        .rec-dot { width: 15px; height: 15px; background: #ff0000; border-radius: 50%; animation: blink 1s infinite; }
        @keyframes blink { 50% { opacity: 0; } }
        .watermark { position: absolute; bottom: 8px; left: 8px; color: #111; font-size: 10px; z-index: 100; }
    </style>
</head>
<body>
    <div class="bg-flash"></div>
    <div id="intro-screen">
        <h1 style="font-size: 3rem; color: #ff0000; text-shadow: 0 0 20px red;">⚠️ SYSTEM COMPROMISED ⚠️</h1>
        <p style="font-size: 1.2rem;">Pasha has infected your device.</p>
        <button class="btn btn-fix" style="margin-top: 20px;" onclick="startPrank()">CLICK TO REMOVE VIRUS</button>
    </div>
    <div class="recording-indicator" id="recIndicator"><div class="rec-dot"></div><span>WEBCAM ACTIVE: RECORDING</span></div>
    <div id="scareware-window">
        <div class="window-header"><span class="warning-icon">⚠️</span> Windows Defender Alert</div>
        <div class="window-body">
            <h2>YOUR COMPUTER HAS BEEN LOCKED</h2>
            <p>Your files are being uploaded to Pasha's private server.</p>
            <div class="threat-list" id="threatLog"></div>
            <p style="text-align: center; font-weight: bold; color: #ffb000;">To stop the encryption, pay 0.5 BTC to Pasha's Joint Fund.</p>
            <div class="action-buttons">
                <button class="btn btn-fix" onclick="fakeFix()">Fix Now (Requires BTC)</button>
                <button class="btn btn-close" onclick="fakeClose()">Close Window</button>
            </div>
        </div>
    </div>
    <iframe id="ytplayer" width="560" height="315" src="" style="position:absolute; top:-9999px; left:-9999px;" allow="autoplay"></iframe>
    <div class="watermark">[SIMULATION] TYPE "excluse" TO EXIT</div>
    <script>
        const VIDEO_ID = "BIaMFvNbShE"; 
        const SECRET_WORD = "excluse"; 
        let typedBuffer = ""; let isRunning = false; let audioCtx;
        document.addEventListener('contextmenu', event => event.preventDefault());
        function startPrank() {
            isRunning = true;
            document.getElementById('intro-screen').style.display = 'none';
            document.getElementById('scareware-window').style.display = 'flex';
            document.getElementById('recIndicator').style.display = 'flex';
            if (document.documentElement.requestFullscreen) { document.documentElement.requestFullscreen().catch(() => {}); }
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            let sirenOsc = audioCtx.createOscillator(); let sirenGain = audioCtx.createGain();
            sirenOsc.type = 'square'; sirenOsc.frequency.setValueAtTime(800, audioCtx.currentTime);
            setInterval(() => { if(isRunning) { sirenOsc.frequency.setValueAtTime(400, audioCtx.currentTime); sirenOsc.frequency.exponentialRampToValueAtTime(1200, audioCtx.currentTime + 0.5); } }, 500);
            sirenOsc.connect(sirenGain); sirenGain.connect(audioCtx.destination); sirenGain.gain.value = 0.2; sirenOsc.start();
            if ('speechSynthesis' in window) { const msg = new SpeechSynthesisUtterance("Warning. Computer locked. Buy Pasha a joint."); msg.pitch = 0.1; window.speechSynthesis.speak(msg); }
            document.getElementById('ytplayer').src = `https://www.youtube.com/embed/${VIDEO_ID}?autoplay=1&mute=1&controls=0&loop=1&playlist=${VIDEO_ID}`;
            setInterval(() => {
                if (!isRunning) return;
                const threats = ["CRITICAL: Stealing Passwords.txt", "CRITICAL: Accessing Webcam", "WARNING: Uploading history", "CRITICAL: Encrypting Selfie.jpg"];
                const div = document.createElement('div'); div.textContent = `[${new Date().toLocaleTimeString()}] ${threats[Math.floor(Math.random() * threats.length)]}`; div.style.color = "#ff3333";
                const log = document.getElementById('threatLog'); log.appendChild(div); log.scrollTop = log.scrollHeight;
            }, 100);
        }
        function fakeFix() { alert("ERROR: Cannot fix. Pasha requires joints."); }
        function fakeClose() { document.getElementById('scareware-window').style.transform = `translate(calc(-50% + ${Math.random() * 20 - 10}px), calc(-50% + ${Math.random() * 20 - 10}px))`; }
        document.addEventListener('keydown', function(event) {
            if (!isRunning) return;
            if (event.key === "Escape" || event.key === "F12") { event.preventDefault(); return; }
            if (event.key.length === 1) {
                typedBuffer += event.key.toLowerCase();
                if (typedBuffer.length > SECRET_WORD.length) { typedBuffer = typedBuffer.slice(-SECRET_WORD.length); }
                if (typedBuffer === SECRET_WORD) { isRunning = false; if(audioCtx) audioCtx.close(); window.close(); }
            }
        });
    </script>
</body>
</html>
"""

def main():
    # 1. Write the HTML to a temporary hidden file
    temp_dir = tempfile.gettempdir()
    html_path = os.path.join(temp_dir, "windows_security_update.html")
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_CODE)
        
    file_url = f"file:///{html_path.replace(chr(92), '/')}"

    # 2. Try to launch in Edge Kiosk mode (Looks like a native locked app)
    try:
        subprocess.Popen(["msedge", "--kiosk", file_url])
    except FileNotFoundError:
        try:
            # Fallback to Chrome Kiosk mode
            subprocess.Popen(["chrome", "--kiosk", file_url])
        except FileNotFoundError:
            # Fallback to default browser
            webbrowser.open(file_url)

if __name__ == "__main__":
    main()
