import logging

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
# #logger.setLevel(logging.INFO)  # Set the log level
# logger.setLevel(logging.DEBUG)  # Set the log level

# # set logging level for fonttools to warning
# logging.getLogger("fontTools").setLevel(logging.WARNING)

# # Create a console handler and set its level and format
# console_handler = logging.StreamHandler()
# #console_handler.setLevel(logging.INFO)
# console_handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# console_handler.setFormatter(formatter)

# # Add the console handler to the logger
# logger.addHandler(console_handler)


# Create a custom logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set logger's level to capture DEBUG and above

# Remove any existing handlers (to avoid duplicate logging)
if logger.hasHandlers():
    logger.handlers.clear()

# Create a console handler with the same log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the custom logger
logger.addHandler(console_handler)
logger.propagate = False

# Configure external libraries as needed
logging.getLogger("fontTools").setLevel(logging.WARNING)