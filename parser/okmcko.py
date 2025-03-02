from datetime import datetime

import jwt
import requests
import urllib3
from dotenv import load_dotenv

from configs import logger_mcko

# Заголовки
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://school.mos.ru/educationmanagement/routing',
    'x-mes-subsystem': 'hteacherweb',
    'Profile-id': '35969011',
    'Content-type': 'application/json'
}

PAYLOAD = {'type': 'deputy'} # Payload для получения токена от mcko

# Отключение шума в логах и загрузка из окружения токена
urllib3.disable_warnings()
load_dotenv()


def is_token_expired(token: str):
    """
    Декодируем bearer токен и проверяем срок годности. Возвращаем False или True.
    Буквально: Токен истёк? True or False
    """
    if not token:
        logger_mcko.warning('Токен не передан в аргумент is_token_expired')
        return True
    try:
        decoded = jwt.decode(token, options={'verify_signature': False})
        exp_timestamp = decoded.get('exp')
        if exp_timestamp:
            exp_date = datetime.fromtimestamp(exp_timestamp)
            if exp_date > datetime.now():
                logger_mcko.info(f'Bearer token действителен до {exp_date}')
                return False
            else:
                logger_mcko.warning('Токен истек!')
                return True
    except jwt.InvalidTokenError:
        logger_mcko.error('Неверный токен!')
        return True


def get_mcko_token(session: requests.Session):
    """
    Получаем токен мцко из school.mos.ru для автоматической авторизации на сайт мцко
    """
    try:
        response_mosru = session.post('https://school.mos.ru/api/ej/acl/v1/mcko/token', json=PAYLOAD)
        response_mosru.raise_for_status()
        mcko_token = response_mosru.json()['token']
        logger_mcko.info('Токен МЦКО получен')
        return mcko_token
    except requests.exceptions.RequestException as e:
        logger_mcko.error(f'Ошибка при получении токена МЦКО в get_mcko_token: {e}')
        return False


def get_mcko_auth(session: requests.Session, mcko_token: str):
    """
    Входим на сайт мцко с токеном и получаем сессионные куки мцко
    """
    try:
        response_mcko_auth = session.get(f'https://okmcko.mos.ru/jump_alt.php?sess_token={mcko_token}')
        response_mcko_auth.raise_for_status()
        logger_mcko.info('Авторизация на МЦКО успешна')
        return True
    except requests.exceptions.RequestException as e:
        logger_mcko.error(f'Ошибка при аутентификации на сайте МЦКО: {e}')
        return False


def start_session():
    """
    Стартуем главную сессию
    :return: session
    """
    session = requests.Session()
    return session

def update_headers(session: requests.Session, bearer_token: str):
    """
    После получения нового bearer token или загрузки старого, необходимо добавить его в заголовок
    :param session: главная сессия
    :param bearer_token: токен из env или напрямую с сайта
    :return:
    """
    HEADERS['Authorization'] = f'Bearer {bearer_token}'
    session.headers.update(HEADERS)



def get_response(session):
    """
    Входим на сайт okmcko.ru с токеном mcko и получаем страничку с таблицей файлов
    """
    try:
        response_mcko = session.get('https://okmcko.mos.ru/index2020.php?c=mid&d=downld')
        logger_mcko.info('Доступ к странице с файламами получен')
        return response_mcko, session
    except requests.exceptions.RequestException as e:
        logger_mcko.error(f'Ошибка перехода на страницу файлов сайта МЦКО: {e}')
        return False, False


if __name__ == '__main__':
    get_response()
