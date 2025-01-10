# --- Import the required libraries / modules:
from datetime import datetime as dt
from RPLCD.i2c import CharLCD

import json
import logging
import os


# --- Get currently active logger:
log = logging.getLogger(__name__)


def initialise_lcd():
    """_summary_
    This function will attempt to initialise the LCD screen that is attached to the system.

    _Arguments_
    No arguments are required.
    
    Returns:
        class: A class called lcd that has the settings for an initialised LCD display.
    """
    
    # --- Specify the path to the display’s config file:
    config_file_path = f"{os.path.abspath(os.path.join(os.path.dirname(__file__)))}/config.json"
    
    # --- Check if the config.json file is present:
    if os.path.exists(config_file_path) == False:
        message = f"The config.json file was not found. Please check that this file exists."
        log.error(message)
        raise Exception(message)
    
    # --- Load the config file to a dictionary:
    with open(config_file_path) as config_file:
        config = json.load(config_file)
    
    # --- Get the screen type:
    screen_type = os.getenv("LCD_SCREEN_TYPE")
    
    # --- If the screen_type matches an entry in config (config.json), initialise the display
    # --- Otherwise, raise an error:
    if screen_type in config.keys():
        
        # --- Create a screen object:
        try:
            lcd = CharLCD(i2c_expander = config[screen_type]["i2c_expander"], 
                        address = int(config[screen_type]["address"], 0),
                        port = config[screen_type]["port"], 
                        cols = config[screen_type]["cols"], 
                        rows = config[screen_type]["rows"], 
                        dotsize = config[screen_type]["dotsize"])
            
        except OSError as error:
            message = f"Display could not be found. Please check the display is connected."
            log.error(message)
            raise Exception(message)
            
        except NotImplementedError as error:
            message = f"The display expander is not supported. Please check the display configuration."
            log.error(message)
            raise Exception(message)
    
    else:
        message = f"Display could not be found. Please check the display is connected."
        log.error(message)
        raise Exception(message)

    return lcd


def output_to_lcd(readings: dict, display: object) -> None:
    """_summary_

    Args:
        temperature (float): The temperature to display.
        humidity (float): The humidity to display.
        pressure (float): The pressure to display.
        altitude (float): The altitude to display.
        display (_type_): The display settings to use.
    Returns:
        None: Nothing is returned.
    """
    try:   
        display.clear()
        
        if display.lcd.cols == 20 and display.lcd.rows == 4:
            display.write_string(f"Temp:     {readings['temperature']}{chr(223)}C\r\n")
            display.write_string(f"Humidity: {readings['humidity']}%\r\n")
            display.write_string(f"Pressure: {readings['pressure']}hpa\r\n")
            display.write_string(f"Altitude: {readings['altitude']}m")
        else:
            display.write_string(f"Temp: {readings['temperature']}{chr(223)}C\r\n")
            display.write_string(f"Humi: {readings['humidity']}%\r\n")
    except OSError as error:
        message = f"Display could not be found. Please check the display is connected."
        log.error(message)
        raise Exception(message)


def output_to_console(readings: dict) -> None:
    """_summary_
    This function will display the readings of the sensor to the console.
    
    Args:
        readings (dict): The dictionary containing the readings from the sensor
        
    Returns:
        None: Nothing is returned.
    """
    
    # --- Clear the output on the terminal console:
    os.system('clear')
    
    # --- Display the values to the terminal console:
    print(dt.now().strftime("%d/%m/%Y, %H:%M:%S\n"))
    print(f"Temperature: {readings['temperature']}°C")
    print(f"Humidity: {readings['humidity']}%")
    print(f"Pressure: {readings['pressure']}hPa")
    print(f"Altitude: {readings['altitude']}m")