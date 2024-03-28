# @auth - Samuel Schnellmann
# @title - Splitscreen.py
#           code name - Snapper
# @brief - This subsection of code will help track the user's mouse and can snap the mouse
#          To the center of a quadrant if the user is to stay still for more than 5 seconds.
#          this is to insure that the calibration is always set correctly and sets up using
#          the face as a joy stick as we had intended on doing
#
# I AM STILL WORKING ON THIS!!!!!!!!!!!!!!!!
# @PROBLEMS - mouse is only moving to the TopLeft quadrant, mouse is snappy instead of smooth,
#             ctrl + alt + s is not working; however shift + alt + s is, program is moving mouse
#             immedietly instead of resting for 5 seconds.
import pygame
import sys
import os

# initalize the screen with pygame
pygame.init()

# screen dimensions
screen_width = 800
screen_height = 600

# Colors
WHITE = (225, 225, 225)
BLACK = (0, 0, 0)

# Set quadrants
quadrant_width = screen_width // 2
quadrant_height = screen_height // 2

# font
font = pygame.font.SysFont(None, 30)


# def for displaying text
def display_text(text, x, y):
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


# def for snaping the mouse back to the center
def move_mouse(quadrant_center):
    current_pos = pygame.mouse.get_pos()
    dx = (quadrant_center[0] - current_pos[0]) / 10
    dy = (quadrant_center[1] - current_pos[1]) / 10
    for _ in range(10):
        pygame.mouse.set_pos((current_pos[0] + dx, current_pos[1] + dy))


# Escaping the program in the event of an emergancy
#   while testing the code, the program locked my mouse into place
#   making it unable to close the program. "Ctrl + Alt + S" will stop all functionallity
#   turning back on the funcionality will be with "Shift + Alt + S"
def check_unlock_key():
    keys = pygame.key.get_pressed()
    ctrl_pressed = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
    alt_pressed = keys[pygame.K_LALT] or keys[pygame.K_LALT]
    s_pressed = keys[pygame.K_s]
    return ctrl_pressed and alt_pressed and s_pressed


def check_restart_key():
    keys = pygame.key.get_pressed()
    shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
    alt_pressed = keys[pygame.K_LALT] or keys[pygame.K_LALT]
    s_pressed = keys[pygame.K_s]
    return shift_pressed and alt_pressed and s_pressed


# Set up screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Crosshair with Text")

# Initialize variables for tracking time spent in each quadrant
time_in_quadrant = [[0, 0], [0, 0], [0, 0], [0, 0]]


# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Check for unlock key combo
    if check_unlock_key():
        pygame.mouse.set_visible(True)

    if check_restart_key():
        python = sys.executable
        pygame.quit()
        python = sys.executable
        os.execl(python.python, *sys.argv)

    # Clear screen
    screen.fill(BLACK)

    # Draw crosshair
    pygame.draw.line(
        screen, WHITE, (screen_width // 2, 0), (screen_width // 2, screen_height), 2
    )
    pygame.draw.line(
        screen, WHITE, (0, screen_height // 2), (screen_width, screen_height // 2), 2
    )

    # Get current mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x, mouse_y = (mouse_x // quadrant_width, mouse_y // quadrant_height)

    # Find the position in the quadrant
    mouse_quadrant = (mouse_x // quadrant_width, mouse_y // quadrant_height)

    # Draw text in each quadrant
    display_text("UpLeft", 10, 10)
    display_text("UpRight", screen_width - 100, 10)
    display_text("DownLeft", 10, screen_height - 40)
    display_text("DownRight", screen_width - 130, screen_height - 40)

    # check where the mouse is periodically
    #   if user stays still for more than 5 seconds, then mouse snaps to the center of the quadrant
    if pygame.mouse.get_rel() == (0, 0):
        time_in_quadrant[mouse_quadrant[0]][mouse_quadrant[1]] += 1
        if (
            time_in_quadrant[mouse_quadrant[0]][mouse_quadrant[1]] >= 500
        ):  # 500 iterations = 5 seconds
            quadrant_center = (
                (2 * mouse_quadrant[0] + 1) * quadrant_width // 2,
                (2 * mouse_quadrant[1] + 1) * quadrant_height // 2,
            )
            move_mouse(quadrant_center)
            time_in_quadrant[mouse_quadrant[0]][mouse_quadrant[1]] = 0
    else:
        time_in_quadrant = [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
        ]  # reset timer if mouse moves

    # Update
    pygame.display.flip()
