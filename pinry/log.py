import logging


class OneLineFormatter(logging.Formatter):
    """Log the message without a traceback.

    Used for django.security, where the message already says what was wrong
    (e.g. which Host header was rejected) and a traceback per request would
    flood the log when bots probe the server.
    """

    def format(self, record):
        record = logging.makeLogRecord(record.__dict__)
        record.exc_info = None
        record.exc_text = None
        return super().format(record)
