import tkinter as tk

def update_color(*args):
    red_val = red_slider.get()
    green_val = green_slider.get()
    blue_val = blue_slider.get()
    status_label.config(bg=f"#{red_val:02x}{green_val:02x}{blue_val:02x}")
    
def change_color(data):
	turn_on()
	status_label.config(bg=data)

def turn_on():
    update_color()
    status_label.config(text="The led is now turned on.", bg="white")
    red_slider.config(state=tk.NORMAL)
    green_slider.config(state=tk.NORMAL)
    blue_slider.config(state=tk.NORMAL)

def turn_off():
    status_label.config(text="The led is now turned off.", bg="black")
    red_slider.config(state=tk.DISABLED)
    green_slider.config(state=tk.DISABLED)
    blue_slider.config(state=tk.DISABLED)

def create_RGB_led():
    # Create the main window
    root = tk.Tk()
    root.title("RGB Led Simulation")

    # Define the variables as global so they can be accessed within the function
    global status_label, red_slider, green_slider, blue_slider

    # Create a label to display lamp status
    status_label = tk.Label(root, text="Lamp is off", bg="white", width=30, height=5, font=("Arial", 12))
    status_label.pack(pady=20)

    # Create RGB sliders
    red_slider = tk.Scale(root, from_=0, to=255, label="Red", orient=tk.HORIZONTAL, length=200, command=update_color)
    red_slider.set(0)
    red_slider.pack()

    green_slider = tk.Scale(root, from_=0, to=255, label="Green", orient=tk.HORIZONTAL, length=200, command=update_color)
    green_slider.set(0)
    green_slider.pack()

    blue_slider = tk.Scale(root, from_=0, to=255, label="Blue", orient=tk.HORIZONTAL, length=200, command=update_color)
    blue_slider.set(0)
    blue_slider.pack()

    # Create buttons to turn the lamp on and off
    on_button = tk.Button(root, text="Turn On", command=turn_on, width=10, height=2)
    on_button.pack(side=tk.LEFT, padx=10)

    off_button = tk.Button(root, text="Turn Off", command=turn_off, width=10, height=2)
    off_button.pack(side=tk.RIGHT, padx=10)

    # Run the GUI
    root.mainloop()

