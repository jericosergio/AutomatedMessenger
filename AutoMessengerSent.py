import tkinter as tk
from tkinter import ttk
    # pip install tkinter
import pyautogui
    # pip install pyautogui
import time
import threading
from datetime import datetime, timedelta
from pynput import keyboard
    # pip install pynput

# Global variables to hold the state
pinned_location = None
is_running = False  # Flag to control if the automation is running
is_paused = False   # Flag to control if the automation is paused
interval_mode = "seconds"  # Default interval mode
location_updating = True  # Controls whether location updates are active
timestamp_format = "%H:%M"  # Default timestamp format
remaining_time = None  # Stores the remaining time for countdown

def update_location_display():
    """Updates the location display in real-time."""
    while True:
        if location_updating:
            x, y = pyautogui.position()
            location_var.set(f"Current Position: ({x}, {y})")
        time.sleep(0.1)

def update_time_display():
    """Updates the current time display in real-time."""
    while True:
        current_time_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(1)

def toggle_location_update():
    """Toggles the location update and pins/unpins the location display."""
    global location_updating, pinned_location
    if location_updating:
        # Pin the location and stop updates
        pinned_location = pyautogui.position()
        location_display.config(background="lightgreen")
        location_var.set(f"Pinned Location: {pinned_location}")
        location_updating = False
    else:
        # Unpin the location and resume updates
        location_display.config(background="white")
        location_updating = True

def set_interval_mode(mode):
    """Set interval mode to seconds or minutes."""
    global interval_mode
    interval_mode = mode

def update_status(message, color="black"):
    """Update the status message displayed on the GUI."""
    status_label.config(text=message, foreground=color)

def set_timestamp_format(format_option):
    """Set the timestamp format based on user selection."""
    global timestamp_format
    format_map = {
        "HH:MM": "%H:%M",
        "HH:MM:SS": "%H:%M:%S",
        "HH:MM:SS AM/PM": "%I:%M:%S %p",
        "HH:MM:SS AM/PM Date": "%I:%M:%S %p %Y-%m-%d"
    }
    timestamp_format = format_map[format_option]

def start_automation(event=None):
    """Starts the message automation based on user input."""
    global is_running, is_paused, pinned_location, remaining_time

    if not pinned_location:
        update_status("Please pin the chat box location first.", "red")
        return

    try:
        message = message_entry.get()
        interval = int(interval_entry.get())

        if interval_mode == "minutes":
            interval *= 60  # Convert minutes to seconds

        if not message:
            update_status("Please enter a message.", "red")
            return

        if interval <= 0:
            update_status("Please enter a valid interval.", "red")
            return

        if is_running:
            update_status("Automation is already running.", "orange")
            return

        # Start the automation in a separate thread
        is_running = True
        is_paused = False
        start_button.config(style="Running.TButton")
        pause_button.config(style="Paused.TButton")
        remaining_time = interval  # Set the initial countdown time
        threading.Thread(target=send_message, args=(message, interval), daemon=True).start()
        threading.Thread(target=update_countdown, args=(interval,), daemon=True).start()
        update_status(f"Automation started. Message: '{message}' every {interval} seconds.", "green")

    except ValueError:
        update_status("Invalid interval. Please enter a number.", "red")

def send_message(message, interval):
    """Sends the specified message at the pinned location every specified interval."""
    global is_running, is_paused
    while is_running:
        if not is_paused:
            # Insert timestamp in the message at [timestamp] placeholder
            timestamp = datetime.now().strftime(timestamp_format)
            formatted_message = message.replace("[timestamp]", timestamp)
            
            pyautogui.click(pinned_location)  # Click on the pinned location to focus the input box
            time.sleep(0.5)  # Small delay to ensure the chat box is active
            pyautogui.typewrite(formatted_message)  # Type the message
            pyautogui.press('enter')  # Press Enter to send
            time.sleep(interval)  # Wait for the specified interval before sending again

def update_countdown(interval):
    """Updates the countdown timer on the GUI."""
    global remaining_time
    while is_running:
        if not is_paused and remaining_time is not None:
            for i in range(remaining_time, 0, -1):
                if is_paused or not is_running:
                    break
                countdown_var.set(str(timedelta(seconds=i)))
                time.sleep(1)
            remaining_time = interval
        else:
            time.sleep(1)

def pause_automation(event=None):
    """Pauses the automation."""
    global is_paused
    if is_running:
        is_paused = not is_paused
        state = "paused" if is_paused else "resumed"
        pause_button.config(style="Paused.TButton" if is_paused else "Running.TButton")
        update_status(f"Automation {state}.", "orange" if is_paused else "green")

def stop_automation(event=None):
    """Stops the automation."""
    global is_running, is_paused, remaining_time
    if is_running:
        is_running = False
        is_paused = False
        remaining_time = None
        start_button.config(style="TButton")
        pause_button.config(style="TButton")
        update_status("Automation stopped.", "red")
        countdown_var.set("00:00:00")

def setup_keybindings():
    """Setup keybindings for various automation actions."""
    listener = keyboard.GlobalHotKeys({
        '<ctrl>+p': toggle_location_update,  # Toggle location updates
        '<ctrl>+s': start_automation,        # Start automation
        '<ctrl>+r': pause_automation,        # Pause/Resume automation
        '<ctrl>+x': stop_automation          # Stop automation
    })
    listener.start()

# Set up the GUI
root = tk.Tk()
root.title("Automated Messenger")

# Apply a modern theme
style = ttk.Style()
style.theme_use('clam')

# Define button styles
style.configure("Running.TButton", background="green", foreground="white")
style.configure("Paused.TButton", background="yellow", foreground="black")

# Create main frame
main_frame = ttk.Frame(root)
main_frame.pack(padx=10, pady=10, expand=True, fill="both")

# Create left and right columns
left_frame = ttk.Frame(main_frame)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

right_frame = ttk.Frame(main_frame)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Configure grid layout to be resizable
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(0, weight=1)

# Variables for dynamic display
location_var = tk.StringVar()
location_var.set("Current Position: (0, 0)")

# Real-time location display
location_display = ttk.Label(left_frame, textvariable=location_var, background="white", width=40)
location_display.pack(pady=5, fill="x")
location_display.bind("<Button-3>", toggle_location_update)  # Right-click to set location

# Status message display
status_label = ttk.Label(left_frame, text="", foreground="black")
status_label.pack(pady=5, fill="x")

# Instructions and input fields
ttk.Label(left_frame, text="Enter the message (use [timestamp] for time):").pack(pady=5, fill="x")
message_entry = ttk.Entry(left_frame)
message_entry.pack(pady=5, fill="x")

ttk.Label(left_frame, text="Enter interval:").pack(pady=5, fill="x")
interval_entry = ttk.Entry(left_frame)
interval_entry.pack(pady=5, fill="x")

# Interval mode variable and radio buttons
interval_var = tk.StringVar(value="seconds")  # Controls the radio button state
ttk.Radiobutton(left_frame, text="Seconds", variable=interval_var, value="seconds", 
               command=lambda: set_interval_mode("seconds")).pack(anchor="w")
ttk.Radiobutton(left_frame, text="Minutes", variable=interval_var, value="minutes", 
               command=lambda: set_interval_mode("minutes")).pack(anchor="w")

# Dropdown menu to select timestamp format
ttk.Label(left_frame, text="Select timestamp format:").pack(pady=5, fill="x")
timestamp_format_var = tk.StringVar(value="HH:MM")
timestamp_options = ["HH:MM", "HH:MM:SS", "HH:MM:SS AM/PM", "HH:MM:SS AM/PM Date"]
timestamp_menu = ttk.OptionMenu(left_frame, timestamp_format_var, *timestamp_options, command=set_timestamp_format)
timestamp_menu.pack(pady=5, fill="x")

# Pin location button
pin_button = ttk.Button(left_frame, text="<ctrl>+p: Toggle Pin Location", command=toggle_location_update)
pin_button.pack(pady=10, fill="x")

# Start button
start_button = ttk.Button(left_frame, text="<ctrl>+s: Start Automation", command=start_automation)
start_button.pack(pady=5, fill="x")

# Pause button
pause_button = ttk.Button(left_frame, text="<ctrl>+r: Pause/Resume", command=pause_automation)
pause_button.pack(pady=5, fill="x")

# Stop button
stop_button = ttk.Button(left_frame, text="<ctrl>+x Stop Automation", command=stop_automation)
stop_button.pack(pady=5, fill="x")

# Countdown timer section
ttk.Label(right_frame, text="COUNTDOWN", font=("Arial", 16)).pack(pady=10)
countdown_var = tk.StringVar()
countdown_var.set("00:00:00")
countdown_label = ttk.Label(right_frame, textvariable=countdown_var, font=("Arial", 24))
countdown_label.pack(pady=10)

# Current time display
ttk.Label(right_frame, text="CURRENT TIME:", font=("Arial", 16)).pack(pady=10)
current_time_var = tk.StringVar()
current_time_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
current_time_label = ttk.Label(right_frame, textvariable=current_time_var, font=("Arial", 16))
current_time_label.pack(pady=10)

# Start real-time location display and current time display in separate threads
threading.Thread(target=update_location_display, daemon=True).start()
threading.Thread(target=update_time_display, daemon=True).start()

# Set up keybindings
setup_keybindings()

# Run the GUI
root.mainloop()
