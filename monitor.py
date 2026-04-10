import cv2
import numpy as np
import json
import datetime
import subprocess

def get_frame(url):
    # Get the actual stream URL using yt-dlp
    cmd = f'yt-dlp -g "{url}"'
    try:
        stream_url = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
        cap = cv2.VideoCapture(stream_url)
        success, frame = cap.read()
        cap.release()
        return frame if success else None
    except:
        return None

def check_bridge():
    # Use the Duluth Harbor Cam URL
    yt_url = "https://www.youtube.com/watch?v=BzwWjdZXymc" # Example URL
    frame = get_frame(yt_url)
    
    if frame is None:
        return "ERROR"

    # 1. Process Live Frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges_frame = cv2.Canny(gray_frame, 50, 150)

    # 2. Process Template
    template = cv2.imread('template.png', 0)
    edges_template = cv2.Canny(template, 50, 150)

    # 3. Match
    res = cv2.matchTemplate(edges_frame, edges_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)

    # Threshold: if it matches > 50%, bridge is likely down
    return "DOWN" if max_val > 0.50 else "UP"

status = check_bridge()
data = {
    "status": status,
    "last_check": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

with open('status.json', 'w') as f:
    json.dump(data, f)
