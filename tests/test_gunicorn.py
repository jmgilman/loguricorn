import contextlib
import errno
import os
import re
import signal
import subprocess


DEFAULT_TIMEOUT_MESSAGE = os.strerror(errno.ETIME)
LOG_PATTERN = r"^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]+ \| [A-Z]+ \s+\|"  # noqa: E501


class Timeout(contextlib.ContextDecorator):
    """A context manager for limiting execution time.

    Source: https://gist.github.com/TySkby/143190ad1b88c6115597c45f996b030c
    """

    def __init__(
        self,
        seconds,
        *,
        timeout_message=DEFAULT_TIMEOUT_MESSAGE,
        suppress_timeout_errors=False
    ):
        self.seconds = int(seconds)
        self.timeout_message = timeout_message
        self.suppress = bool(suppress_timeout_errors)

    def _timeout_handler(self, signum, frame):
        raise TimeoutError(self.timeout_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self._timeout_handler)
        signal.alarm(self.seconds)

    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.alarm(0)
        if self.suppress and exc_type is TimeoutError:
            return True


def test_gunicorn():
    # Run gunicorn with the custom logger
    p = subprocess.Popen(
        [
            "gunicorn",
            "--worker-class",
            "aiohttp.worker.GunicornWebWorker",
            "--logger-class",
            "loguricorn.Logger",
            "tests.app:app",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Capture output and kill after 5 seconds
    out: list[bytes] = []
    try:
        with Timeout(5):
            while True:
                out.append(p.stderr.readline())
    except TimeoutError:
        p.kill()

    # Assert that the log lines are formatted correctly
    for line in out:
        assert re.match(LOG_PATTERN, line.decode("utf-8")) is not None

    # Run gunicorn without the custom logger
    p = subprocess.Popen(
        [
            "gunicorn",
            "--worker-class",
            "aiohttp.worker.GunicornWebWorker",
            "tests.app:app",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Capture output and kill after 5 seconds
    out: list[bytes] = []
    try:
        with Timeout(5):
            while True:
                out.append(p.stderr.readline())
    except TimeoutError:
        p.kill()

    # Assert that the log lines are not formatted correctly
    for line in out:
        assert re.match(LOG_PATTERN, line.decode("utf-8")) is None
