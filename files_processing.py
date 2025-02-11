from bs4 import BeautifulSoup
import lxml


def get_data(response):
    """
    Получаем код страницы и парсим время загрузки файла, имя, ссылку и описание из болда и регулар частей
    """
# with open('okmcko.html', 'r', encoding='windows-1251') as file:
#     html_content = file.read()

    soup = BeautifulSoup(response, 'lxml')

    table = soup.select_one('table[class=tbl]')
    rows = table.find_all('tr')

    data = dict()
    for row in rows[1:]:
        cells = row.find_all('td')

        data['time'] = cells[1].select_one('font[class=smalldesc7]').text[-5:]
        data['name'] = cells[2].text.strip()
        data['href'] = cells[2].find('a').get('href')
        # Болда может не быть
        try:
            data['desc_bold'] = cells[3].find('b').text.strip()
        except AttributeError:
            data['desc_bold'] = ''
        # Если нет болда, то нет и br и там просто текст
        try:
            data['desc_regular'] = cells[3].find('br').next_sibling.strip()
        except AttributeError:
            data['desc_regular'] = cells[3].text.strip()
    return data

if __name__ == '__main__':
    with open('okmcko.html', 'r', encoding='windows-1251') as file:
        html_content = file.read()
    print(get_data(html_content))