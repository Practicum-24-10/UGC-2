import logging

from starlette_context import context


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        if context.exists() and "X-Request-ID" in context.data:
            record.request_id = context.data["X-Request-ID"]
        else:
            record.request_id = "none"
        return True


LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DEFAULT_HANDLERS = [
    "console",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": LOG_FORMAT},
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": "%(levelprefix)s %(client_addr)s - "
                   "'%(request_line)s' %(status_code)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {
            "handlers": LOG_DEFAULT_HANDLERS,
            "level": "INFO",
        },
        "uvicorn.error": {
            "level": "INFO",
        },
        "uvicorn.access": {
            "handlers": ["access"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "level": "INFO",
        "formatter": "verbose",
        "handlers": LOG_DEFAULT_HANDLERS,
    },
}
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "filters": {
#         "custom_filter": {
#             "()": RequestIdFilter,
#         }
#     },
#     "formatters": {
#         "access": {
#             "()": "uvicorn.logging.AccessFormatter",
#             "fmt": '%(levelprefix)s %(asctime)s :: %(client_addr)s - "%(request_line)s" %(status_code)s',
#         },
#     },
#     "handlers": {
#         "logstash": {
#             "level": "INFO",
#             "class": "logstash.LogstashHandler",
#             "filters": ["custom_filter"],
#             "host": "logstash",
#             "port": 5044,
#             "version": 1,
#             "message_type": "logstash",
#             "fqdn": False,
#             "tags": ["ugc"],
#         },
#     },
#     "loggers": {
#         "uvicorn.error": {
#             "propagate": True,
#         },
#         "uvicorn.access": {"propagate": True},
#     },
#     "root": {"level": "INFO", "handlers": ["logstash"]},
# }
