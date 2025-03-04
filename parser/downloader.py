import requests
from pathlib import Path
from configs import logger_downloader

#TODO надо понять, как работает path.cwd(), если запускается бот из bot/main.py

DOWNLOADS = Path('../data/downloads')

def is_exists_directory():
    """
    Проверяем есть ли папка для закачки
    """
    if DOWNLOADS.exists():
        return True
    else:
        logger_downloader.info('Папки для закачек нет')
        return False


def download_files(session: requests.Session, new_data: list):
    """
    Скачиваем файлы при наличии списка
    """
    if not is_exists_directory():
        DOWNLOADS.parent.mkdir(parents=True, exist_ok=True)
        logger_downloader.info('Создали папку')

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
            #TODO - уведомить админа, удалить new_data из json
            return False
    logger_downloader.info('Файлы скачены!')
    return True






