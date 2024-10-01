import asyncio
import os
from pathlib import Path

# Change dir to project root (three levels up from this file)
os.chdir(Path(__file__).parents[2])

from src.bot.app import main  # noqa: E402

# NOTE: No need for if __name__ == "__main__":, because this is the __main__.py module already
asyncio.run(main())
