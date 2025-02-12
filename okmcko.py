import os
from datetime import datetime

import jwt
import requests
import urllib3
from dotenv import load_dotenv, set_key

from logging_config import logger_mcko
from mos_token import get_token


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


def is_token_expired(token):
    """
    Декодируем токен и проверяем срок годности. Возвращаем False или True
    """
    if not token:
        logger_mcko.warning('Токен не передан в аргумент')
    try:
        decoded = jwt.decode(token, options={'verify_signature': False})
        exp_timestamp = decoded.get('exp')
        if exp_timestamp:
            exp_date = datetime.fromtimestamp(exp_timestamp)
            if exp_date > datetime.now():
                logger_mcko.info(f'Токен действителен до {exp_date}')
                return False
            else:
                logger_mcko.warning('Токен истек!')
                return True
    except jwt.InvalidTokenError:
        logger_mcko.error('Неверный токен!')
        return True


def get_mcko_token(session):
    """
    Получаем токен мцко из school.mos.ru для автоматической авторизации на сайт мцко
    """
    try:
        response_mosru = session.post('https://school.mos.ru/api/ej/acl/v1/mcko/token', json=PAYLOAD)
        response_mosru.raise_for_status()
        mcko_token = response_mosru.json()['token']
        return mcko_token
    except requests.exceptions.RequestException as e:
        logger_mcko.error(f'Ошибка при получении токена МЦКО: {e}')


def get_mcko_auth(session, mcko_token):
    """
    Входим на сайт мцко с токеном и получаем сессионные куки мцко
    """
    try:
        response_mcko_auth = session.get(f'https://okmcko.mos.ru/jump_alt.php?sess_token={mcko_token}')
        response_mcko_auth.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger_mcko.error(f'Ошибка при первой аутентификации на сайте МЦКО: {e}')



def get_response():
    """
    Входим на сайт okmcko.ru с токеном mcko и получаем страничку с таблицей файлов
    """
    session = requests.Session() # Стартуем главную сессию
    bearer_token = os.getenv('TOKEN')

    if is_token_expired(bearer_token): # Если True, то получаем новый токен и заносим в env
        bearer_token = get_token()
        set_key('.env', 'TOKEN', bearer_token)
        logger_mcko.info('Новый токен получен и сохранен')

    HEADERS['Authorization'] = f'Bearer {bearer_token}' # Добавляем токен в заголовок
    session.headers.update(HEADERS) # Обновляем заголовки

    mcko_token = get_mcko_token(session)
    logger_mcko.info('Токен МЦКО получен')
    get_mcko_auth(session, mcko_token)
    logger_mcko.info('Авторизация на МЦКО успешна')
    try:
        response_mcko = session.get('https://okmcko.mos.ru/index2020.php?c=mid&d=downld')
        logger_mcko.info('Доступ к файлам получен')
        return response_mcko, session
    except requests.exceptions.RequestException as e:
        logger_mcko.error(f'Ошибка перехода на страницу файлов сайта МЦКО: {e}')


if __name__ == '__main__':
    get_response()
