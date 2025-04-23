import pyautogui


def apply_offset(dx, dy, smooth=0.2):
    pyautogui.moveRel(dx, dy, duration=smooth)