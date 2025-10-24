import customtkinter
import logging


def ui(logger: logging.Logger = None):
    if logger:
        logger.info("UI started")
    app = customtkinter.CTk()
    app.title("Chirp")
    app.geometry("400x300")

    app.mainloop()
