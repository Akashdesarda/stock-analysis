import logging
import sys

class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    grey = "\x1b[38;21m"
    green = "\x1b[32;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_info = '[%(asctime)s] [%(levelname)s]...%(message)s'
    format_all = "[%(asctime)s] [%(levelname)s]...%(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format_all + reset,
        logging.INFO: green + format_info + reset,
        logging.WARNING: yellow + format_all + reset,
        logging.ERROR: red + format_all + reset,
        logging.CRITICAL: bold_red + format_all + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt,"%Y-%m-%d %H:%M:%S")
        return formatter.format(record)
    
def logger(level: str='debug'):
    # create logger with 'spam_application'
    logger = logging.getLogger(__name__)
    
    if level == 'debug':
        logger.setLevel(logging.DEBUG)
    if level == 'info':
        logger.setLevel(logging.INFO)
    if level == 'warning':
        logger.setLevel(logging.WARNING)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(CustomFormatter())

    logger.addHandler(ch)
    
    if level not in ['debug', 'info', 'warning']:
        logger.error('level can be from debug, info, warning');sys.exit()

    return logger