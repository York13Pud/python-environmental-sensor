# --- Import the required libraries / modules:
from modules.database.engine import Base, engine
from modules.database.crud import add_reading
from modules.displays.displays import initialise_lcd, output_to_lcd, output_to_console
from modules.env.env_vars import load_env_vars
from modules.logging.log_config import load_logging
from modules.sensors.sensors import initialise_sensor, get_readings

import logging
import os


def main() -> None:
    """_summary_
    This is the main function that controls the execution flow of the program.
    
    Returns:
        None: Nothing is returned.
    """
    
    # --- Load the environment variables:
    load_env_vars()
    
    # --- Setup the database:
    Base.metadata.create_all(engine)
    
    # --- Create a sensor object:
    sensor = initialise_sensor()

    # --- Determine if LCD screen output is required:
    if os.getenv("LCD_SCREEN_CONNECTED") in ["True", "true", "TRUE", "1"]:
        OUTPUT_TO_LCD_REQUIRED: bool = True
        
        # --- Initialise the LCD screen:
        lcd_screen = initialise_lcd()
    else:
        OUTPUT_TO_LCD_REQUIRED: bool = False

    # --- Determine if console output is required:
    if os.getenv("OUTPUT_TO_CONSOLE") in ["True", "true", "TRUE", "1"]:
        OUTPUT_TO_CONSOLE_REQUIRED: bool = True
    else:
        OUTPUT_TO_CONSOLE_REQUIRED: bool = False
    
    # --- Get a new set of readings from the sensor:
    readings: dict = get_readings(sensor = sensor)
    
    # --- Add readings data to database:
    add_reading(readings = readings)
    
    # --- Show the results on the displays (if set to do so):
    if OUTPUT_TO_LCD_REQUIRED == True or OUTPUT_TO_CONSOLE_REQUIRED == True:
    
    # --- If console output is required, output the values to the console:
        if OUTPUT_TO_CONSOLE_REQUIRED == True:
            output_to_console(readings = readings)
        
        # --- If LCD screen output is required, output the values to the LCD screen:
        if OUTPUT_TO_LCD_REQUIRED == True:
            # --- Pass the values of the sensor to the output_to_lcd function:
            output_to_lcd(readings = readings,
                          display = lcd_screen)


# --- Start the program:
if __name__ == "__main__":
    # --- Initialise logging:
    load_logging()
    
    # --- Get the currently active logger:
    log = logging.getLogger(__name__)
    
    # --- Attempt to run the main function:
    try:
        main()
    except NameError:
        message = "Unable to locate or run main function. Please check the program is setup correctly."
        log.critical(message)
        raise Exception(message)
