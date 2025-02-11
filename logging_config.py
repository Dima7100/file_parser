import logging
from logging import Logger
from logging.handlers import RotatingFileHandler

def setup_logger():
    """
    Настройка логирования
    """

    logger = logging.getLogger('okmcko')
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = RotatingFileHandler(
        filename="mcko.log",
        maxBytes= 10 * 1024 * 1024,
        backupCount= 3,
        encoding= 'utf-8'
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()

