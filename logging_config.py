import logging
from logging import Logger
from logging.handlers import RotatingFileHandler

def setup_logger(name):
    """
    Настройка логирования
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

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

logger_mcko = setup_logger('mcko')
logger_mos = setup_logger('mos')
logger_storage = setup_logger('file_storage')
logger_processing = setup_logger('file_process')
logger_downloader = setup_logger('downloader')
