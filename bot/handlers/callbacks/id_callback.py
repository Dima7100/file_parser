from aiogram import Router, types
from aiogram.filters import Command
from database import update_user_status, get_user, delete_user

router = Router()


@router.callback_query(lambda c: c.data.startswith('id'))
async def id_callback(callback: types.CallbackQuery):
    user_id = int(callback.data.split('_')[2])
    status = callback.data.split('_')[1]
    print(f'callback status: {status}')
    if status == 'reject':
        await update_user_status(user_id, 'rejected')
        await callback.answer('Юзеру закрыт доступ')
        await callback.bot.send_message(user_id, text='Вам закрыли доступ к боту')

    elif status == 'approve':
        await update_user_status(user_id, 'approved')
        await callback.answer('Юзеру открыт доступ')
        await callback.bot.send_message(user_id, text='Вам открыли доступ к боту')

    elif status == 'delete':
        await delete_user(user_id)
        await callback.answer('Юзеру удалён')
        await callback.bot.send_message(user_id, text='Вас удалили из базы данных бота')