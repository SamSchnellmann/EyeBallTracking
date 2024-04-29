# Made by Jacob Davis
import configparser
import os
import sys
import subprocess

from PIL import Image, ImageTk
from customtkinter import *
from pystray import MenuItem as item, Icon as tray_icon


# ~~~~~~~~~~~~~~~~~~~ Handle Script ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def start_other_script():
    """
    Attempts to start an external Python script located in a specified directory.
    If successful, the script is launched as a separate process.
    The main application window is minimized to the system tray upon launching the script.
    """
    try:
        # Resolve the path to the script intended to be started
        script_path = resource('Scroll.py')
        # Start the script as a new process, allowing it to run independently from the main application
        subprocess.Popen(['python', script_path], start_new_session=True)
    except Exception as e:
        # Output an error message if the script cannot be started
        print(f"Failed to start script: {e}")

    # Minimize the main application window
    app.iconify()


# ~~~~~~~~~~~~~~~~~~~ Configuration Handling ~~~~~~~~~~~~~~~~~~~ #
def resource(relative_path):
    """
    Resolves the absolute path of a given resource relative to the application's directory.
    Supports both development and deployed (frozen) environments.
    """
    # Identify the base path, accommodating situations where the application is frozen (bundled)
    base_path = getattr(
        sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    # Combine the base path with the relative path to form the absolute path
    return os.path.join(base_path, relative_path)


def save_preferences(theme=None, ui_scale=None):
    """
    Saves user preferences such as theme and UI scale to a configuration file.
    These settings can then be loaded later when the application starts.
    """
    config = configparser.ConfigParser()
    config.read(resource('user_preferences.ini'))  # Load the existing configuration file

    # Create a new section if it doesn't exist
    if not config.has_section('Preferences'):
        config.add_section('Preferences')

    # Update theme setting if provided
    if theme is not None:
        config.set('Preferences', 'Theme', theme)

    # Update UI scale setting if provided
    if ui_scale is not None:
        config.set('Preferences', 'UI_Scale', str(ui_scale))

    # Save the updated configuration back to file
    with open(resource('user_preferences.ini'), 'w') as configfile:
        config.write(configfile)


def load_preferences():
    """
    Loads user preferences from a configuration file, providing default values if specific settings are not found.
    """
    config = configparser.ConfigParser()
    config.read(resource('user_preferences.ini'))
    # Retrieve the theme setting, defaulting to 'Dark' if not specified
    theme = config.get('Preferences', 'Theme', fallback='Dark')
    # Retrieve the UI scale setting, defaulting to 1.0 if not specified
    ui_scale = config.getfloat('Preferences', 'UI_Scale', fallback=1.0)
    return theme, ui_scale


# Load initial preferences to set the application's mode and UI scale
current_mode, current_ui_scale = load_preferences()


def scaled_font_size(base_size, ui_scale):
    """
    Calculates the font size scaled according to a base size and a user-defined UI scale factor.
    """
    return int(base_size * ui_scale)


# Define global font sizes based on current UI scale
title_font_size = scaled_font_size(25, current_ui_scale)
heading_font_size = scaled_font_size(18, current_ui_scale)
info_font_size = scaled_font_size(15, current_ui_scale)
button_font_size = scaled_font_size(20, current_ui_scale)


def initialize_app():
    """
    Initializes the main application window with specified properties like size, title, and icon.
    The appearance mode (theme) is set based on previously loaded preferences.
    """
    global app  # Declare 'app' as global to ensure it can be accessed elsewhere in the application
    app = CTk()  # Create a new custom tkinter window
    app.geometry("856x645")  # Set the dimensions of the window
    app.resizable(1, 1)  # Allow the window to be resizable
    app.title("Eye Click")  # Set the window title
    app.iconbitmap(resource("logo.ico"))  # Set the window icon
    set_appearance_mode(current_mode)  # Apply the loaded theme preference


# ~~~~~~~~~~~~~~~~~~~ Frame Setup ~~~~~~~~~~~~~~~~~~~ #
def show_frame(frame_to_show):
    """
    Manages the visibility of frames within the application. It hides all other frames and displays the specified one.
    """
    # Hide all currently displayed frames
    dashboard_frame.pack_forget()
    instruction_frame.pack_forget()
    settings_frame.pack_forget()
    # Display the requested frame in a specified position and size
    frame_to_show.pack(side="left", fill="both", expand=True)


def toggle_appearance_mode():
    """
    Toggles the appearance mode (theme) of the application between 'Dark' and 'Light'.
    Saves the new theme preference once changed.
    """
    global current_mode  # Access the global variable that stores the current mode
    if current_mode == "Dark":
        current_mode = "Light"  # Change to light mode if currently in dark mode
    else:
        current_mode = "Dark"  # Change to dark mode if currently in light mode
    set_appearance_mode(current_mode)  # Apply the new appearance mode
    save_preferences(theme=current_mode)  # Persist the new mode in the configuration


def apply_new_ui_scale(new_scale):
    """
    Applies a new UI scale factor across the application, updating the font sizes and saving the preference.
    """
    global current_ui_scale, title_font_size, heading_font_size, info_font_size, button_font_size
    current_ui_scale = new_scale  # Update the global UI scale variable

    # Recalculate global font sizes based on the new UI scale
    title_font_size = scaled_font_size(25, new_scale)
    heading_font_size = scaled_font_size(18, new_scale)
    info_font_size = scaled_font_size(15, new_scale)
    button_font_size = scaled_font_size(14, new_scale)

    save_preferences(ui_scale=new_scale)  # Save the new UI scale setting

    # Refresh UI elements to apply the new font sizes
    update_ui_elements()


def clear_frame(frame):
    """
    Clears all widgets from a given frame, effectively resetting its content.
    """
    for widget in frame.winfo_children():
        widget.destroy()  # Remove each widget from the frame


def update_ui_elements():
    """
    Refreshes the UI elements by clearing existing content and repopulating frames.
    This is typically called after changes in UI preferences to ensure the interface reflects the new settings.
    """
    # Clear existing content from all relevant frames
    clear_frame(dashboard_frame)
    clear_frame(instruction_frame)
    clear_frame(settings_frame)

    # Repopulate the frames with updated content
    setup_dashboard_content()
    setup_instruction_content()
    setup_settings_content()
    # Additional frames or content can be updated here as necessary


# ~~~~~~~~~~~~~~~~~~~ Sidebar Setup ~~~~~~~~~~~~~~~~~~~ #
def setup_sidebar():
    """
    Initializes and configures the sidebar of the application, including the display of a logo.
    """
    global sidebar_frame  # Declare the sidebar_frame as a global variable for accessibility
    sidebar_frame = CTkFrame(master=app, fg_color="#000017", width=176, height=650, corner_radius=0)
    sidebar_frame.pack_propagate(0)  # Disable automatic resizing of the frame based on its contents
    sidebar_frame.pack(fill="y", anchor="w", side="left")  # Position the frame within the main window

    # Load and display the application logo
    logo_img_data = Image.open(resource("logo.ico"))  # Open the logo image file
    logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data,
                        size=(100, 110))  # Prepare the image for both themes
    CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")  # Display the logo


# ~~~~~~~~~~~~~~~~~~~ Main View Setup ~~~~~~~~~~~~~~~~~~~ #
def setup_main_view():
    """
    Sets up the main viewing area of the application, configuring frames for different sections of the GUI.
    """
    global dashboard_frame, instruction_frame, settings_frame  # Declare frames as global for accessibility
    dashboard_frame = CTkFrame(master=app, width=680, height=650, corner_radius=0)
    instruction_frame = CTkScrollableFrame(master=app, width=680, height=650, corner_radius=0)
    settings_frame = CTkScrollableFrame(master=app, width=680, height=650, corner_radius=0)

    # Initially display the dashboard frame and hide the others
    dashboard_frame.pack(side="left", fill="both", expand=True)
    instruction_frame.pack_forget()
    settings_frame.pack_forget()


# ~~~~~~~~~~~~~~~~~~~ Sidebar Buttons Setup ~~~~~~~~~~~~~~~~~~~ #
def setup_sidebar_buttons():
    """
    Configures and adds buttons to the sidebar for navigating between different sections of the application.
    """
    global button_font_size, sidebar_frame  # Access global variables
    # Create and display a button for navigating to the Dashboard
    analytics_img_data = Image.open(resource("analytics_icon.png"))  # Load icon for the dashboard button
    analytics_img = CTkImage(dark_image=analytics_img_data, light_image=analytics_img_data)
    CTkButton(master=sidebar_frame, image=analytics_img, text="Dashboard", fg_color="transparent",
              font=("Arial Bold", button_font_size), hover_color="#4541B6", anchor="w",
              command=lambda: show_frame(dashboard_frame)).pack(side="top", fill="x", anchor="w", pady=(60, 0))

    # Repeat for other sections: Instructions and Settings
    list_img_data = Image.open(resource("list_icon.png"))
    list_img = CTkImage(dark_image=list_img_data, light_image=list_img_data)
    CTkButton(master=sidebar_frame, image=list_img, text="Instructions", fg_color="transparent",
              font=("Arial Bold", button_font_size), hover_color="#4541B6", anchor="w",
              command=lambda: show_frame(instruction_frame)).pack(side="top", fill="x", anchor="w", pady=(16, 0))

    settings_img_data = Image.open(resource("settings_icon.png"))
    settings_img = CTkImage(dark_image=settings_img_data, light_image=settings_img_data)
    CTkButton(master=sidebar_frame, image=settings_img, text="Settings", fg_color="transparent",
              font=("Arial Bold", button_font_size), hover_color="#4541B6", anchor="w",
              command=lambda: show_frame(settings_frame)).pack(side="top", fill="x", anchor="w", pady=(16, 0))


# ~~~~~~~~~~~~~~~~~~~ Dashboard Content ~~~~~~~~~~~~~~~~~~~ #
def setup_dashboard_content():
    """
    Configures and populates the content of the dashboard frame within the application.
    """
    global title_font_size, info_font_size  # Access global variables for font sizes

    # Add title label to the dashboard
    dashboard_title = CTkLabel(master=dashboard_frame, text="Dashboard", font=("Arial Black", title_font_size),
                               text_color="#6862E4")
    dashboard_title.pack(pady=20)

    # Add introductory information text to the dashboard
    dashboard_info = CTkLabel(master=dashboard_frame, text="Welcome to the Dashboard!\nHere's your summary.",
                              font=("Arial", info_font_size), text_color="#555")
    dashboard_info.pack(pady=10)

    # Additional descriptive text about the application
    project_description = "This is Eye Click, a simple and intuitive way to help people navigate the web."
    description_label = CTkLabel(master=dashboard_frame, text=project_description, font=("Arial", info_font_size),
                                 wraplength=650, justify="left")
    description_label.pack(pady=10)

    # Further instructions or welcome message
    project_description2 = "To begin, click start. Or, if you're not quite ready, navigate the sidebar."
    description_label = CTkLabel(master=dashboard_frame, text=project_description2, font=("Arial", info_font_size),
                                 wraplength=650, justify="left")
    description_label.pack(pady=10)

    # Button to initiate a key application function
    start_button = CTkButton(master=dashboard_frame, text="Start", fg_color="#4541B6",
                             command=start_other_script)
    start_button.pack(pady=(10, 20))


# ~~~~~~~~~~~~~~~~~~~ Instructions Content ~~~~~~~~~~~~~~~~~~~ #
def image_and_labels(labels, images):
    """
    Dynamically creates and displays a set of labels and corresponding images within the instruction frame.
    Each label and image pair is presented in sequence.
    """
    global info_font_size  # Access the global variable to use consistent font size for all labels
    # Define a standard size for all images to maintain uniformity
    standard_size = (200, 150)  # 200 pixels wide, 150 pixels tall

    for text, img_path in zip(labels, images):
        # Create and pack the text label with appropriate styling and alignment
        text_label = CTkLabel(master=instruction_frame, text=text, font=("Arial", info_font_size), wraplength=650,
                              justify="left")
        text_label.pack(pady=(10, 0))  # Add padding above the label

        # Load the image from the specified path, resize it, and ensure high quality with LANCZOS filtering
        original_image = Image.open(resource(img_path))
        resized_image = original_image.resize(standard_size, Image.LANCZOS)

        # Create a photo image object to be used with CustomTkinter
        photo = ImageTk.PhotoImage(image=resized_image)

        # Create and pack the image label with the image
        image_label = CTkLabel(master=instruction_frame, image=photo, text=" ")
        image_label.image = photo  # Keep a reference to the image to avoid garbage collection
        image_label.pack(pady=(0, 10))  # Add padding below the image


def setup_instruction_content():
    """
    Sets up the content within the instruction frame of the application, detailing steps and related images.
    """
    global title_font_size, info_font_size, heading_font_size  # Access global variables for font sizes
    # Add a title label to the instruction frame
    instruction_title = CTkLabel(master=instruction_frame, text="Instructions", font=("Arial Black", title_font_size),
                                 text_color="#6862E4")
    instruction_title.pack(pady=(29, 0), padx=27, anchor="nw")  # Position and style the title

    # Add a subheading label to introduce the section
    getting_started = CTkLabel(master=instruction_frame, text="Getting Started:",
                               font=("Arial Black", heading_font_size),
                               text_color="#6862E4")
    getting_started.pack(pady=(29, 0), padx=27, anchor="nw")

    # Define text instructions and corresponding image paths
    instructions_text = [
        "      1. Click on the start button on the dashboard to start the application.",
        "      2. Open your mouth to toggle between scrolling and mouse navigation.",
        "      3. To scroll nod your head up and down.",
        "      4. To move your mouse move your head like a joystick"
    ]
    instructions_images = [
        "startInstructions.png",
        "mouth.png",
        "nod.png",
        "joystick.png"
    ]

    # Utilize the earlier defined function to dynamically generate label and image pairs
    image_and_labels(instructions_text, instructions_images)


# ~~~~~~~~~~~~~~~~~~~ Settings Content ~~~~~~~~~~~~~~~~~~~ #
def setup_settings_content():
    """
    Configures and populates the settings frame of the application with various adjustable options for the user.
    """
    global title_font_size, info_font_size  # Access global variables for consistent font sizes

    # Add a title label to the settings frame
    setting_title = CTkLabel(master=settings_frame, text="Settings", font=("Arial Black", title_font_size),
                             text_color="#6862E4")
    setting_title.pack(pady=(20, 20), padx=27, anchor="nw")

    # Create two sub-frames within the settings frame to organize settings into columns
    settings_left_column = CTkFrame(master=settings_frame, corner_radius=0)
    settings_right_column = CTkFrame(master=settings_frame, corner_radius=0)

    # Pack the sub-frames to align side by side
    settings_left_column.pack(side="left", fill="both", expand=True)
    settings_right_column.pack(side="left", fill="both", expand=True)

    # Add a label and button for toggling the theme of the application
    CTkLabel(master=settings_left_column, text="Toggle Theme:", font=("Arial", info_font_size),
             text_color="#6862E4").pack(pady=(10, 20))
    CTkButton(master=settings_right_column, text="Toggle", fg_color="#4541B6", command=toggle_appearance_mode).pack(
        pady=(10, 20))

    # Add a label and slider for adjusting the UI scale of the application
    ui_scale_label = CTkLabel(master=settings_left_column, text="UI Scale:", font=("Arial", info_font_size),
                              text_color="#6862E4")
    ui_scale_label.pack(pady=(10, 20))

    # Initialize a slider to adjust UI scale between defined limits
    ui_scale_slider = CTkSlider(master=settings_right_column, from_=0.75, to=1.5)
    ui_scale_slider.set(current_ui_scale)  # Set the slider's current value to match the global UI scale
    ui_scale_slider.pack(pady=(10, 20))

    # Add a button to apply the new UI scale from the slider
    apply_ui_scale_button = CTkButton(master=settings_right_column, text="Apply", fg_color="#4541B6",
                                      command=lambda: apply_new_ui_scale(ui_scale_slider.get()))
    apply_ui_scale_button.pack(pady=(10, 20))


# ~~~~~~~~~~~~~~~~~~~ Main ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
if __name__ == "__main__":
    # Execute the application setup functions when the script is run directly
    initialize_app()  # Initialize the main application window and settings
    setup_sidebar()  # Configure the sidebar with navigation buttons and logos
    setup_main_view()  # Prepare the main view area with various frames for content
    setup_sidebar_buttons()  # Populate the sidebar with buttons linking to different frames
    setup_dashboard_content()  # Set up initial content within the dashboard frame
    setup_instruction_content()  # Prepare the instruction frame with step-by-step guides
    setup_settings_content()  # Load the settings frame with configurable options

    app.mainloop()  # Start the main loop to keep the application running
