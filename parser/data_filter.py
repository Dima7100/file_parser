import json
import os
from pathlib import Path
from configs import logger_storage


PROJECT_ROOT = Path(__file__).parent.parent
JSON_PATH = PROJECT_ROOT / 'data' / 'data.json'
JSON_PATH.mkdir(parents=True, exist_ok=True)

def is_file_exists():
    """
    Проверяем наличие файла с метаданными о файлах
    """
    if os.path.exists(JSON_PATH):
        return True
    else:
        logger_storage.warning('data.json не существует')
        return False

def save_data(_data):
    """
    Сохраняем в json
    """
    with open(JSON_PATH, 'w', encoding='utf-8') as file:
        json.dump(_data, file, ensure_ascii=False, indent=5)
        logger_storage.info('Новые данные сохранены в data.json')


def load_data():
    """
    Загружаем из data.json
    """
    with open(JSON_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def is_file_in_old_data(file_name, old_data):
    """
    Проверяем есть ли данные о файле в загруженном data.json
    """
    for file_info in old_data:
        if file_info['name'] == file_name:
            return True
    return False


def filter_new_files(data: list):
    """
    Основной метод, который исключает из переданного списка словарей те,
    что уже есть, сохраняет обновленный словарь и возвращает только новые.
    """
    new_data = list()
    # Если файла ещё нет, то значит все переданные данные новые, сразу и сохраняем и возвращаем как есть
    if not is_file_exists():
        save_data(data)
        return data

    old_data = load_data()
    logger_storage.info('Файл data.json загружен')
    # Проходимся по спарсеным данным и загруженным данным и сравниваем имя, при отсутствии, добавляем в новый список
    for file_info in data:
        if not is_file_in_old_data(file_info['name'], old_data):
            logger_storage.info(f'Найден новый файл {file_info['name']}')
            new_data.append(file_info)
    old_data.extend(new_data)
    save_data(old_data)
    if new_data:
        return new_data
    else:
        logger_storage.info('Новый данных нет')
        return False

