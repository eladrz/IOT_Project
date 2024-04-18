import tkinter as tk
from tkinter import Scale, PhotoImage
from PIL import Image

class RGBLamp:
    def __init__(self, master):
        self.master = master
        self.master.title("RGB Lamp Control")

        self.red_scale = Scale(master, from_=60, to=255, orient=tk.HORIZONTAL, label="Red", command=self.update_color)
        self.green_scale = Scale(master, from_=60, to=255, orient=tk.HORIZONTAL, label="Green", command=self.update_color)
        self.blue_scale = Scale(master, from_=60, to=255, orient=tk.HORIZONTAL, label="Blue", command=self.update_color)

        self.red_scale.pack()
        self.green_scale.pack()
        self.blue_scale.pack()

        # Load the image of the lamp
        self.lamp_image = PhotoImage(file="lamp_image.png")

        self.lamp_label = tk.Label(master, image=self.lamp_image)
        self.lamp_label.pack()

    def update_color(self, event=None):
        red_value = self.red_scale.get()
        green_value = self.green_scale.get()
        blue_value = self.blue_scale.get()
        color_hex = f"#{red_value:02X}{green_value:02X}{blue_value:02X}"
        self.lamp_label.config(bg=color_hex)
        
    def get_color(self, color_hex):
        # Extract RGB values from color_hex
        red_value = int(color_hex[1:3], 16)
        green_value = int(color_hex[3:5], 16)
        blue_value = int(color_hex[5:], 16)

        # Update the scales with extracted RGB values
        self.red_scale.set(red_value)
        self.green_scale.set(green_value)
        self.blue_scale.set(blue_value)

