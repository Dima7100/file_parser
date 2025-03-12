from aiogram import F
from aiogram import Router, types
from aiogram.filters import Command
from configs.config import ADMIN_ID
from database import get_users


router = Router()

@router.message(F.text, Command("users"))
async def cmd_users(message: types.Message):
    if message.from_user.id == int(ADMIN_ID):
        users = await get_users()
        text = ''
        if users:
            for user in users:
                user_info = (f'id: {user[0]}\n'
                             f'first_name: {user[1]}\n'
                             f'last_name: {user[2]}\n'
                             f'username: {user[3]}\n'
                             f'status: {user[4]}\n\n')
                text += user_info
            await message.answer(text)