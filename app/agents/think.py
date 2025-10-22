import asyncio

# Processor agent that thinks of a response based on input
async def think(message_queue):
    print("🧠 Processor Agent started...")
    while True:
        await asyncio.sleep(1)