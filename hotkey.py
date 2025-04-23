import keyboard


# System status
active = False

def toggle_active():
    global active
    active = not active
    print(f"[INFO] Auto aim is {'on' if active else 'off'}")


def keyboard_listener():
    keyboard.add_hotkey('ctrl+alt+shift+t', toggle_active)
    keyboard.wait()  # Keep listening

def is_active():
    return active
