import turtle as fern
import random
import sys
import json

try: # This adds ability to visualize the fern without having to install pillow in case the user don't want the
    # functionality to export the result.
    from PIL import ImageGrab
except ImportError:
    ImageGrab = None

default_preferences = {
    "ultrafast": True,
    "x_offset": 0,
    "y_offset": -230,
    "scale": 50,
    "plot_points": 10000,
    "probabilities": [0.01, 0.85, 0.07, 0.07],
    "x": 0,
    "y": 0,
    "speed": 0,
    "leftleaf_color": "#6E4C21",
    "rightleaf_color": "#37B469",
    "base_color": "#988a4f",
    "top_color": "#788511",
    "completion_message": None,
    "background_color": "black",
    "save_image": False
}


# Definition of the function to get the coordinates of the window
def window_coordinates():
    """ This function is solely to get the display size without adding any additional dependencies. What is does is it takes a screenshot of the screen and gets the size of the screenshot using python pillows utilities."""
    if ImageGrab:
        display_width, display_height = ImageGrab.grab().size
        left = (display_width - fern.window_width()) // 2
        upper = (display_height - fern.window_height()) // 2
        right = left + fern.window_width()
        lower = upper + fern.window_height()
        return (left, upper, right, lower)


# Definition of the Function to Check  command line arguments
def check_cmd_args(sys_args, arg_count):
    global preferences
    if arg_count > 1 and sys_args[1] == "-s":
        preferences["ultrafast"] = False
        print("plotting in slow mode.")
        if arg_count == 3:
            preferences["speed"] = int(sys_args[2])

    elif arg_count == 2 and sys_args[1] == "-u":
        preferences["ultrafast"] = True
        print("Plotting in ultra fast mode.")

    elif arg_count == 2 and sys_args[1] == "save":
        preferences["save_image"] = True

    elif arg_count == 3 and sys_args[1] == "-p" and sys_args[2].isdigit():
        preferences["plot_points"] = int(sys_args[2])
        print("plotting", sys_args[2], "points.")

    elif len(sys_args) == 2 and sys_args[1] == "-h":
        print("Refer the README.md file for more information.")
        sys.exit()

    elif arg_count > 2 and sys_args[1] == "-c":
        for arg in sys_args[2:]:
            if len(arg) == 9 and arg[2] == "#" and (int(arg[3:], 16) < 16777216):
                if arg[:2].lower() == "ll":
                    preferences["leftleaf_color"] = arg[2:]
                elif arg[:2].lower() == "rl":
                    preferences["rightleaf_color"] = arg[2:]
                elif arg[:2].lower() == "bs":
                    preferences["base_color"] = arg[2:]
                elif arg[:2].lower() == "tp":
                    preferences["top_color"] = arg[2:]

    elif arg_count == 2 and sys_args[1] == "reset":
        preferences = default_preferences
        print("Preferences set to default.")
    # Definitions of the functions for the fractal transformations.


def function1(x, y):
    fern.pencolor(preferences["base_color"])
    x1 = 0 * x + 0 * y
    y1 = 0 * x + 0.16 * y
    return x1, y1


def function2(x, y):
    fern.pencolor(preferences["top_color"])
    x2 = 0.85 * x + 0.04 * y + 0
    y2 = (-0.04) * x + 0.85 * y + 1.6
    return x2, y2


def function3(x, y):
    fern.pencolor(preferences["leftleaf_color"])
    x3 = 0.2 * x + (-0.26) * y + 0
    y3 = 0.23 * x + 0.22 * y + 1.6
    return x3, y3


def function4(x, y):
    fern.pencolor(preferences["rightleaf_color"])
    x4 = (-0.15) * x + 0.28 * y + 0
    y4 = 0.26 * x + 0.24 * y + 0.44
    return x4, y4


# end of function definitions


# Load preferences from the JSON file if there is any.
try:
    with open("preferences_barnsley.json", "r") as file:
        preferences = json.load(file)
except FileNotFoundError:
    print("Using default preferences.")
    preferences = default_preferences
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
# end of loading preferences

# Changing preferences according to the command line arguments.
arg_count = len(sys.argv)
check_cmd_args(sys.argv, arg_count)

x = preferences["x"]
y = preferences["y"]
functions = [function1, function2, function3, function4]

# Plotting related code starts here.
fern.bgcolor(preferences["background_color"])
fern.speed(preferences["speed"])
fern.hideturtle()
fern.title("Barnsley Fern")

if preferences.get("ultrafast", True):
    fern.tracer(0)
try:
    for step in range(preferences["plot_points"]):
        fern.penup()
        fern.goto(x * preferences["scale"] + preferences["x_offset"], y * preferences["scale"] + preferences[
            "y_offset"])  # plotting the point after calculations with scale and offset
        fern.pendown()
        fern.circle(1)
        next_function = random.choices(functions, preferences["probabilities"])[
            0]  # randomly choosing the next function according to the probabilities.
        x, y = next_function(x, y)
        fern.update()
    if preferences["completion_message"]:
        fern.penup()
        fern.home()
        fern.goto(0, preferences["y_offset"] - 50)
        fern.pendown()
        fern.write(preferences["completion_message"], font=("Arial", 16, "normal"), align="center")

    if ImageGrab and preferences["save_image"]:
        # Capturing and saving the captured image as a PNG file
        image = ImageGrab.grab(bbox=window_coordinates())
        image.save("image_barnsley.png", "PNG")
    fern.exitonclick()

except fern.Terminator:
    print("Visualisation window closed by the user.")
# end of plotting code
finally:
    # Save preferences to a JSON file
    if arg_count > 1:
        try:
            with open("preferences_barnsley.json", "w") as file:
                json.dump(preferences, file)
            print("Your preferences have been saved.")
        except:
            print("Your preferences did not save.")
