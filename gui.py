from tkinter import *
from PIL import ImageTk, Image
import os, pyglet
import winsound
import random

import weather

# Size of the GUI, center positions.
WIDTH, HEIGHT = 300, 400
X_CENTER, Y_CENTER = WIDTH/2, HEIGHT/2

# Name.
name = "PixelArt Weather App"

# Load all fonts.
pyglet.font.add_directory("./fonts")

# Items.
canvas = None
weather_canvas = None

# Creates root and frame.
def createRoot():
    global root, frame
    root = Tk()
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.title(name)
    root.iconbitmap("pictures/icons/weather.ico")
    root.config(cursor = "@./pictures/cursor.cur")
    root.resizable(False, False)
    frame = Frame(root)
    frame.pack(expand = YES, fill = BOTH)

# Creates a new canvas and destroys the old one.
def createNewCanvas():
    global canvas

    if canvas != None:
        canvas.destroy()

    canvas = Canvas(frame)
    canvas.pack(expand = YES, fill = BOTH)

# Creates a new weather canvas and deletes the old one.
def createWeatherCanvas(weather_data):
    global canvas, weather_canvas, canvas_img, flag_img, icon_img

    if weather_canvas != None:
        weather_canvas.destroy()

    # Class WeatherObject.
    wo = weather.getWeatherObject(weather_data)

    # Weather canvas.
    weather_canvas = Canvas(canvas, width = WIDTH - 40, height = 240, highlightthickness = 0, bd = 0)
    canvas_img = ImageTk.PhotoImage(Image.open("./pictures/gui/canvas.png"))
    weather_canvas.create_image((0, 0), image = canvas_img, anchor = "nw")
    weather_canvas.place(x = 20, y = 85)

    # City name and flag.
    weather_canvas.create_text((30, 10), text = wo.name, font = "pixelmix 10", fill = "#bdbdbd", justify = "left", anchor = "w")
    flagPath = wo.getCountryFlag()

    if flagPath != None:
        flag_img = ImageTk.PhotoImage(Image.open(flagPath))
        weather_canvas.create_image((5, 6), image = flag_img, anchor = "nw")

    # Icon and temperature.
    icon_img = ImageTk.PhotoImage(Image.open(wo.getIcon()))
    weather_canvas.create_image((5, 30), image = icon_img, anchor = "nw")
    weather_canvas.create_text((55, 50), text = f"{wo.temp}°C", font = "pixelmix 24", fill = "#ffffff", justify = "left", anchor = "w")

    # Extra info.
    weather_canvas.create_text((10, 150), text = wo.getExtraInfo(), font = "pixelmix 7", fill = "#ffffff", justify = "left", anchor = "w")

# Creates the main menu.
def createMainMenu():
    global canvas, mainmenu_img, sun_img
    createNewCanvas()

    # Main menu background.
    mainmenu_img = ImageTk.PhotoImage(Image.open("./pictures/gui/mainmenu.png"))
    canvas.create_image((0, 0), image = mainmenu_img, anchor = "nw")

    # Title.
    canvas.create_text((X_CENTER, 20), text = name.upper(), font = "Pixeled 10 bold", fill = "#ffffff")

    # Logo.
    sun_img = ImageTk.PhotoImage(Image.open("./pictures/gui/weather.png"))
    canvas.create_image((X_CENTER - 32, 45), image = sun_img, anchor = "nw")

    # Main menu buttons.
    startY = 130
    bWidth, bHeight = 140, 60

    for t in ["Start", "Info", "Quit"]:
        b = Button(canvas, text = t, font = "Pixeled 9")
        b["command"] = lambda b = b: onMenuButtonClick(b["text"])
        b.configure(bg = "#ffffff", highlightthickness = 0, bd = 0, relief = FLAT)
        b.place(x = X_CENTER - (bWidth/2), y = startY, width = bWidth, height = bHeight)
        startY += 80

def createStart():
    global canvas, start_img
    createNewCanvas()

    # Start background.
    start_img = ImageTk.PhotoImage(Image.open("./pictures/gui/start.png"))
    canvas.create_image((0, 0), image = start_img, anchor = "nw")

    # Back button.
    b = Button(canvas, text = "Back", font = "Pixeled 9")
    b["command"] = lambda b = b: onMenuButtonClick(b["text"])
    b.configure(bg = "#ffffff", highlightthickness = 0, bd = 0, relief = FLAT)
    b.place(x = 10, y = HEIGHT - 60, width = 100, height = 50)

    # Text above entry.
    canvas.create_text((X_CENTER, 20), text = "Enter a city name and press enter:", font = "Pixeled 6 bold", fill = "#ffffff", justify = "left")

    # Entry.
    e = Entry(canvas, font = "Pixeled 8")
    e.bind("<Return>", lambda event = e: pressedEnter(e.get()))
    e.bind("<KeyRelease>", lambda event = e: entryChanged(e.get()))
    e.focus_set()
    canvas.create_window(X_CENTER, 60, width = WIDTH - 40, height = 30, window = e)

# Creates the info section.
def createInfo():
    global canvas, info_img, github_img
    createNewCanvas()

    # Info background.
    info_img = ImageTk.PhotoImage(Image.open("./pictures/gui/info.png"))
    canvas.create_image((0, 0), image = info_img, anchor = "nw")

    # Back button.
    b = Button(canvas, text = "Back", font = "Pixeled 9")
    b["command"] = lambda b = b: onMenuButtonClick(b["text"])
    b.configure(bg = "#ffffff", highlightthickness = 0, bd = 0, relief = FLAT)
    b.place(x = 10, y = 10, width = 100, height = 50)

    # Info text.
    canvas.create_text((X_CENTER, Y_CENTER), text = "Thank you for\nusing this Weather App.\nI made this with\npassion and love.\nMake sure to credit me\nif you're going to copy anything.", font = "Pixeled 7 bold", fill = "#ffffff", justify = "center")

    # Github image.
    github_img = ImageTk.PhotoImage(Image.open("./pictures/gui/github.png").resize((40, 42)))
    canvas.create_image((10, HEIGHT - 52), image = github_img, anchor = "nw")

    # Github link.
    canvas.create_text((170, HEIGHT - 30), text = "Github.com/PdV99", font = "Pixeled 9 bold", fill = "#ffffff")

# Runs when a button is clicked.
def onMenuButtonClick(text):
    playSound("click")
    text = text.lower()

    if text == "start":
        createStart()
    elif text == "info":
        createInfo()
    elif text == "back":
        createMainMenu()
    elif text == "quit":
        root.destroy()
    else:
        print(f"{text} has no method assigned.")

# Runs when enter is pressed in the entry.
def pressedEnter(entryText):
    global canvas

    if not entryText.isspace():
        cityName = weather.entryToCityName(entryText)
        weather_data = weather.getWeatherJson(cityName)

        if weather_data != None:
            createWeatherCanvas(weather_data)

def entryChanged(entryText):
    num = random.randint(1, 2)

    if len(entryText) > 0:
        if entryText[-1] == " ":
            playSound("spacebar")
        else:
            playSound(f"keyboard{num}")
    else:
        playSound(f"keyboard{num}")

# Plays a '.wav' sound if it's in the sounds directory.
def playSound(sname: str):
    sname += ".wav"
    sPath = f"./sounds/{sname}"

    if os.path.isfile(sPath):
        winsound.PlaySound(sPath, winsound.SND_ASYNC)
    else:
        print(f"Couldn't play sound `{sname}`")

if __name__ != "__main__":
    createRoot()
    createMainMenu()
    root.mainloop()