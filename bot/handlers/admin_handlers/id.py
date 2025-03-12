from aiogram import F
from aiogram import Router, types
from aiogram.filters import CommandObject, Command
from configs.config import ADMIN_ID
from database import get_user
from bot.keyboards import id_keyboard

router = Router()

@router.message(Command('id'))
async def cmd_id(message: types.Message,
                 command: CommandObject):
    if command.args is None:
        await message.answer('Не передан id')
        return
    try:
        user_id = int(command.args)
        user = await get_user(user_id)
        status = user[5]
        print(status)
        keyboard = id_keyboard(user_id, status)
        text = f'Действия с пользователем {user_id}'
        await message.answer(text = text, reply_markup=keyboard.as_markup())

    except ValueError:
        await message.answer('Что то не так с аргументом. Должно быть /id <номер id>')
        return
    #TODO берем из бд данные по id и пишем сообщение с инлайн клавой и двумя колбэками (клава зависит от статуса юзера)