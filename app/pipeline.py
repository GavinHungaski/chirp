import asyncio
import logging
from app.agents.listen import listen
from app.agents.think import think
from app.agents.speak import speak


# module logger (will be used if no logger passed)
logger = logging.getLogger(__name__)

# shared message queue for agents
message_queue = asyncio.Queue()


async def run_agents(logger: logging.Logger = None):
    logger = logger or logging.getLogger(__name__)

    logger.info("Starting pipeline (agents)")

    tasks = [
        asyncio.create_task(listen(logger, message_queue), name="listen"),
        asyncio.create_task(think(message_queue), name="think"),
        asyncio.create_task(speak(message_queue), name="speak"),
    ]

    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, BaseException) and not isinstance(r, asyncio.CancelledError):
                logger.error("Task finished with exception: %s", r)

    except asyncio.CancelledError:
        logger.info("Pipeline tasks cancelled")
        raise

    except Exception as e:
        logger.exception("Unhandled exception in pipeline: %s", e)
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    finally:
        logger.info("Pipeline has been shut down.")
