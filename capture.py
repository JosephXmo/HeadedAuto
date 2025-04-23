import mss
import numpy as np
import cv2


def get_camera_frame(cap):
    ret, frame = cap.read()
    return frame if ret else None

def get_screen_frame(monitor_id=1):
    with mss.mss() as sct:
        monitor = sct.monitors[monitor_id]              # Main display is 1 by default
        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)[:, :, :3]          # Discard alpha channel
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
