import sys
from loguru import logger


def set_logger(level: str = "DEBUG"):
    logger.remove()
    logger.add(
        sys.stdout,
        level=level,
        format="<blue>{time:DD-MM-YYYY HH:mm:ss}</blue> - [<level>{level}</level>] - <level>{message}</level>",
        colorize=True,
    )
    return logger
