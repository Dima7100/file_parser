import json
import os

from logging_config import logger_storage


def is_file_exists():
    """
    Проверяем наличие файла с метаданными о файлах
    """
    if os.path.exists('data.json'):
        return True
    else:
        logger_storage.warning('data.json не существует')
        return False

def save_data(data):
    """
    Сохраняем в json
    """
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=5)
        logger_storage.info('Новые данные сохранены в data.json')


def load_data():
    """
    Загружаем из data.json
    """
    with open('data.json', 'r', encoding='utf-8') as file:
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


#TODO сделать проверку в main, чтобы функция вызывалась только если есть data!
def filter_new_files(data):
    """
    Основной метод, который исключает из переданного списка словарей те,
    что уже есть и возвращает только новые
    """
    new_data = list()
    # Если файла ещё нет, то значит все переданные данные новые, сразу и сохраняем
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
    return new_data
