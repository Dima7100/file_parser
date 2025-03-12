from parser import get_data_to_bot, get_mcko_session, session_status
from database import get_users_id
from configs import logger_bot

import asyncio
from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.exceptions import TelegramRetryAfter

from datetime import datetime, time, timedelta

async def check_and_send_data(bot: Bot):
    """
    Здесь просто лютое говнокодище. Сюда впихнул назначение file_id после первой отправки файла, чтобы потом его использовать.
    Потом впихнул сохранение сессии, чтобы одной пользоваться, а не создавать новую, пока не стухнет
    И ещё слипы, чтобы не попасть под ограничение
    :param bot:
    :return:
    """
    counter = 0
    session = None
    while True:
        now = datetime.now().time()
        if session_status(session) is False:
            session = get_mcko_session()
        files_info = get_data_to_bot(session)
        print('Дошли до получения айди юзеров')
        users_id = await get_users_id('МЦКО')
        print(f'Получили айди юзеров {users_id}')
        if files_info:
            print('Файлы имеются, отсылаем')
            for user_id in users_id:
                for file in files_info:
                    text = (f"Файл <b>{file['name']}</b>\n"
                            f"Загружен в {file['time']}\n"
                            f"<b>{file['desc_bold']}</b>\n"
                            f"{file['desc_regular']}")
                    if file['file_id']:
                        document = file['file_id']
                    else:
                        document = FSInputFile(f'../data/downloads/{file["name"]}')
                    try:
                        sent_document = await bot.send_document(user_id, document=document, caption=text, parse_mode='HTML')
                    except TelegramRetryAfter as e:
                        logger_bot.warning(f'Много отправок, блок: {e}')


                    if not file['file_id']:
                        file['file_id'] = sent_document.document.file_id
                    counter+=1
                    if counter == 25:
                        await asyncio.sleep(1)
                        counter = 0
                await asyncio.sleep(10)
        if time(8, 0) <= now <= time(9, 0):
            await asyncio.sleep(60)
        elif time(9, 1) <= now <= time(19, 0):
            await asyncio.sleep(3600)
        else:
            # Спать до 8 утра следующего дня
            now_datetime = datetime.now()
            next_morning = now_datetime.replace(hour=8, minute=0, second=0, microsecond=0)
            if now_datetime >= next_morning:
                next_morning += timedelta(days=1)
            sleep_duration = (next_morning - now_datetime).total_seconds()
            logger_bot.info(f'Рассылка спит до 8 утра ещё: {sleep_duration}')
            await asyncio.sleep(sleep_duration)
