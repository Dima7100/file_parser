import os

from parser import (get_token, get_mcko_token, get_mcko_auth, get_response, get_data, update_headers,
                    start_session, download_files, filter_new_files, is_token_expired)
from configs import logger_mcko
from dotenv import load_dotenv, set_key

load_dotenv()


def get_mcko_session():
    session = start_session()
    bearer_token = os.getenv('TOKEN')
    if is_token_expired(bearer_token):  # Если True, то получаем новый токен и заносим в env
        bearer_token = get_token()
        if bearer_token is False:
            return False
        set_key('../.env', 'TOKEN', bearer_token)
        logger_mcko.info('Новый токен получен и сохранен')

    update_headers(session, bearer_token)

    mcko_token = get_mcko_token(session)

    if mcko_token is False:
        return False

    auth_success = get_mcko_auth(session, mcko_token)
    if auth_success is False:
        return False
    return session


def get_data_to_bot(session):
    """
    Это основной модуль парсера. В нем реализованы следующие этапы:
    1. Стартуется сессия.
    2. Загружается токен. Если токена нет или истёк, то получает новый токен и сохраняет в env
    3. Обновляет заголовки с токеном
    4. Через school.mos.ru получает токен МЦКО
    5. Переходит на сайт МЦКО с токеном в ссылке и получает необходимые куки
    6. Переходит на страницу МЦКО с загрузками и парсит таблицу с файлами, описанием и т.д.
    7. Спарсенные данные обрабатываются и сравниваются с теми, что уже были сохранены.
    8. Те, что определены, как новые - скачиваются, а так же передаются боту в формате json
    :return:
    """

    response, session = get_response(session)
    if response is False:
        return False

    data = get_data(response)
    if data is False:
        return False

    new_data = filter_new_files(data)
    if new_data is False:
        return False

    download_success = download_files(session, new_data)
    if download_success is False:
        return False

    return new_data
