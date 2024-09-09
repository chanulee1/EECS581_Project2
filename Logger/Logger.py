"""
Logger.py
Authors:
    - Pierce Lane
Date: 9/2/2024

Purpose: all-purpose logging functions for battleship
"""
from datetime import datetime
import os

# the only global you will ever see me defining in such an object-oriented program
LOG_FILE_NAME = "log.txt"

def clear_log():
    """Deletes everything inside the log, 
    will make a new log if there was not one already"""
    # try to open the file and clear it
    try:
        # open the file
        with open(LOG_FILE_NAME, "w") as log:
            # clear it
            log.write("")
    # if there was no file there
    except FileNotFoundError:
        # make one
        __make_log_file()

def log(log_str):
    """Will log log_str to global log file with timestamp.
    log_str should have the function that it was called from at the beginning
    ex. "foo(bar): Encountered internal exception doing x thing"
    If no log file exists, will make one
    @param log_str: string containing log information
    """
    # note for later:
        # could add in different levels of logs
        #  1 - debugging
        #  2 - warning
        #  3 - error (not crash-inducing)
        #  4 - critical error (crash-inducing)

    # define what now is
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # prepend it to the log_str
    log_str = f"{now} : {log_str}\n"

    print(log_str, end="")
    # try to make a log file
    try:
        # open it
        with open(LOG_FILE_NAME, "a") as log:
            # write to it
            log.write(log_str)

    # if there was not a file there
    except FileNotFoundError:
        # make it
        __make_log_file()
        # open it
        with open(LOG_FILE_NAME, "a") as log:
            # write to it
            log.write(log_str)

def __make_log_file():
    """Makes a new log file from nothing!
    @return bool: returns True on success, False on failure"""
    # try to make the file, if this doesn't work we'll send a message
    try:
        # Use os.path.join to ensure compatibility with all OS path formats
        log_dir = os.path.dirname(LOG_FILE_NAME)

        # Create the directories if they don't exist
        os.makedirs(log_dir, exist_ok=True)

        # Create the log file
        with open(LOG_FILE_NAME, "w") as log:
            # Initialize the log file with a header or leave it empty
            log.write("Log file created on {}\n".format(datetime.now()))

        # return True on success
        return True

    # except anything
    except Exception as e:
        # If there is any error, return False
        print(f"Error creating log file: {e}")
        # return False on failure
        return False
