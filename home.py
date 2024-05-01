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
    If successful, the script is launched as a separate process, allowing it to run independently.
    The main application window is minimized to the system tray upon launching the script.

    This function uses the 'resource' function to resolve the path to the script, then attempts to
    execute it as a new process. If there are any issues in starting the script, it catches the exception
    and prints an error message. Regardless of success or failure in launching the script,
    the application window is minimized.
    """
    try:
        # Determine the full path to the script that needs to be launched
        script_path = resource('Scroll.py')
        # Launch the script as a separate process to allow it to run independently
        subprocess.Popen(['python', script_path], start_new_session=True)
    except Exception as e:
        # Log an error message if the script fails to start
        print(f"Failed to start script: {e}")

    # Minimize the main application window to the system tray
    app.iconify()


# ~~~~~~~~~~~~~~~~~~~ Configuration Handling ~~~~~~~~~~~~~~~~~~~ #
def resource(relative_path):
    """
    Resolves the absolute path for a given resource, accommodating both development and deployment environments.

    Args:
    relative_path (str): The relative path to the resource.

    Returns:
    str: The absolute path to the resource.

    This function identifies the base path of the application, accounting for whether the application
    is running in a development environment or as a bundled application (e.g., using PyInstaller).
    It then returns the absolute path by combining the base path with the provided relative path.
    """
    # Identify the base path, accommodating situations where the application is frozen (bundled)
    base_path = getattr(
        sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    # Combine the base path with the relative path to form the absolute path
    return os.path.join(base_path, relative_path)


def save_preferences(theme=None, ui_scale=None):
    """
    Saves user preferences such as theme and UI scale to a configuration file for future sessions.

    Args:
    theme (str, optional): The theme preference to save.
    ui_scale (float, optional): The UI scale preference to save.

    This function updates the user preferences configuration file with the provided theme and UI scale settings.
    It loads the current configuration, updates it with new values if provided, and writes the updated configuration
    back to the file, ensuring user settings are persisted across sessions.
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
    Loads user preferences from a configuration file, applying default values where specific settings are not found.

    Returns:
    tuple: A tuple containing the theme and UI scale settings loaded from the configuration.

    This function reads the configuration file to retrieve user preferences for the theme and UI scale.
    It provides default values for each setting if they are not explicitly set in the configuration file,
    ensuring the application has sensible defaults.
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
    Computes a scaled font size based on a given base size and a user-defined scale factor.

    Args:
    base_size (int): The base font size before scaling.
    ui_scale (float): The scale factor to apply to the base font size.

    Returns:
    int: The new font size after applying the scale factor.

    This function allows for dynamic font sizing throughout the application which adjusts according to user preferences
    for UI scalability. This is particularly useful for accessibility and different screen resolutions.
    """
    return int(base_size * ui_scale)


# Define global font sizes based on current UI scale
title_font_size = scaled_font_size(25, current_ui_scale)
heading_font_size = scaled_font_size(18, current_ui_scale)
info_font_size = scaled_font_size(15, current_ui_scale)
button_font_size = scaled_font_size(20, current_ui_scale)


def initialize_app():
    """
    Sets up the main application window with predefined properties such as size, title, and icon,
    and configures the UI based on the user's preferences.

    This function initializes the graphical interface of the application, setting the window size, enabling resize capability,
    assigning a window title, and applying an icon. It also adjusts the theme of the application based on the
    user's previously saved preferences to ensure a consistent user experience.
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
    # Hide all currently displayed frames
    dashboard_frame.pack_forget()
    instruction_frame.pack_forget()
    settings_frame.pack_forget()
    # Display the requested frame in a specified position and size
    frame_to_show.pack(side="left", fill="both", expand=True)


def toggle_appearance_mode():
    """
    Toggles the appearance mode (theme) of the application between 'Dark' and 'Light'.

    This function switches the current theme of the application and updates the global setting. It ensures
    that the theme preference is saved persistently so that it remains consistent across sessions. The function
    invokes other functions to apply the new theme to the UI and save the updated preference in a configuration file.
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

    Args:
    new_scale (float): The new scale factor to be applied to the UI elements.

    This function updates the global UI scale setting and recalculates all related font sizes based on the new scale.
    It also updates the configuration to reflect this change and refreshes UI elements to apply the new settings immediately.
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
    Clears all widgets from a specified frame, effectively resetting its content.

    Args:
    frame (tk.Frame): The frame from which all widgets will be removed.

    This function iterates over all child widgets of a given frame and removes them. This is typically used to refresh
    the contents of a frame before repopulating it with new widgets, ensuring that there are no leftover widgets from
    previous states.
    """
    for widget in frame.winfo_children():
        widget.destroy()  # Remove each widget from the frame


def update_ui_elements():
    """
    Refreshes the UI elements by clearing existing content and repopulating frames.

    This function is called after any changes to UI preferences like theme or scale to ensure the interface
    reflects the new settings accurately. It systematically clears content from all active frames and then
    reinitializes them with updated content based on the current configuration.
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
    Initializes and configures the sidebar of the application, setting up elements like logos and menu options.

    The sidebar is a constant visual element in the application that provides navigation or branding. This function
    configures the sidebar with a specific background color, dimensions, and prevents its contents from resizing
    the sidebar itself. It also handles the placement and presentation of the application logo.
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
    Sets up the main viewing area of the application, which includes various functional frames like dashboard, instructions, and settings.

    This function establishes the layout of the main application window, defining the space where most of the user interaction
    occurs. It initializes separate frames for different sections of the application, such as dashboard and settings,
    and prepares them for content filling based on user navigation.
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

    This function creates and adds buttons to the sidebar frame, enabling users to switch between different sections
    such as the Dashboard, Instructions, and Settings. Each button is associated with an icon and configured to
    display in a manner consistent with the application's theme. Buttons are linked to the appropriate frame display
    functions to facilitate UI navigation.
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

    This function sets up the initial display content for the dashboard, adding various UI components like
    labels and buttons that provide information and interaction opportunities for the user. The content
    is intended to give users an overview and controls for the primary functionalities of the application.
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
    Dynamically creates and displays a series of labels and their corresponding images within the instruction frame.

    Args:
    labels (list of str): Text descriptions to accompany each image.
    images (list of str): File paths for the images corresponding to each label.

    This function iterates over provided lists of labels and images, creating a label and image pair for each.
    It ensures that each image is resized to a standard dimension for uniformity and uses high-quality image
    resizing for better display. Labels and images are added to the instruction frame sequentially with appropriate
    padding and alignment.
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
    Initializes and populates the instruction frame with structured content, including steps and visuals.

    This function sets up the instructional content for the application, detailing the operational steps
    and associated imagery. It organizes content into a coherent sequence of instructions and images that
    guide the user through the application's usage.
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
        "      4. To move your mouse move your head like a joystick.",
        "      5. To right click wink your right eye for a second. To left click wink your left eye for a second.",
        "      6. To go back a page tilt your head to the left. To go forward a page tilt your head to the right."
    ]
    instructions_images = [
        "startInstructions.png",
        "mouth.png",
        "nod.png",
        "joystick.png",
        "wink.png",
        "navigate_page.png"
    ]

    # Utilize the earlier defined function to dynamically generate label and image pairs
    image_and_labels(instructions_text, instructions_images)


# ~~~~~~~~~~~~~~~~~~~ Settings Content ~~~~~~~~~~~~~~~~~~~ #
def setup_settings_content():
    """
    Configures and populates the settings frame with various adjustable options for the user.

    This function is responsible for setting up the user interface elements within the settings frame,
    allowing users to customize application settings such as the appearance theme and UI scaling.
    It organizes settings into two columns for a structured layout and provides interactive elements
    like buttons and sliders for user input.
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
