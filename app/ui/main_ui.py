import threading
import asyncio
import logging
import customtkinter
import app.pipeline as pipeline


class App(customtkinter.CTk):
    def __init__(self, logger: logging.Logger = None):
        super().__init__()
        self.title("Chirp")
        self.geometry("400x300")
        self.logger = logger or logging.getLogger(__name__)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # Start pipeline button
        self.start_button = customtkinter.CTkButton(
            self, text="Start Agents", command=self.on_start_agents
        )
        self.start_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Simple log/output area
        self.log_widget = customtkinter.CTkTextbox(self, wrap="word")
        self.log_widget.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.log_widget.insert("0.0", "UI ready.\n")

    def on_start_agents(self):
        self.logger.info("Start button clicked; spawning pipeline thread")
        self.start_button.configure(state="disabled")
        thread = threading.Thread(target=self._run_pipeline_thread, daemon=True)
        thread.start()

    def _run_pipeline_thread(self):
        try:
            asyncio.run(pipeline.run_agents(logger=self.logger))
        except Exception as e:
            self.logger.exception("Pipeline thread stopped with exception: %s", e)
            # Show the error in UI log widget in a thread-safe way
            self._insert_log(f"Pipeline error: {e}\n")

    def _insert_log(self, text: str):
        def _append():
            self.log_widget.insert("end", text)
            self.log_widget.see("end")

        # Tk must be updated in main thread
        self.after(0, _append)


def ui(logger: logging.Logger = None):
    if logger:
        logger.info("UI starting")
    app = App(logger=logger)
    app.mainloop()
