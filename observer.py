import pyautogui


def get_observation_point(screen_size, mode='percent', value=(0.5, 0.5)):
    width, height = screen_size
    if mode == 'center':
        return width // 2, height // 2
    elif mode == 'absolute':
        x, y = value
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("Absolute mode requires numeric values")
        return value
    elif mode == 'percent':
        x_percent, y_percent = value
        if isinstance(x_percent, str):
            x_percent = float(x_percent.strip('%')) / 100
        if isinstance(y_percent, str):
            y_percent = float(y_percent.strip('%')) / 100
        if not (0 <= x_percent <= 1 and 0 <= y_percent <= 1):
            raise ValueError("Percent values must be between 0 and 1")
        x = int(width * x_percent / 100)
        y = int(height * y_percent / 100)
        return x, y
    elif mode == 'mouse':
        x, y = pyautogui.position()
        if not (0 <= x <= width and 0 <= y <= height):
            raise ValueError("Mouse position is outside the screen bounds")
        return x, y
    else:
        raise ValueError("Unsupported observation point mode")