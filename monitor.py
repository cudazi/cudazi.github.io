def get_frame(url):
    # Use yt-dlp to get the direct stream URL
    # --quiet keeps the logs clean; --no-warnings prevents clutter
    cmd = f'yt-dlp -g --format "best[ext=mp4]" "{url}"'
    try:
        stream_url = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
        
        # Open the stream with OpenCV
        cap = cv2.VideoCapture(stream_url)
        
        # Set a timeout/buffer so it doesn't hang
        success, frame = cap.read()
        cap.release()
        
        if not success:
            print("Failed to capture frame from stream.")
            return None
            
        return frame
    except Exception as e:
        print(f"Error fetching stream: {e}")
        return None
