import logging
from pydantic import BaseSettings

log = logging.getLogger("test_bot")

config = None


class Settings(BaseSettings):
    version: str
    client_id: str
    client_secret: str
    username: str
    password: str
    subreddit: str
    word_count: int
    days: int
    check_before_posting: int
    make_sticky: int

    class Config:
        env_file = ".env"

    @property
    def user_agent(self):
        return f"script:WordCountBot:v{self.version} (by /u/thillsd)"


def setup_config():
    global config

    config = Settings()
    log.debug(f"Running with conf: {dict(config)!r}")
