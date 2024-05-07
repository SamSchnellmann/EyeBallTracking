# EyeBallTracking

# Project summary
Python application that will allow users with impaired hand functionality to use a Windows computer to the same capacity as everyone else.
 This will be done by using face and eye tracking technology to detect where on the screen the user is looking and to tell when the user either 
 blinks or winks intentionally to detect a mouse click

# Software Features

## Hands Free Mouse:
The user will then be able to control the mouse by turning their face to look at diffrent parts of the screen, left and right click with 
diffrent blink patterns as well as double click and scroll up and down.
- Face Tracking
- Eye Tracking
- Scroll / Previous / Next Page Gesture Commands

# System Requirements

## Hardware
- **Processor**: Modern multi-core processor (Intel i5/i7/i9, AMD Ryzen).
- **RAM**: Minimum 8GB, 16GB recommended.
- **Webcam**: Required for video input.
- **Graphics Card**: Optional but recommended for enhanced performance.

## Software
- **Operating System**: Compatible with Windows, macOS, and Linux.
- **Python**: Version 3.6 or later.

# Python Script Requirements and Installation Guide

## Requirements

- Python 3.6 or later
- HD USB Webcam
- OpenCV
- Mediapipe
- NumPy
- PyAutoGUI
- CustomTkinter

## Installation

1. **Install Python 3.11.7**: Ensure Python 3.6 or later (3.11.7 recommended) is installed and properly configured on your system. 

    For in depth instructions on how to properly install Python on your system, you may follow this guide by "Python Programmer"
        https://www.youtube.com/watch?v=YKSpANU8jPE&pp=ygUqaW5zdGFsbCBhbmQgY29uZmlndXJlIHB5dGhvbiBvbiB3aW5kb3dzIDEw

2. **Install Dependencies**: Open your terminal or command prompt and navigate to the directory where `home.py` and `requirements.txt` are stored. Then, run the following command:

    
    `pip install -r requirements.txt`
    

    This command will install all the required dependencies listed in the `requirements.txt` file.

3. **Webcam Setup**: Before attempting to run the program, please make sure that the webcam you intend to use for this program is set as your device's default webcam.

    If you have a camera that is not the one you wish to use set as your default camera, the program will either use that, or it may fail to excecute if the camera is a different device (such as a capture card) that is registered as a webcam.

    For in depth instructions on how to properly configure your webcam for this application, please visit this handy guide.
        https://gemoo.com/blog/switch-camera-on-windows-10.htm#:~:text=Set%20Camera%20Device%20as%20default,section%20of%20the%20Control%20Panel.

## Running the Script

1. **Run the Script**: With your terminal or command prompt still open to the directory where your Python script (`home.py`) is located, execute the following command to start the Python script:

    `python home.py`

    This command will run the Python script and execute the code within it.


## Using EyeClick

1. **Home GUI**: Once you have successfully run the home.py script, you will see the EyeClick home GUI open on your desktop on the Dashboard. 

2. **Running EyeClick**: To run the EyeClick software, click the start button. The start up process will take a short time to run, and once it is complete you will see your camera stream pop up on your screen. Congratulations, you are now using EyeClick! For further instructions on how to use the software, please refer to the `Instructions` page of the EyeClick launcher.

## Exe version

1. If you are using the EXE version of the program, simply double click on the home.exe file that is provided in the distribution and follow the instructions for operating the program as normal.
