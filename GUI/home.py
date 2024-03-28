from customtkinter import *
from PIL import Image, ImageTk
import configparser


# ~~~~~~~~~~~~~~~~~~~ Configuration Handling ~~~~~~~~~~~~~~~~~~~ #
def save_preferences(theme=None, ui_scale=None):
    config = configparser.ConfigParser()
    config.read('user_preferences.ini')  # Load existing preferences

    if not config.has_section('Preferences'):
        config.add_section('Preferences')

    if theme is not None:
        config.set('Preferences', 'Theme', theme)

    if ui_scale is not None:
        config.set('Preferences', 'UI_Scale', str(ui_scale))

    with open('user_preferences.ini', 'w') as configfile:
        config.write(configfile)


def load_preferences():
    config = configparser.ConfigParser()
    config.read('user_preferences.ini')
    theme = config.get('Preferences', 'Theme', fallback='Dark')  # Default to 'Dark' if not found
    ui_scale = config.getfloat('Preferences', 'UI_Scale', fallback=1.0)  # Default to 1.0 if not found
    return theme, ui_scale


current_mode, current_ui_scale = load_preferences()


# Initialize global font sizes
def scaled_font_size(base_size, ui_scale):
    return int(base_size * ui_scale)


title_font_size = scaled_font_size(25, current_ui_scale)
heading_font_size = scaled_font_size(18, current_ui_scale)
info_font_size = scaled_font_size(15, current_ui_scale)
button_font_size = scaled_font_size(20, current_ui_scale)


def initialize_app():
    global app

    app = CTk()
    app.geometry("856x645")
    app.resizable(1, 1)
    app.title("Eye Click")
    app.iconbitmap('logo.ico')
    set_appearance_mode(current_mode)  # Use the already loaded preference


# ~~~~~~~~~~~~~~~~~~~ Frame Setup ~~~~~~~~~~~~~~~~~~~ #
# Helper Functions
def show_frame(frame_to_show):
    # Hide all frames
    dashboard_frame.pack_forget()
    instruction_frame.pack_forget()
    settings_frame.pack_forget()
    # Show the requested frame
    frame_to_show.pack(side="left", fill="both", expand=True)


def toggle_appearance_mode():
    global current_mode  # Use the global variable to track the current mode
    if current_mode == "Dark":
        current_mode = "Light"  # Switch to light mode
    else:
        current_mode = "Dark"  # Switch to dark mode
    set_appearance_mode(current_mode)
    save_preferences(theme=current_mode)  # Save the current theme preference


def apply_new_ui_scale(new_scale):
    global current_ui_scale
    current_ui_scale = new_scale  # Update the global UI scale variable

    # Update global font sizes
    global title_font_size, heading_font_size, info_font_size
    title_font_size = scaled_font_size(25, new_scale)
    heading_font_size = scaled_font_size(18, new_scale)
    info_font_size = scaled_font_size(15, new_scale)
    button_font_size = scaled_font_size(14, new_scale)

    save_preferences(ui_scale=new_scale)  # Save the new scale setting

    # Refresh UI elements to apply the new font sizes (Implement this function as needed)
    update_ui_elements()


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def update_ui_elements():
    # Clear existing content
    clear_frame(dashboard_frame)
    clear_frame(instruction_frame)
    clear_frame(settings_frame)

    # Repopulate the frames
    setup_dashboard_content()
    setup_instruction_content()
    setup_settings_content()
    # Repeat for other frames/content as necessary


# ~~~~~~~~~~~~~~~~~~~ Sidebar Setup ~~~~~~~~~~~~~~~~~~~ #
def setup_sidebar():
    global sidebar_frame
    sidebar_frame = CTkFrame(master=app, fg_color="#000017", width=176, height=650, corner_radius=0)
    sidebar_frame.pack_propagate(0)
    sidebar_frame.pack(fill="y", anchor="w", side="left")

    # Logo
    logo_img_data = Image.open("logo.ico")
    logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(100, 110))
    CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")


# ~~~~~~~~~~~~~~~~~~~ Main View Setup ~~~~~~~~~~~~~~~~~~~ #
def setup_main_view():
    global dashboard_frame, instruction_frame, settings_frame
    dashboard_frame = CTkFrame(master=app, width=680, height=650, corner_radius=0)
    instruction_frame = CTkScrollableFrame(master=app, width=680, height=650, corner_radius=0)
    settings_frame = CTkScrollableFrame(master=app, width=680, height=650, corner_radius=0)

    dashboard_frame.pack(side="left", fill="both", expand=True)
    instruction_frame.pack_forget()
    settings_frame.pack_forget()


# ~~~~~~~~~~~~~~~~~~~ Sidebar Buttons Setup ~~~~~~~~~~~~~~~~~~~ #
def setup_sidebar_buttons():
    global button_font_size, sidebar_frame
    analytics_img_data = Image.open("analytics_icon.png")
    analytics_img = CTkImage(dark_image=analytics_img_data, light_image=analytics_img_data)
    CTkButton(master=sidebar_frame, image=analytics_img, text="Dashboard", fg_color="transparent",
              font=("Arial Bold", button_font_size), hover_color="#4541B6", anchor="w",
              command=lambda: show_frame(dashboard_frame)).pack(side="top", fill="x", anchor="w", pady=(60, 0))

    list_img_data = Image.open("list_icon.png")
    list_img = CTkImage(dark_image=list_img_data, light_image=list_img_data)
    CTkButton(master=sidebar_frame, image=list_img, text="Instructions", fg_color="transparent",
              font=("Arial Bold", button_font_size), hover_color="#4541B6", anchor="w",
              command=lambda: show_frame(instruction_frame)).pack(side="top", fill="x", anchor="w", pady=(16, 0))

    settings_img_data = Image.open("settings_icon.png")
    settings_img = CTkImage(dark_image=settings_img_data, light_image=settings_img_data)
    CTkButton(master=sidebar_frame, image=settings_img, text="Settings", fg_color="transparent",
              font=("Arial Bold", button_font_size), hover_color="#4541B6", anchor="w",
              command=lambda: show_frame(settings_frame)).pack(side="top", fill="x", anchor="w", pady=(16, 0))


# ~~~~~~~~~~~~~~~~~~~ Dashboard Content ~~~~~~~~~~~~~~~~~~~ #


def setup_dashboard_content():
    global title_font_size, info_font_size

    dashboard_title = CTkLabel(master=dashboard_frame, text="Dashboard", font=("Arial Black", title_font_size),
                               text_color="#6862E4")
    dashboard_title.pack(pady=20)

    dashboard_info = CTkLabel(master=dashboard_frame, text="Welcome to the Dashboard!\nHere's your summary.",
                              font=("Arial", info_font_size), text_color="#555")
    dashboard_info.pack(pady=10)

    project_description = "This is Eye Click, a simple and intuitive way to help people navigate the web."
    description_label = CTkLabel(master=dashboard_frame, text=project_description, font=("Arial", info_font_size),
                                 wraplength=650, justify="left")
    description_label.pack(pady=10)

    project_description2 = "To begin, click start. Or, if you're not quite ready, navigate the sidebar."
    description_label = CTkLabel(master=dashboard_frame, text=project_description2, font=("Arial", info_font_size),
                                 wraplength=650, justify="left")
    description_label.pack(pady=10)

    # Start Button at the bottom
    start_button = CTkButton(master=dashboard_frame, text="Start", fg_color="#4541B6",
                             command=lambda: print("Starting..."))
    start_button.pack(pady=(10, 20))


# ~~~~~~~~~~~~~~~~~~~ Instructions Content ~~~~~~~~~~~~~~~~~~~ #

def image_and_labels(labels, images):
    global info_font_size
    for text, img_path in zip(labels, images):
        # Create and pack the text label
        text_label = CTkLabel(master=instruction_frame, text=text, font=("Arial", info_font_size), wraplength=650,
                              justify="left")
        text_label.pack(pady=(10, 0))

        # Load the image
        original_image = Image.open(img_path)
        base_width, base_height = original_image.size
        new_size = ((base_width * current_ui_scale) / 1.5, (base_height * current_ui_scale) / 1.5)
        image = Image.open(img_path)
        photo = CTkImage(image, size=new_size)

        # Create and pack the image label
        image_label = CTkLabel(master=instruction_frame, image=photo, text=" ")
        image_label.image = photo  # Keep a reference!
        image_label.pack(pady=(0, 10))


def setup_instruction_content():
    global title_font_size, info_font_size, heading_font_size
    instruction_title = CTkLabel(master=instruction_frame, text="Instructions", font=("Arial Black", title_font_size),
                                 text_color="#6862E4")
    instruction_title.pack(pady=(29, 0), padx=27, anchor="nw")

    getting_started = CTkLabel(master=instruction_frame, text="Getting Started:",
                               font=("Arial Black", heading_font_size),
                               text_color="#6862E4")
    getting_started.pack(pady=(29, 0), padx=27, anchor="nw")

    # Text instructions
    instructions_text = [
        "      1. Click on the start button on the dashboard to start the application.",
        "      2. Follow through the calibration instructions.",
        "      3. To scroll {{INSERT INSTRUCTIONS HERE}}",
        "      4. To click {{INSERT INSTRUCTIONS HERE}}",
        "      5. {{INCLUDE MORE CONTROLS}}",
        "      6. Once done, {{INSERT INSTRUCTIONS HERE}}"
    ]

    # Image paths corresponding to each step
    instructions_images = [
        "startInstructions.png",
        "startInstructions.png",  # Replace with actual image paths
        "startInstructions.png",  # Replace with actual image paths
        "startInstructions.png",  # Replace with actual image paths
        "startInstructions.png",  # Replace with actual image paths
        "startInstructions.png"  # Replace with actual image paths
    ]

    # Dynamically create labels and images based on instructions
    image_and_labels(instructions_text, instructions_images)


# ~~~~~~~~~~~~~~~~~~~ Settings Content ~~~~~~~~~~~~~~~~~~~ #
def setup_settings_content():
    global title_font_size, info_font_size
    setting_title = CTkLabel(master=settings_frame, text="Settings", font=("Arial Black", title_font_size),
                             text_color="#6862E4")
    setting_title.pack(pady=(20, 20), padx=27, anchor="nw")

    # Creating two sub-frames for a two-column layout within the settings frame
    settings_left_column = CTkFrame(master=settings_frame, corner_radius=0)
    settings_right_column = CTkFrame(master=settings_frame, corner_radius=0)

    settings_left_column.pack(side="left", fill="both", expand=True)
    settings_right_column.pack(side="left", fill="both", expand=True)

    # Setting 1: Theme Toggle
    CTkLabel(master=settings_left_column, text="Toggle Theme:", font=("Arial", info_font_size),
             text_color="#6862E4").pack(
        pady=(10, 20))
    CTkButton(master=settings_right_column, text="Toggle", fg_color="#4541B6", command=toggle_appearance_mode).pack(
        pady=(10, 20))

    # Setting 2: UI Scale
    ui_scale_label = CTkLabel(master=settings_left_column, text="UI Scale:", font=("Arial", info_font_size),
                              text_color="#6862E4")
    ui_scale_label.pack(pady=(10, 20))

    ui_scale_slider = CTkSlider(master=settings_right_column, from_=0.75, to=1.5)
    ui_scale_slider.set(current_ui_scale)  # Assuming current_ui_scale holds the current UI scale value
    ui_scale_slider.pack(pady=(10, 20))

    apply_ui_scale_button = CTkButton(master=settings_right_column, text="Apply", fg_color="#4541B6",
                                      command=lambda: apply_new_ui_scale(ui_scale_slider.get()))
    apply_ui_scale_button.pack(pady=(10, 20))


# ~~~~~~~~~~~~~~~~~~~ Main ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
if __name__ == "__main__":
    initialize_app()
    setup_sidebar()
    setup_main_view()
    setup_sidebar_buttons()
    setup_dashboard_content()
    setup_instruction_content()
    setup_settings_content()

    app.mainloop()
