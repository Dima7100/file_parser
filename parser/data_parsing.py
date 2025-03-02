from bs4 import BeautifulSoup

from configs import logger_processing


def get_data(response):
    """
    Получаем код страницы и парсим время загрузки файла, имя, ссылку и описание из болда и регулар частей
    """
    soup = BeautifulSoup(response.content, 'lxml', from_encoding="windows-1251")

    table = soup.select_one('table[class=tbl]')
    try:
        rows = table.find_all('tr')
    except AttributeError:
        logger_processing.error('Таблица в get_data не найдена!')
        return False
    logger_processing.info('Находим таблицу с файлами')
    data = list()
    # Исключаем заголовок таблицы
    for row in rows[1:]:
        cells = row.find_all('td')
        file_inf = dict()
        file_inf['time'] = cells[1].select_one('font[class=smalldesc7]').text[-5:]
        file_inf['name'] = cells[2].text.strip()
        file_inf['href'] = cells[2].find('a').get('href')

        # Болда может не быть
        try:
            file_inf['desc_bold'] = cells[3].find('b').text.strip()
        except AttributeError:
            file_inf['desc_bold'] = ''
        # Если нет болда, то нет и br и там просто текст
        try:
            file_inf['desc_regular'] = cells[3].find('br').next_sibling.strip()
        except AttributeError:
            file_inf['desc_regular'] = cells[3].text.strip()
        data.append(file_inf)
    logger_processing.info('Данные спарсены и сохранены словарем в переменной data')
    return data



if __name__ == '__main__':
    with open('../okmcko.html', 'r', encoding='windows-1251') as file:
        html_content = file.read()
    print(get_data(html_content))