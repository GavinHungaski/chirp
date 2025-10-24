import customtkinter
import logging


class App(customtkinter.CTk):
    def __init__(self, logger: logging.Logger = None):
        super().__init__()
        self.title("Chirp")
        self.geometry("400x300")
        self.logger = logger

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    def button_callback(self):
        if self.logger:
            self.logger.info("Button clicked")

def ui(logger: logging.Logger = None):
    if logger:
        logger.info("UI started")
    app = App(logger=logger)
    app.mainloop()
