from aiogram import F
from aiogram import Router, types
from aiogram.filters import Command

from bot.handlers.callbacks.subscribes_callback import available_subscribes
from configs.config import ADMIN_ID
from database import get_user, get_subscribes, get_user_subscribes, check_user_status
from bot.keyboards import subscribes_keyboard

router = Router()

#TODO Добавить эмодзи галочки для оформленной подписки и что при нажатии на оформленную - отменяется подписка. И наоборот
@router.message(F.text, Command('subscribes'))
async def cmd_subscribes(message: types.Message):
    user_id = message.from_user.id
    check_exist = await get_user(user_id)
    if check_exist:
        status = await check_user_status(user_id)
        if status == 'approved':
            user_subscribes = await get_user_subscribes(user_id)
            subscribes = await get_subscribes()
            if user_subscribes is None:
                keyboard = subscribes_keyboard(subscribes)
            else:
                keyboard = subscribes_keyboard(subscribes, user_subscribes)
            await message.answer('Доступные подписки\nЕсли отмечено галочкой, то подписка оформлена:', reply_markup=keyboard.as_markup())
        else:
            await message.answer('Нет доступа')


