from customtkinter import *
from PIL import Image, ImageTk
import configparser


# ~~~~~~~~~~~~~~~~~~~ Configuration Handling ~~~~~~~~~~~~~~~~~~~ #
def save_preferences(theme):
    config = configparser.ConfigParser()
    config['Preferences'] = {'Theme': theme}
    with open('user_preferences.ini', 'w') as configfile:
        config.write(configfile)


def load_preferences():
    config = configparser.ConfigParser()
    config.read('user_preferences.ini')
    theme = config.get('Preferences', 'Theme', fallback='Dark')  # Default to 'Dark' if not found
    return theme


# Initialize current_mode with the user's saved preference
current_mode = load_preferences()

app = CTk()
app.geometry("856x645")
app.resizable(1, 1)
app.title("Eye Click")
app.iconbitmap('logo.ico')
set_appearance_mode(current_mode)  # Apply the loaded theme preference


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
        set_appearance_mode("Light")  # Switch to light mode
        current_mode = "Light"
    else:
        set_appearance_mode("Dark")  # Switch to dark mode
        current_mode = "Dark"
    save_preferences(current_mode)  # Save the current theme preference


# ~~~~~~~~~~~~~~~~~~~ Sidebar Setup ~~~~~~~~~~~~~~~~~~~ #
sidebar_frame = CTkFrame(master=app, fg_color="#000017", width=176, height=650, corner_radius=0)
sidebar_frame.pack_propagate(0)
sidebar_frame.pack(fill="y", anchor="w", side="left")

# Assuming you have a logo image named 'logo.ico' in your project directory
logo_img_data = Image.open("logo.ico")
logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(100, 110))
CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")
# ~~~~~~~~~~~~~~~~~~~ Main View Setup ~~~~~~~~~~~~~~~~~~~ #

# New frame for the Dashboard
dashboard_frame = CTkFrame(master=app, width=680, height=650, corner_radius=0)

# New frame for Instructions
instruction_frame = CTkScrollableFrame(master=app, width=680, height=650, corner_radius=0)

# New frame for Settings
settings_frame = CTkScrollableFrame(master=app, width=680, height=650, corner_radius=0)

# Initially show the dashboard frame
dashboard_frame.pack(side="left", fill="both", expand=True)
instruction_frame.pack_forget()
settings_frame.pack_forget()

# ~~~~~~~~~~~~~~~~~~~ Sidebar Buttons Setup ~~~~~~~~~~~~~~~~~~~ #
analytics_img_data = Image.open("analytics_icon.png")
analytics_img = CTkImage(dark_image=analytics_img_data, light_image=analytics_img_data)
CTkButton(master=sidebar_frame, image=analytics_img, text="Dashboard", fg_color="transparent", font=("Arial Bold", 14),
          hover_color="#4541B6", anchor="w", command=lambda: show_frame(dashboard_frame)).pack(anchor="center", ipady=5,
                                                                                               pady=(60, 0))
list_img_data = Image.open("list_icon.png")
list_img = CTkImage(dark_image=list_img_data, light_image=list_img_data)
CTkButton(master=sidebar_frame, image=list_img, text="Instructions", fg_color="transparent", font=("Arial Bold", 14),
          hover_color="#4541B6", anchor="w", command=lambda: show_frame(instruction_frame)).pack(anchor="center",
                                                                                                 ipady=5,
                                                                                                 pady=(16, 0))

settings_img_data = Image.open("settings_icon.png")
settings_img = CTkImage(dark_image=settings_img_data, light_image=settings_img_data)
CTkButton(master=sidebar_frame, image=settings_img, text="Settings", fg_color="transparent", font=("Arial Bold", 14),
          hover_color="#4541B6", anchor="w", command=lambda: show_frame(settings_frame)).pack(anchor="center", ipady=5,
                                                                                              pady=(16, 0))
# ~~~~~~~~~~~~~~~~~~~ Dashboard Content ~~~~~~~~~~~~~~~~~~~ #
dashboard_title = CTkLabel(master=dashboard_frame, text="Dashboard", font=("Arial Black", 25), text_color="#6862E4")
dashboard_title.pack(pady=20)

dashboard_info = CTkLabel(master=dashboard_frame, text="Welcome to the Dashboard!\nHere's your summary.",
                          font=("Arial", 15), text_color="#555")
dashboard_info.pack(pady=10)

project_description = "This is Eye Click, a simple and intuitive way to help people navigate the web."
description_label = CTkLabel(master=dashboard_frame, text=project_description, font=("Arial", 15),
                             wraplength=650, justify="left")
description_label.pack(pady=10)

project_description2 = "To begin, click start. Or, if you're not quite ready, navigate the sidebar."
description_label = CTkLabel(master=dashboard_frame, text=project_description2, font=("Arial", 15),
                             wraplength=650, justify="left")
description_label.pack(pady=10)

# Start Button at the bottom
start_button = CTkButton(master=dashboard_frame, text="Start", fg_color="#4541B6", command=lambda: print("Starting..."))
start_button.pack(pady=(10, 20))

# ~~~~~~~~~~~~~~~~~~~ Instructions Content ~~~~~~~~~~~~~~~~~~~ #
instruction_title = CTkLabel(master=instruction_frame, text="Instructions", font=("Arial Black", 25),
                             text_color="#6862E4")
instruction_title.pack(pady=(29, 0), padx=27, anchor="nw")

getting_started = CTkLabel(master=instruction_frame, text="Getting Started:", font=("Arial Black", 18),
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
for text, img_path in zip(instructions_text, instructions_images):
    # Create and pack the text label
    text_label = CTkLabel(master=instruction_frame, text=text, font=("Arial", 18), wraplength=650, justify="left")
    text_label.pack(pady=(10, 0))

    # Load the image
    image = Image.open(img_path)
    photo = ImageTk.PhotoImage(image)

    # Create and pack the image label
    image_label = CTkLabel(master=instruction_frame, image=photo, text=" ")
    image_label.image = photo  # Keep a reference!
    image_label.pack(pady=(0, 10))

# ~~~~~~~~~~~~~~~~~~~ Settings Content ~~~~~~~~~~~~~~~~~~~ #
setting_title = CTkLabel(master=settings_frame, text="Settings", font=("Arial Black", 25), text_color="#6862E4")
setting_title.pack(pady=(20, 20), padx=27, anchor="nw")

# Creating two sub-frames for a two-column layout within the settings frame
settings_left_column = CTkFrame(master=settings_frame, corner_radius=0)
settings_right_column = CTkFrame(master=settings_frame, corner_radius=0)

settings_left_column.pack(side="left", fill="both", expand=True)
settings_right_column.pack(side="left", fill="both", expand=True)

# Example Setting 1: Theme Toggle
CTkLabel(master=settings_left_column, text="Toggle Theme:", font=("Arial", 15), text_color="#6862E4").pack(
    pady=(10, 20))
CTkButton(master=settings_right_column, text="Toggle", fg_color="#4541B6", command=toggle_appearance_mode).pack(
    pady=(10, 20))

app.mainloop()