import asyncio

# Speaker agent that reads messages from the queue and "speaks" them out
async def speak(message_queue):
    print("🗣️  Speaker Agent started...")
    while True:
        await asyncio.sleep(1)