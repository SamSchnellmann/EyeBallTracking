from customtkinter import *
from PIL import Image

# ~~~~~~~~~~~~~~~~~~~ Frame Setup ~~~~~~~~~~~~~~~~~~~ #
app = CTk()
app.geometry("856x645")
app.resizable(1, 1)
set_appearance_mode("dark")
current_mode = "Dark"  # Assuming you start in dark mode


# ~~~~~~~~~~~~~~~~~~~ Frame Setup ~~~~~~~~~~~~~~~~~~~ #


# ~~~~~~~~~~~~~~~~~~~ Helper Functions ~~~~~~~~~~~~~~ #
def show_frame(frame_to_show):
    # Hide all frames
    dashboard_frame.pack_forget()
    instruction_frame.pack_forget()
    settings_frame.pack_forget()
    # Add more frames if you have them

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


# ~~~~~~~~~~~~~~~~~~~ Helper Functions ~~~~~~~~~~~~~~ #


# ~~~~~~~~~~~~~~~~~~~ Sidebar Setup ~~~~~~~~~~~~~~~~~ #
sidebar_frame = CTkFrame(master=app, fg_color="#000017", width=176, height=650, corner_radius=0)
sidebar_frame.pack_propagate(0)
sidebar_frame.pack(fill="y", anchor="w", side="left")

# Load Data
logo_img_data = Image.open("logo.webp")
logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(100, 110))
CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")
# ~~~~~~~~~~~~~~~~~~~ Sidebar Setup ~~~~~~~~~~~~~~~~~ #


# ~~~~~~~~~~~~~~~~~~~ Main view ~~~~~~~~~~~~~~~~~~~~~ #

# New frame for the Dashboard
dashboard_frame = CTkFrame(master=app, width=680, height=650, corner_radius=0)

# New frame for instructions
instruction_frame = CTkFrame(master=app, width=680, height=650, corner_radius=0)

# New frame for settings
settings_frame = CTkFrame(master=app, width=680, height=650, corner_radius=0)

dashboard_frame.pack(side="left", fill="both", expand=True)
instruction_frame.pack_forget()
settings_frame.pack_forget()

# ~~~~~~~~~~~~~~~~~~~ Main view ~~~~~~~~~~~~~~~~~~~~~ #


# ~~~~~~~~~~~~~~~~~~~ Buttons ~~~~~~~~~~~~~~~~~~~~~~~ #
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
          hover_color="#4541B6", anchor="w", command=lambda: show_frame(settings_frame)).pack(anchor="center",
                                                                                              ipady=5,
                                                                                              pady=(16, 0))
# ~~~~~~~~~~~~~~~~~~~ Buttons ~~~~~~~~~~~~~~~~~~~~~~~ #


# ~~~~~~~~~~~~~~~~~~~ Dashboard ~~~~~~~~~~~~~~~~~~~~~ #
dashboard_title = CTkLabel(master=dashboard_frame, text="Dashboard", font=("Arial Black", 25), text_color="#6862E4")
dashboard_title.pack(pady=20)

dashboard_info = CTkLabel(master=dashboard_frame, text="Welcome to the Dashboard!\nHere's your summary.",
                          font=("Arial", 15), text_color="#555")
dashboard_info.pack(pady=10)

project_description = """This is Eye Click, a simple and intuitive way to help people navigate the web."""
description_label = CTkLabel(master=dashboard_frame, text=project_description, font=("Arial", 15),
                             wraplength=650, justify="left")
description_label.pack(pady=10)

# Why We Started
reason_for_starting = """We started this project with a simple aspiration; we wanted to bring the joy of computers to everyone."""
reason_label = CTkLabel(master=dashboard_frame, text=reason_for_starting, font=("Arial", 15),
                        wraplength=650, justify="left")
reason_label.pack(pady=10)

# Additional Information
additional_info = """With our introduction out of the way, click the start button below to start the application, or browse our tabs to get started."""
info_label = CTkLabel(master=dashboard_frame, text=additional_info, font=("Arial", 15),
                      wraplength=650, justify="left")
info_label.pack(pady=10)

# Start Button at the bottom
start_button = CTkButton(master=dashboard_frame, text="Start", fg_color="#4541B6", command=lambda: print("Starting..."))
start_button.pack(pady=(10, 20))
# ~~~~~~~~~~~~~~~~~~~ Dashboard ~~~~~~~~~~~~~~~~~~~~~ #


# ~~~~~~~~~~~~~~~~~~~ Instructions ~~~~~~~~~~~~~~~~~~ #
# Assuming main_view is for orders, let's add a title and a 'New Order' button
instruction_title = CTkLabel(master=instruction_frame, text="Instructions", font=("Arial Black", 25),
                             text_color="#6862E4")
instruction_title.pack(pady=(29, 0), padx=27, anchor="nw")

getting_started = CTkLabel(master=instruction_frame, text="Getting Started:", font=("Arial Black", 18),
                           text_color="#6862E4")
getting_started.pack(pady=(29, 0), padx=27, anchor="nw")

first_instruction = """Now we write the instructions. So, probably just put controls here"""
first_label = CTkLabel(master=instruction_frame, text=project_description, font=("Arial", 15),
                       wraplength=650, justify="left")
first_label.pack(pady=10)

# ~~~~~~~~~~~~~~~~~~~ Instructions ~~~~~~~~~~~~~~~~~~ #


# ~~~~~~~~~~~~~~~~~~~ Settings ~~~~~~~~~~~~~~~~~~~~~~ #
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

# ~~~~~~~~~~~~~~~~~~~ Settings ~~~~~~~~~~~~~~~~~~~~~~ #

app.mainloop()
