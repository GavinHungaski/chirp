import asyncio
import logging
from app.agents.listen import listen
from app.agents.think import think
from app.agents.speak import speak
from app.ui.main_ui import ui


# Basic logger
logging.basicConfig(
    level=logging.INFO,
    format=" %(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers = [
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# Main function to run the pipeline
async def run():
    try:
        # The message queue used for inter-component communication
        message_queue = asyncio.Queue()
        ui_queue = asyncio.Queue()

        logger.info("Starting pipeline")

        tasks = [
            asyncio.create_task(ui(logger, message_queue, ui_queue), name="ui"),
            asyncio.create_task(listen(logger, message_queue), name="listen"),
            asyncio.create_task(think(message_queue), name="think"),
            asyncio.create_task(speak(message_queue), name="speak"),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, BaseException) and not isinstance(r, asyncio.CancelledError):
                logger.error("Task finished with exception: %s", r)

    # Gracefully shut down and handle logging of errors
    except KeyboardInterrupt:
        logger.info("Shutting down (KeyboardInterrupt)...")
        for t in tasks:
            t.cancel()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, BaseException) and not isinstance(r, asyncio.CancelledError):
                logger.error(f"Task ended with exception: {r}")
    
    except Exception as e:
        logger.exception(f"Unhandled exception occurred: {e}")
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    finally:
        logger.info("Pipeline has been shut down.")
