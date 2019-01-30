#! /usr/bin/env/ python

import datetime
from server import *

#############################
#!# The Door Main Program #!#
#############################

if __name__ == "__main__":

    date = datetime.datetime.now()
    file_path = "/opt/the-door/log/{}{}".format(date.strftime("%Y-%m-%d"), ".log")

    # Uses %(<dictionary key>)s styled string substitution; the possible keys are documented in LogRecord attributes.
    log_format = "[ %(asctime)s ]\t[ %(levelname)s ]\t%(message)s"

    # Create logger Object
    logger = logging.getLogger("log")
    logging.basicConfig(format=log_format,
                        filename=file_path)  # Pass the filename and the log strings format used in file logs
    logger.setLevel(logging.DEBUG)  # Set logging level to DEBUG

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Can select a different logging lvl for the console if needed

    # Create formatter
    formatter = logging.Formatter(log_format)

    # Add the formatter to console handler
    console_handler.setFormatter(formatter)

    # Add the console handler to logger
    logger.addHandler(console_handler)

    logger.debug("Log opened")

    server = Server(logger)
    server.run()

    logger.debug("Log closed")
