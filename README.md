# Automated Messenger

This Python-based application allows you to automatically send messages at specified intervals, specific times, or at random intervals within an hour. It's a versatile tool that can be customized through a dynamic graphical user interface (GUI).

## Features

### 1. Random Intervals Mode
- **Minimum Interval**: The shortest time between messages.
- **Maximum Interval**: The longest time between messages.

### 2. Specific Time Mode
- **Specific Minute**: The exact minute of each hour when the message should be sent.

### 3. Interval Mode
- **Custom Intervals**: Set intervals in seconds or minutes for message automation.

### 4. Dynamic GUI Elements
- **Dynamic Input Field Handling**: The input fields are automatically shown or hidden based on the selected mode:
    - **Interval Mode**: Shows interval input fields and radio buttons for seconds/minutes.
    - **Specific Time Mode**: Shows the specific minute input field.
    - **Random Intervals Mode**: Shows the random minute range input field.

### 5. Instructions and Validation
- **Instructions**: Clear instructions are provided within the GUI.
- **Input Validation**: Ensures that all entered values are correct and logical.

## Installation

### Prerequisites
1. Install Python from [python.org](https://www.python.org/).

### Python Dependencies
Run the following commands to install the required Python libraries:

### on cmd
pip install tkinter
pip install pyautogui
pip install pynput

### Running the Script
After installing the dependencies, you can run the script using:

bash
Copy code
python script_name.py

### Usage
Once the script is running, the GUI will provide you with options to select the desired mode:

Interval Mode: Enter the interval in seconds or minutes and start the automation.
Specific Time Mode: Enter the specific minute (e.g., 05 for 5 minutes past the hour) and the message will be sent at that time every hour.
Random Intervals Mode: Set the range for random intervals (e.g., between 5 and 15 minutes) and the message will be sent at a random minute within that range each hour.

Key Bindings
- Ctrl + P: Toggle the pin location for the message.
- Ctrl + S: Start the automation.
- Ctrl + R: Pause/Resume the automation.
- Ctrl + X: Stop the automation.

Bored Programmer: Mat Jerico Sergio, CCSYB (2024 MIS HEAD)