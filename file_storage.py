import json
import os

def is_file_exists():
    """
    Проверяем наличие файла
    """
    if os.path.exists('data.json'):
        return True
    else:
        return False

def save_data(data):
    """
    Сохраняем в json
    """
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


def load_data():
    """
    Загружаем из data.json
    """
    return json.load('data.json')


def is_file_in_old_data(file_name, old_data):
    """
    Проверяем есть ли данные о файле в загруженном data.json
    """
    for file_info in old_data:
        if file_info['name'] == file_name:
            return True
    return False


#TODO сделать проверку в main, чтобы функция вызывалась только если есть data!
def exclude_old(data):
    """Основной метод, который исключает из переданного списка словарей те,
    что уже есть и возвращает только новые"""
    new_data = list()
    # Если файла ещё нет, то значит все переданные данные новые, сразу и сохраняем
    if not is_file_exists():
        save_data(data)
        return data

    old_data = load_data()
    for file_info in data:
        if not is_file_in_old_data(file_info['name'], old_data):
            new_data.append(file_info)
    old_data.append(new_data)
    save_data(old_data)
    return new_data
