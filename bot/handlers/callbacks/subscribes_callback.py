from aiogram import Router, types
from aiogram.filters import Command
from database import update_user_status, get_user, get_user_subscribes, add_user_subscribe, delete_user_subscribe, get_subscribes
from bot.keyboards import subscribes_keyboard

router = Router()

@router.callback_query(lambda c: c.data.startswith(f'sub_'))
async def available_subscribes(callback_query: types.CallbackQuery):
    sub_name = callback_query.data[8:]
    print('колбэк подписок отловился')
    if 'not' in callback_query.data:
        print(sub_name)
        await add_user_subscribe(callback_query.from_user.id, sub_name)
        await callback_query.answer(f'Подписка {sub_name} добавлена')
    else:
        await delete_user_subscribe(callback_query.from_user.id, sub_name)
        await callback_query.answer(f'Подписка {sub_name} удалена')
    user_subscribes = await get_user_subscribes(callback_query.from_user.id)
    subscribes = await get_subscribes()
    if user_subscribes is None:
        keyboard = subscribes_keyboard(subscribes)
    else:
        keyboard = subscribes_keyboard(subscribes, user_subscribes)
    await callback_query.message.edit_text('Доступные подписки\nЕсли отмечено галочкой, то подписка оформлена:', reply_markup=keyboard.as_markup())
