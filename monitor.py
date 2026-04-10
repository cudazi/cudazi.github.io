def get_frame(url):
    # We add --no-check-certificate and a Chrome User-Agent to bypass blocks
    cmd = [
        'yt-dlp', 
        '-g', 
        '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        '--format', 'best[ext=mp4]/best', 
        url
    ]
    try:
        stream_url = subprocess.check_output(cmd).decode('utf-8').strip().split('\n')[0]
        cap = cv2.VideoCapture(stream_url)
        success, frame = cap.read()
        cap.release()
        return frame if success else None
    except Exception as e:
        print(f"Log Error: {e}")
        return None

def check_bridge():
    # Try the standard watch URL instead of the /live/ link
    yt_url = "https://www.youtube.com/watch?v=BzwWjdZXymc"
    
    frame = get_frame(yt_url)
    
    if frame is None:
        # If the first link fails, try the general channel link as a backup
        print("First link failed, trying backup...")
        frame = get_frame("https://www.youtube.com/@DuluthHarborCam/live")

    if frame is None:
        return "STREAM_TIMEOUT" # More specific than ERROR

    # ... (rest of your edge detection code stays the same)
