import logging
from itertools import takewhile
import datetime
from .config import config
import humanize
from rich.syntax import Syntax
from rich.console import Console
from rich.prompt import Prompt

log = logging.getLogger("wordcountbot")


SUBMISSION_BODY = "In the last {days} days, the following comments were longer than {word_count} words:\n\n"
SUBMISSION_LINK = "- **[{name}](https://reddit.com{permalink})** in **{title}** @ {ago}\n"


def newer_than(days):
    today = datetime.datetime.now()
    ago = (today - datetime.timedelta(days=days)).timestamp()

    def inner(comment):
        if comment.created_utc > ago:
            return True

    return inner


def longer_than_wordcount(comment):
    word_count = len(comment.body.split(" "))
    if word_count > int(config.word_count):
        return True


def main(reddit):
    comments = filter(
        longer_than_wordcount,
        takewhile(
            newer_than(days=int(config.days)), reddit.subreddit(config.subreddit).comments(limit=1000)
        ),
    )

    submission_title = "[{}-{}] Our Longest Comments".format(
        (datetime.date.today() - datetime.timedelta(days=int(config.days))).strftime("%d %b"),
        datetime.date.today().strftime("%d %b")
    )
    submission_body = SUBMISSION_BODY.format(
        days=int(config.days), word_count=config.word_count
    )
    for comment in comments:
        ago = humanize.naturalday(datetime.datetime.fromtimestamp(comment.created_utc))

        submission_body += SUBMISSION_LINK.format(
            name=comment.author.name if comment.author else "Deleted",
            permalink=comment.permalink,
            title=comment.submission.title,
            ago=ago,
        )

    logging.debug(f"Title: {submission_title!r}")
    Console().print(Syntax(submission_body, "md"))
    if int(config.check_before_posting):
        post = Prompt.ask(
            f"Are you sure you want to post this to /r/{config.subreddit}?",
            choices=["y", "n"],
            default="y",
        )
        if post == "n":
            log.debug("Did nothing!")
            return

    submission = reddit.subreddit(config.subreddit).submit(
        title=submission_title, selftext=submission_body
    )
    if int(config.make_sticky):
        submission.mod.sticky(state=True)
    log.debug(f"Done post at: {submission.url}")
