import asyncio
from app.pipeline import run_agents

def main():
    try:
        asyncio.run(run_agents())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()