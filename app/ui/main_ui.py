import customtkinter
import asyncio
import logging


async def ui(logger: logging.Logger = None, message_queue: asyncio.Queue = None, ui_queue: asyncio.Queue = None):
    if logger:
        logger.info("UI started")
    app = customtkinter.CTk()
    app.title("Chirp UI")
    app.geometry("400x300")

    await asyncio.get_event_loop().run_in_executor(None, app.mainloop)
    