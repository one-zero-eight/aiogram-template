import asyncio
import os

from src.prepare import BASE_DIR, prepare

os.chdir(BASE_DIR)

prepare()

from src.bot.app import main  # noqa: E402

# NOTE: No need for if __name__ == "__main__":, because this is the __main__.py module already
asyncio.run(main())
