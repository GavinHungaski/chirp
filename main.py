# ---------------------------------------------------------------------------- #
#                                                                              #
#   Main entry point for the application.                                      #
#   Sets up logging and starts the user interface.                             #
#                                                                              #
# ---------------------------------------------------------------------------- #

import logging
from app.ui.main_ui import ui

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("pipeline.log"),
            logging.StreamHandler()
        ],
    )
    root_logger = logging.getLogger()
    ui(logger=root_logger)

if __name__ == "__main__":
    main()
