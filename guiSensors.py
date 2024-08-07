import tkinter as tk
import re
import json


def parse_rgb(rgb_string):
    # Define the regular expression pattern to match the RGB values
    pattern = r'rgb\((\d+),\s*(\d+),\s*(\d+)\)'

    # Use re.findall to extract the values
    match = re.findall(pattern, rgb_string)

    if match:
        # Convert the extracted values to integers and return them
        red, green, blue = map(int, match[0])
        return red, green, blue
    else:
        raise ValueError("Invalid RGB string format")


def publishValueRGB(value, sensor_client):
    msg = {
        'sys_id': sensor_client.client_id,
        'payload': value
    }
    json_message = json.dumps(msg)
    sensor_client.client.publish('EV_RGB', json_message)


def update_color(sensor_client):
    red_val = red_slider.get()
    green_val = green_slider.get()
    blue_val = blue_slider.get()
    status_label.config(bg=f"#{red_val:02x}{green_val:02x}{blue_val:02x}")
    RGBValue = f'rgb({red_val},{green_val},{blue_val})'
    publishValueRGB(RGBValue, sensor_client)
    return red_val, green_val, blue_val


def update_screen_color(*args):
    red_val = red_slider.get()
    green_val = green_slider.get()
    blue_val = blue_slider.get()
    status_label.config(bg=f"#{red_val:02x}{green_val:02x}{blue_val:02x}")
    return red_val, green_val, blue_val


def change_color_from_msg(data):
    red_val, green_val, blue_val = parse_rgb(data)
    status_label.config(bg=f"#{red_val:02x}{green_val:02x}{blue_val:02x}")
    red_slider.set(red_val)
    green_slider.set(green_val)
    blue_slider.set(blue_val)
    red_slider.config(state=tk.NORMAL)
    green_slider.config(state=tk.NORMAL)
    blue_slider.config(state=tk.NORMAL)


def turn_on(sensor_client):
    red_val, green_val, blue_val = update_color(sensor_client)
    status_label.config(text="The led is now turned on.", fg="black", bg=f"#{red_val:02x}{green_val:02x}{blue_val:02x}")
    red_slider.config(state=tk.NORMAL)
    green_slider.config(state=tk.NORMAL)
    blue_slider.config(state=tk.NORMAL)


def publishStatusRGB(status, sensor_client):
    msg = {
        'sys_id': sensor_client.client_id,
        'payload': status
    }
    json_message = json.dumps(msg)
    sensor_client.client.publish('E_RGB', json_message)


def turn_on_and_publish(sensor_client):
    turn_on(sensor_client)
    publishStatusRGB('on', sensor_client)


def turn_off(sensor_client):
    status_label.config(text="The led is now turned off.", fg="white", bg="black")
    # red_slider.config(state=tk.DISABLED)
    # green_slider.config(state=tk.DISABLED)
    # blue_slider.config(state=tk.DISABLED)


def turn_off_and_publish(sensor_client):
    turn_off(sensor_client)
    publishStatusRGB('off', sensor_client)


def create_RGB_led(sensor_client):
    # Create the main window
    root = tk.Tk()
    root.title("RGB Led Simulation")

    # Define the variables as global so they can be accessed within the function
    global status_label, red_slider, green_slider, blue_slider

    # Create a label to display lamp status
    status_label = tk.Label(root, text="Lamp is off", bg="white", width=30, height=5, font=("Arial", 12))
    status_label.pack(pady=20)

    # Create RGB sliders
    red_slider = tk.Scale(root, from_=0, to=255, label="Red", orient=tk.HORIZONTAL, length=200,
                          command=update_screen_color)
    red_slider.set(0)
    red_slider.pack()

    green_slider = tk.Scale(root, from_=0, to=255, label="Green", orient=tk.HORIZONTAL, length=200,
                            command=update_screen_color)
    green_slider.set(0)
    green_slider.pack()

    blue_slider = tk.Scale(root, from_=0, to=255, label="Blue", orient=tk.HORIZONTAL, length=200,
                           command=update_screen_color)
    blue_slider.set(0)
    blue_slider.pack()

    # Create buttons to turn the lamp on and off
    on_button = tk.Button(root, text="Turn On", command=lambda: turn_on_and_publish(sensor_client), width=10, height=2)
    on_button.pack(side=tk.LEFT, padx=10)

    off_button = tk.Button(root, text="Turn Off", command=lambda: turn_off_and_publish(sensor_client), width=10,
                           height=2)
    off_button.pack(side=tk.RIGHT, padx=10)

    # Run the GUI
    root.mainloop()


########################################################################################################################
DoorLock_sensor_client = None


def get_sensor_client(client):
    global DoorLock_sensor_client
    DoorLock_sensor_client = client


def update_screen(value):
    current_text = screen_label.cget("text")
    if current_text == "Door open" or current_text == "Door close" or current_text == "Not correct":
        clear_screen()
    screen_label.config(text=screen_label.cget("text") + value)


def clear_screen():
    screen_label.config(text="")


def check_password():
    entered_password = screen_label.cget("text")
    msg = {
        'sys_id': DoorLock_sensor_client.client_id,
        'payload': ''
    }

    if entered_password == "1234*":
        screen_label.config(text="Door open")
        msg['payload'] = 'open'
        json_message = json.dumps(msg)
        DoorLock_sensor_client.client.publish('E_DoorLock', json_message)
    else:
        screen_label.config(text="Not correct")
        msg['payload'] = 'close'
        json_message = json.dumps(msg)
        DoorLock_sensor_client.client.publish('E_DoorLock', json_message)


def check_signal(payload):
    if payload == "open":
        screen_label.config(text="Door open")
    else:
        screen_label.config(text="Door close")


def DoorLock_Simulation():
    # Define the matrix of numbers
    number_matrix = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
        ["*", "0", "#"]
    ]

    # Create the main window
    root = tk.Tk()
    root.title("Number Matrix")

    # Create a frame to hold the screen
    screen_frame = tk.Frame(root)
    screen_frame.pack(pady=10)

    # Create the screen label as a global variable
    global screen_label
    screen_label = tk.Label(screen_frame, text="", font=("Arial", 20), width=15, height=2, bg="white", relief="solid",
                            borderwidth=1)
    screen_label.pack()

    # Create a frame to hold the matrix
    matrix_frame = tk.Frame(root)
    matrix_frame.pack()

    # Create labels for each element in the matrix
    for row_idx, row in enumerate(number_matrix):
        for col_idx, value in enumerate(row):
            label = tk.Button(matrix_frame, text=value, font=("Arial", 20), width=5, height=2, relief="solid",
                              borderwidth=1,
                              command=lambda val=value: update_screen(val))
            label.grid(row=row_idx, column=col_idx, padx=5, pady=5)

    # Create an "Enter" button
    enter_button = tk.Button(root, text="Enter", font=("Arial", 16), width=10, command=check_password)
    enter_button.pack(pady=5)

    # Create a "Clear" button
    clear_button = tk.Button(root, text="Clear", font=("Arial", 16), width=10, command=clear_screen)
    clear_button.pack(pady=5)

    # Run the GUI
    root.mainloop()
