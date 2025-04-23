import cv2
import win32gui
import win32con
import pyautogui
import time
import threading
import argparse

# === Layer of Hoykey Listening
from hotkey import keyboard_listener, is_active
# === Layer of View Input
from capture import get_camera_frame, get_screen_frame
# === Layer of Target Recognition - Nose by Default
from targeting import get_extractor
# === Layer of Observation Point
from observer import get_observation_point
# === Layer of Shift Calculation
from shift import compute_offset
# === Layer of Control and Execution
from control import apply_offset


def suppress_all_logs():
    import os
    import absl.logging
    from ultralytics.utils import LOGGER

    absl.logging.set_verbosity(absl.logging.ERROR)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    LOGGER.setLevel("ERROR")

# Main procedure
def main(args):
    # Set up capture source object if needed
    if args.source == 'camera': cap = cv2.VideoCapture(0)
    
    screen_size = pyautogui.size()

    if args.debug: pyautogui.FAILSAFE = False  # Disable fail-safe to prevent mouse movement issues

    threading.Thread(target=keyboard_listener, daemon=True).start()

    # No need to set observation point since mouse mode updates it every cycle
    if not args.mode == 'mouse':
        observation_point = get_observation_point(screen_size, mode=args.mode, value=args.ref_point)
        print(f"[INFO] Set observation point to: {observation_point}")

    extract_target_coordinates = get_extractor(args.model)

    print("[INFO] System running, press \"Q\" to quit")
    print("[INFO] Active after 2 seconds, press \"Ctrl+Alt+Shift+T\" to toggle auto aim")
    time.sleep(2)  # Wait for user preparation
    print(f"[INFO] {"Not taken" if not is_active() else "Taken"} mouse control")

    # Configure preview window
    cv2.namedWindow("AutoAim - Press Q to exit", cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("AutoAim - Press Q to exit", 640, 320)

    # Set window to topmost
    hwnd = win32gui.FindWindow(None, "AutoAim - Press Q to exit")
    if hwnd:
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            0, 0, 0, 0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
        )

    while True:
        # Select frame source
        if args.source == "camera":     frame = get_camera_frame(cap)
        elif args.source == "screen":   frame = get_screen_frame()
        else:                           frame = None

        # Invalid source check
        if frame is None: break

        # Update observation point per cycle only if in mouse mode
        if args.mode == "mouse": observation_point = get_observation_point(screen_size, mode=args.mode, value=args.ref_point)

        target = extract_target_coordinates(frame)

        if target and is_active():
            if target[0] <= 0 or target[1] <= 0:
                continue

            dx, dy = compute_offset(target, observation_point, args.x_revert, args.y_revert)
            if abs(dx) < 10 and abs(dy) < 10:
                pyautogui.click()  # Click if close enough to target
                print("[INFO] Clicked on target")
            else:
                # Trim shift if close enough
                if abs(dx) < 10: dx = 0
                if abs(dy) < 10: dy = 0

                apply_offset(dx, dy, smooth=args.smooth)
                print(f"[INFO] Offset applied: {dx}, {dy}")

        # Visualize target point
        if target:
            if not is_active(): print(f"[INFO] Target detected at: {target[0]}, {target[1]}")
            cv2.circle(frame, target, 8, (255, 128, 128), 2)
            cv2.arrowedLine(frame, observation_point, target, (255, 255, 255), 2, tipLength=0.05)

        # Show preview
        cv2.imshow("AutoAim - Press Q to exit", frame)

        # Quit on key press
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Auto Aiming Tool for FPS Games - PROTOPYPE',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--mode', type=str, default='center', choices=['absolute', 'percent', 'center', 'mouse'],
                        help='Mode for observation point')
    parser.add_argument('--source', type=str, default='screen', choices=['camera', 'screen'],
                        help='Source for input frame')
    parser.add_argument('--ref_point', type=float, nargs=2, default=(0.5, 0.5),
                        help='Reference point for absolute mode (x, y)')
    parser.add_argument('--smooth', type=float, default=0.3,
                        help='Smoothing factor for offset application')
    parser.add_argument('--model', type=str, default='mediapipe', choices=['mediapipe', 'yolov8'],
                        help='Model for target detection')
    parser.add_argument('--x_revert', action='store_true',
                        help='Revert the x offset direction')
    parser.add_argument('--y_revert', action='store_true',
                        help='Revert the y offset direction')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode')
    args = parser.parse_args()

    if not args.debug:
        suppress_all_logs()

    main(args)
