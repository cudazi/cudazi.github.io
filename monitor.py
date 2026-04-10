import cv2
import numpy as np
import json
import datetime
import subprocess
import os

def get_frame(url):
    """
    Uses yt-dlp to grab the direct stream URL and OpenCV to capture one frame.
    """
    # We use a Chrome User-Agent to prevent YouTube from blocking the 'bot'
    cmd = [
        'yt-dlp', 
        '-g', 
        '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        '--format', 'best[ext=mp4]/best', 
        url
    ]
    try:
        # Get the stream URL
        stream_url = subprocess.check_output(cmd).decode('utf-8').strip().split('\n')[0]
        
        # Capture the frame
        cap = cv2.VideoCapture(stream_url)
        success, frame = cap.read()
        cap.release()
        
        return frame if success else None
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

def check_bridge():
    # 1. The Video Source
    yt_url = "https://www.youtube.com/watch?v=BzwWjdZXymc"
    
    # 2. Try to get the frame
    frame = get_frame(yt_url)
    if frame is None:
        return "ERROR: Stream Offline"

    # 3. Check for the template file
    # Ensure you have uploaded 'template.png' to your GitHub repo!
    if not os.path.exists('template.png'):
        return "ERROR: template.png not found"

    # 4. Image Processing (The Shape Detection)
    # Convert live frame to edges
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges_frame = cv2.Canny(gray_frame, 50, 150)

    # Convert template to edges
    template = cv2.imread('template.png', 0)
    edges_template = cv2.Canny(template, 50, 150)

    # 5. Template Matching
    # This looks for the 'shape' of the template inside the live frame
    res = cv2.matchTemplate(edges_frame, edges_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)

    print(f"Match Score: {max_val:.2f}")

    # Threshold: If it matches > 50%, the bridge is DOWN
    if max_val > 0.50:
        return "DOWN"
    else:
        return "UP"

# --- Main Execution ---
try:
    status_result = check_bridge()
except Exception as e:
    status_result = f"ERROR: {str(e)}"

# Prepare the data for your web page
data = {
    "status": status_result,
    "last_check": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Save to status.json
with open('status.json', 'w') as f:
    json.dump(data, f)

print(f"Process Complete. Status: {status_result}")
