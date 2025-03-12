from aiogram import F
from aiogram import Router, types
from aiogram.filters import Command
from configs.config import ADMIN_ID
from database import add_user, get_user
from bot.keyboards.approve_keyboard import approve_keyboard

router = Router()

@router.message(F.text, Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    user_exist = await get_user(user_id)
    if not user_exist:
        await add_user(user_id, first_name, last_name, username)
        admin_message = (
            f"Новый пользователь хочет получить доступ:\n"
            f"ID: {user_id}\n"
            f"Имя: {first_name}\n"
            f"Фамилия: {last_name}\n"
            f"Никнейм: @{username}"
        )
        keyboard = approve_keyboard(user_id)

        await message.bot.send_message(ADMIN_ID, admin_message, reply_markup=keyboard.as_markup())
        await message.answer("Ваш запрос на доступ отправлен администратору.")
    else:
        status = ''
        if user_exist[5] == 'pending':
            status = 'на рассмотрении'
        elif user_exist[5] == 'approved':
            status = 'одобрен'
        elif user_exist[5] == 'rejected':
            status = 'отклонен'
        await message.answer(f"Вы уже отправили запрос. Статус запроса: {status}")



