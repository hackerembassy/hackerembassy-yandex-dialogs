import asyncio
import logging
import os
import time

from aioalice import Dispatcher, get_new_configured_app
from loguru import logger

from hackem_yandex_dialogs.core.config_manager import ConfigManager

config = ConfigManager("config.toml")

features = list(
    filter(lambda feature: feature[1], config.get_section("features").items())
)
logger.info(
    f"Using features: {', '.join([x.split('_', maxsplit=1)[1] for x, _ in features if x.startswith('use')])}"
)

is_prod = os.environ.get("ENV") == "production" or config.get_item(
    "app", "prod"
)
PROJECT_NAME = __name__
_startup_time = time.time()
if is_prod:
    logger.warning("Running in production!")

try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

dp = Dispatcher(loop)
app = get_new_configured_app(dp, config.get_item("app", "webhook_url"))


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # type: ignore
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


if config.get_item("features", "use_file_logs"):
    logger.add(
        "static/logs/debug.log",
        rotation="10MB",
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True,
        level="DEBUG",
    )
    logger.add(
        "static/logs/base.log",
        rotation="10MB",
        compression="zip",
        enqueue=True,
        level="INFO",
    )
    logger.add(
        "static/logs/error.log",
        rotation="10MB",
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True,
        level="ERROR",
    )

logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
