import os
import structlog
from dataclasses import dataclass, asdict


@dataclass
class Platform:
    aws: dict

    def __init__(self):
        self.aws = {"account": os.getenv("AWS_ACCOUNT", "")}

    def to_dict(self):
        return asdict(self)


@dataclass
class Release:
    commit_hash: str
    created_at: str
    version: str

    def __init__(self):
        self.commit_hash = os.getenv("COMMIT_HASH", "")
        self.created_at = os.getenv("COMMIT_DATE", "")
        self.version = os.getenv("VERSION", "")

    def to_dict(self):
        return asdict(self)


@dataclass
class Session:
    uid: str
    type: str

    def __init__(self, uid="", type_=""):
        self.uid = uid
        self.type = type_

    def to_dict(self):
        return asdict(self)


@dataclass
class User:
    uid: str
    type: str

    def __init__(self, uid, type_):
        self.uid = uid
        self.type = type_

    def to_dict(self):
        return asdict(self)


@dataclass
class Context:
    version: str
    correlation_id: str
    service_name: str
    platform: Platform
    release: Release
    session: Session
    user: User

    def __init__(self, correlation_id):
        self.version = "1.0.0"
        self.correlation_id = correlation_id
        self.service_name = os.getenv("SERVICE_NAME", "")
        self.platform = Platform()
        self.release = Release()
        self.session = None
        self.user = None

    def to_dict(self):
        return {
            "version": self.version,
            "correlation_id": self.correlation_id,
            "service_name": self.service_name,
            "platform": self.platform.to_dict() if self.platform else None,
            "release": self.release.to_dict() if self.release else None,
            "session": self.session.to_dict() if self.session else None,
            "user": self.user.to_dict() if self.user else None,
        }


@dataclass
class Event:
    action: str
    message: str
    data: dict

    def __init__(self, message, action="", data=None):
        self.action = action
        self.message = message
        self.data = data or {}

    def to_dict(self):
        return asdict(self)


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
        self.logger = self.logger.bind(context=ctx.to_dict())

    def log(self, level, message, action="", **kwargs):
        # Action is optional and message comes first
        ev = Event(message, action, kwargs)
        self.logger.bind(event=ev.to_dict()).msg(message)

    def trace(self, message, action="", **kwargs):
        self.log("TRACE", message, action, **kwargs)

    def debug(self, message, action="", **kwargs):
        self.log("DEBUG", message, action, **kwargs)

    def info(self, message, action="", **kwargs):
        self.log("INFO", message, action, **kwargs)

    def warn(self, message, action="", **kwargs):
        self.log("WARN", message, action, **kwargs)

    def error(self, message, action="", **kwargs):
        self.log("ERROR", message, action, **kwargs)
