import logging

from rich.logging import RichHandler
from rich.traceback import install

# rich exception handler
install(show_locals=True)


# setup logging
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("wordcountbot")
logging.getLogger('praw').setLevel(logging.WARNING)
logging.getLogger('requests').setLevel(logging.WARNING)

# setup config
from . import config
config.setup_config()
from .config import config
config['user_agent'] = f"script:WordCountBot:v{config.version} (by /u/thillsd)"


import praw
from .countwords import main


if __name__ == "__main__":
    reddit = praw.Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent,
        username=config.username,
        password=config.password)

    main(reddit)