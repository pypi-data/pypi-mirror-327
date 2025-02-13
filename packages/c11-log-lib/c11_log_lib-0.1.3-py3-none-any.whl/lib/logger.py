import os
import structlog


class Platform:
    def __init__(self):
        self.aws = {"account": os.getenv("AWS_ACCOUNT", "")}


class Release:
    def __init__(self):
        self.commit_hash = os.getenv("COMMIT_HASH", "")
        self.created_at = os.getenv("COMMIT_DATE", "")
        self.version = os.getenv("VERSION", "")


class Session:
    def __init__(self, uid="", type_=""):
        self.uid = uid
        self.type = type_


class User:
    def __init__(self, uid, type_):
        self.uid = uid
        self.type = type_


class Context:
    def __init__(self, correlation_id):
        self.version = "1.0.0"
        self.correlation_id = correlation_id
        self.service_name = os.getenv("SERVICE_NAME", "")
        self.platform = Platform()
        self.release = Release()
        self.session = None
        self.user = None


class Event:
    def __init__(self, action, message):
        self.action = action
        self.message = message


class Log:
    def __init__(self, correlation_id):
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            wrapper_class=structlog.BoundLogger,
        )

        self.logger = structlog.get_logger()
        ctx = Context(correlation_id)
        self.logger = self.logger.bind(context=ctx.__dict__)

    def trace(self, action, message):
        ev = Event(action, message)
        self.logger.bind(event=ev.__dict__).msg("TRACE")

    def debug(self, action, message):
        ev = Event(action, message)
        self.logger.bind(event=ev.__dict__).msg("DEBUG")

    def info(self, action, message):
        ev = Event(action, message)
        self.logger.bind(event=ev.__dict__).msg("INFO")

    def warn(self, action, message):
        ev = Event(action, message)
        self.logger.bind(event=ev.__dict__).msg("WARN")

    def error(self, action, message):
        ev = Event(action, message)
        self.logger.bind(event=ev.__dict__).msg("ERROR")
