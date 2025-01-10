# --- Import the required libraries / modules:
from adafruit_bme280 import basic as adafruit_bme280

import board
import logging


# --- Get the currently active logger:
log = logging.getLogger(__name__)


# --- Attempt to initialise the sensor on the i2c bus using the default values:
def initialise_sensor() -> object:
    """_summary_
    This function provides the application with the methods required to
    interact with an Adafruit bme280 sensor.
        
    Returns:
        class: An object that contains the methods for interacting with 
               an Adafruit bme280 sensor.
    """
    
    # --- Initialise the i2c interface for the sensor:
    try:
        i2c = board.I2C()  # --- uses board.SCL and board.SDA. Add i2c interface number.
    except OSError as error:
        message = "Unable to connect to the i2c interface. Please check that it is enabled."
        log.error(message)
        raise Exception(message)
    except ValueError as error:
        message = "Unable to connect to the i2c interface. Please check that it is enabled."
        log.error(message)
        raise Exception(message)
    
    # --- Initialise the bme280 sensor:
    try:
        sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c)
    except OSError as error:
        message = "No sensor board was found. Please check that it is connected."
        log.critical(message)
        raise Exception(message)
    except ValueError as error:
        message = "No sensor board was found. Please check that it is connected."
        log.critical(message)
        raise Exception(message)
    
    # --- change this to match the location's pressure (hPa) at sea level.
    sensor.sea_level_pressure = 1027

    return sensor


def get_readings(sensor: object) -> dict:
    """_summary_
    This function will make a call to the sensor to get the current sensor readings and
    store them in a dictionary that will be returned to the caller.
    
    Args:
        sensor (object): This is the object containing the initialised sensor object.

    Returns:
        dict: Returns a dictionary with the keys / values for the temperature, 
              humidity, pressure and altitude. All values are floats, rounded to
              two decimal places.
    """
    
    try:
        readings = {
            "temperature": round(float(sensor.temperature), 2),
            "humidity": round(float(sensor.humidity), 2),
            "pressure": round(float(sensor.pressure), 2),
            "altitude": round(float(sensor.altitude), 2)
        }
    except OSError as error:
        message = f"Unable to get readings from the sensor. Please check the sensor is connected and active."
        log.error(message)
        raise Exception(message)

    return readings