from box import Box
from dotenv import dotenv_values
import os
import logging

log = logging.getLogger("test_bot")

config = None


def setup_config():
    global config

    config = Box(
        {**dotenv_values(".env"), **os.environ}  # load shared development variables
    )
    log.debug(f"Running with conf: {dict(config)!r}")
