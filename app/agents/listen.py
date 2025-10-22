import asyncio
from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np


# Initialize the whisper model
model = WhisperModel("base.en", device="cpu", compute_type="int8")


# Audio configuration
DEVICE_ID = 2  # Surface Stereo Microphones
SAMPLE_RATE = 16000
DURATION = 5
CHANNELS = 1
THRESHOLD = 0.01


async def listen(logger, message_queue):
    print("🎧 Listener Agent started...")
    
    # Print available devices and verify selected device
    devices = sd.query_devices()
    print(f"Using input device: {devices[DEVICE_ID]['name']}")

    while True:
        # logger.info("Listening...")
        try:
            # Record audio using specified device
            audio_data = sd.rec(
                int(SAMPLE_RATE * DURATION),
                samplerate=SAMPLE_RATE,
                channels=CHANNELS,
                dtype=np.float32,
                device=DEVICE_ID,
                blocking=True
            )

            # Check if audio level is above threshold
            if np.max(np.abs(audio_data)) < THRESHOLD:
                # logger.info("Silence detected, continuing...")
                await asyncio.sleep(0.1)
                continue

            # Flatten the array and convert to 1D
            audio_data = audio_data.flatten()

            segments, _ = model.transcribe(audio_data, beam_size=4) 

            for s in segments:
                if s.text.strip(): # Only process non-empty text
                    logger.info(f"User said: {s.text.strip()}")
                    await message_queue.put({
                        "type": "user_input",
                        "content": s.text.strip(),
                    })

        except Exception as e:
            logger.error(f"Error in listener: {e}")
            await asyncio.sleep(1)
            continue

        await asyncio.sleep(0.1)