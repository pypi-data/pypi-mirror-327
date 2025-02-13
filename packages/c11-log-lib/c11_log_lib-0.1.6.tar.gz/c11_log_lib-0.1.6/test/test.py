import os
import logging
import json_log_formatter


class Platform:
    def __init__(self):
        self.aws = {"account": os.getenv("AWS_ACCOUNT", "")}


class Release:
    def __init__(self):
        self.commit_hash = os.getenv("COMMIT_HASH", "")
        self.created_at = os.getenv("COMMIT_DATE", "")
        self.version = os.getenv("VERSION", "")


class Context:
    def __init__(self, correlation_id):
        self.version = "1.0.0"
        self.correlation_id = correlation_id
        self.service_name = os.getenv("SERVICE_NAME", "")
        self.platform = Platform().__dict__
        self.release = Release().__dict__


class Event:
    def __init__(self, action, message):
        self.action = action
        self.message = message


class Log:
    def __init__(self, correlation_id):
        self.logger = logging.getLogger("go_log")
        self.logger.setLevel(logging.DEBUG)

        formatter = json_log_formatter.JSONFormatter()
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)
        self.context = Context(correlation_id).__dict__

    def _log(self, level, action, message):
        event = Event(action, message).__dict__
        self.logger.log(level, "", extra={"context": self.context, "event": event})

    def trace(self, action, message):
        self._log(logging.DEBUG, action, message)  # Python does not have TRACE level

    def debug(self, action, message):
        self._log(logging.DEBUG, action, message)

    def info(self, action, message):
        self._log(logging.INFO, action, message)

    def warn(self, action, message):
        self._log(logging.WARNING, action, message)

    def error(self, action, message):
        self._log(logging.ERROR, action, message)


logger = Log(correlation_id="12345")

# Log an info message
logger.info("Simple test message", {"test": "value"})