import requests
import os
from requests import Session
from pathlib import Path
from logging_config import logger_downloader

CURRENT_PATH = Path.cwd()
DOWNLOADS = CURRENT_PATH / 'downloads'

def is_exists_directory():
    """
    Проверяем есть ли папка для закачки
    """
    logger_downloader.info('Проверяем наличие папки для закачек')
    if DOWNLOADS.exists():
        logger_downloader.info('Папка существует')
        return True
    else:
        logger_downloader.info('Папки нет')
        return False



def download_files(session: requests.Session, new_data: list):
    """
    Скачиваем файлы при наличии списка
    """
    if not is_exists_directory():
        Path.mkdir(DOWNLOADS)
        logger_downloader.info('Создали папку')

        logger_downloader.info('Приступаем к закачке новых файлов')

    for file_info in new_data:
        try:
            name = file_info['name']
            href = file_info['href']
            response = session.get(f'https://okmcko.mos.ru{href}')
            response.raise_for_status()

            file_path = DOWNLOADS / name
            with open(file_path, 'wb') as file:
                file.write(response.content)
                logger_downloader.info(f'Файл {name} сохранен в папку')
        except (requests.exceptions.RequestException, IOError) as e:
            logger_downloader.error(f'Сайт не ответил или файл не скачался {e}')
     logger_downloader.info('Файлы скачены!')






