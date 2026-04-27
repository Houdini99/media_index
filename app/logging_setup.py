"""StreamToLogger and rotating-file handler setup — preserved verbatim
from the original main.py.
"""
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, stream=None, log_level=logging.INFO):
        self.logger = logger
        self.stream = stream
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        # Also write to original stream (console)
        if self.stream:
            self.stream.write(buf)

        # Log to file
        temp_linebuf = self.linebuf + buf
        self.linebuf = ''
        for line in temp_linebuf.splitlines(True):
            if line[-1:] == '\n':
                self.logger.log(self.log_level, line.rstrip())
            else:
                self.linebuf += line

    def flush(self):
        if self.linebuf != '':
            self.logger.log(self.log_level, self.linebuf.rstrip())
        self.linebuf = ''
        if self.stream:
            self.stream.flush()


def configure_logging(base_dir):
    """Set up rotating file logging and redirect stdout/stderr through it."""
    log_dir = os.path.join(base_dir, 'log')
    os.makedirs(log_dir, exist_ok=True)

    # Set up logger for stdout
    stdout_logger = logging.getLogger('STDOUT')
    stdout_logger.setLevel(logging.INFO)

    # Set up logger for stderr
    stderr_logger = logging.getLogger('STDERR')
    stderr_logger.setLevel(logging.ERROR)

    # Create TimedRotatingFileHandler for daily rotation
    log_path = os.path.join(log_dir, "app.log")
    stdout_handler = TimedRotatingFileHandler(log_path, when="midnight", interval=1)
    stdout_handler.suffix = "%Y-%m-%d"
    stdout_formatter = logging.Formatter('%(asctime)s [STDOUT] %(message)s')
    stdout_handler.setFormatter(stdout_formatter)

    stderr_handler = TimedRotatingFileHandler(log_path, when="midnight", interval=1)
    stderr_handler.suffix = "%Y-%m-%d"
    stderr_formatter = logging.Formatter('%(asctime)s [STDERR] %(message)s')
    stderr_handler.setFormatter(stderr_formatter)

    # Add handlers to loggers
    stdout_logger.addHandler(stdout_handler)
    stderr_logger.addHandler(stderr_handler)

    # Redirect stdout and stderr to loggers while keeping console output
    sys.stdout = StreamToLogger(stdout_logger, sys.stdout, logging.INFO)
    sys.stderr = StreamToLogger(stderr_logger, sys.stderr, logging.ERROR)
