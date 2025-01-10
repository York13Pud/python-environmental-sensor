# --- Import the required libraries / modules:
import logging
import os


def load_logging():
    """_summary_
    This function will setup the logging facility for the program.
    
    Returns:
        None: Nothing is returned.
    """
    
    # --- Get the root folder path that the app is stored in:
    LOG_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "logs"))
    
    # --- Check if the log folder exists. If not, create it:
    if os.path.exists(LOG_FOLDER_PATH) == False:
        os.mkdir(path = LOG_FOLDER_PATH)
    
    # --- Setup the logging:    
    log_file = f"{LOG_FOLDER_PATH}/error.log"
    
    # --- Define the configuration for the logging:
    logging.basicConfig(filename = log_file, 
                        encoding = "utf-8", 
                        level = logging.ERROR,
                        format='%(levelname)s:%(asctime)s:%(name)s:%(message)s')
    