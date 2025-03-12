import asyncio

import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from bot.handlers import router as handlers_router
from database import init_db, add_user, add_subscribe
from bot.services import check_and_send_data
from configs.config import ADMIN_ID
from bot.services import set_commands

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
admin_id = os.getenv('ADMIN_ID')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(handlers_router)


async def main():
    await init_db()
    await set_commands(bot)
    await add_user(ADMIN_ID, 'Админ', 'Админов', 'Admin', 'approved')
    await add_subscribe('МЦКО')

    await asyncio.gather(dp.start_polling(bot), check_and_send_data(bot))



if __name__ == '__main__':
    asyncio.run(main())
