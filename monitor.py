import cv2
import numpy as np
import json
import datetime
import subprocess
import os

def get_frame(url):
    # Use yt-dlp to get the direct stream URL
    # The --format "best[ext=mp4]" ensures we get a format OpenCV can read easily
    cmd = f'yt-dlp -g --format "best[ext=mp4]" "{url}"'
    try:
        stream_url = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
        cap = cv2.VideoCapture(stream_url)
        success, frame = cap.read()
        cap.release()
        return frame if success else None
    except Exception as e:
        print(f"Stream Fetch Error: {e}")
        return None

def check_bridge():
    # YOUR SPECIFIC LIVE URL
    yt_url = "https://www.youtube.com/live/BzwWjdZXymc"
    
    frame = get_frame(yt_url)
    
    if frame is None:
        return "STREAM_OFFLINE"

    # 1. Convert live frame to edges
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges_frame = cv2.Canny(gray_frame, 50, 150)

    # 2. Check if template exists
    if not os.path.exists('template.png'):
        return "MISSING_TEMPLATE"

    # 3. Load and process template
    template = cv2.imread('template.png', 0)
    edges_template = cv2.Canny(template, 50, 150)

    # 4. Compare (Template Matching)
    res = cv2.matchTemplate(edges_frame, edges_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)

    print(f"Match Score: {max_val:.2f}")

    # If the match score is above 0.5, the bridge matches our 'Down' template
    return "DOWN" if max_val > 0.50 else "UP"

# Execute and Save
current_status = check_bridge()
data = {
    "status": current_status,
    "last_check": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

with open('status.json', 'w') as f:
    json.dump(data, f)

print(f"Final Status: {current_status}")
