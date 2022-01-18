==============
Word Count Bot
==============

When run, posts a new thread listing the comments from the past week with high word counts.


Install
-------

1. Install python 3.8+.
2. Install `Poetry <https://python-poetry.org/docs/#installation/>`_
3. ``cd`` into the project directory and run ``poetry install`` to install dependencies.
4. Copy-paste and edit this ``.env`` file and save it in the project root directory

.. code-block:: txt

    version=0.1
    client_id=
    client_secret=
    username=
    password=
    subreddit=
    word_count=300
    days=7
    check_before_posting=1
    make_sticky=1

5. From the project root, run ``poetry run python -m wordcountbot``.
6. If you want to run this automatically, set up hosting, make sure ``check_before_posting`` is set to 0 and run automatically using a ``cron`` job or similar.

Limitations
-----------

Only retrieves the last 1000 comments from a sub as per the current reddit API.