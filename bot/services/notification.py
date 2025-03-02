from parser.coordinator import get_data_to_bot
from database import get_users_id

import asyncio
from aiogram import Bot
from aiogram.types import FSInputFile

async def check_and_send_data(bot: Bot):
    while True:
        files_info = get_data_to_bot()
        users_id = await get_users_id()
        if files_info:
            for user_id in users_id:
                for file in files_info:
                    text = (f"Файл <b>{file['name']}</b>\n"
                            f"Загружен в {file['time']}\n"
                            f"<b>{file['desc_bold']}</b>\n"
                            f"{file['desc_regular']}")
                    downloaded_file = FSInputFile(f'downloads/{file["name"]}')
                    await bot.send_document(user_id, downloaded_file, caption=text, parse_mode='HTML')

        await asyncio.sleep(100)
