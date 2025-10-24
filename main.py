import asyncio
from app.pipeline import run_agents
import signal
import sys

def main():
    try:
        # Handle SIGINT (Ctrl+C) gracefully
        signal.signal(signal.SIGINT, lambda _, __: sys.exit(0))
        
        asyncio.run(run_agents())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sys.exit(0)

if __name__ == "__main__":
    main()