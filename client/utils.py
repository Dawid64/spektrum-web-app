import logging


class CustomFormatter(logging.Formatter):
    cyan = "\x1b[96m"
    grey = "\x1b[30;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    text_format = "%(asctime)s - %(name)s [%(levelname)s]: %(message)s"

    FORMATS = {
        logging.DEBUG: cyan + text_format + reset,
        logging.INFO: grey + text_format + reset,
        logging.WARNING: yellow + text_format + reset,
        logging.ERROR: red + text_format + reset,
        logging.CRITICAL: bold_red + text_format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setFormatter(CustomFormatter())
        logger.addHandler(ch)
    logger.propagate = False
    return logger
