import pyautogui  # Import the PyAutoGUI library for controlling the mouse cursor.


def screen_size():
    """
    Find the screen size

    Parameters:
    - none

    Returns:
    - the width and height of the screen in pixels
    """
    return pyautogui.size()

# Yes, I know it is kinda useless to have this rn;
# however, if we are going to be making calibration
# and everything, this is probably where we would put it.
