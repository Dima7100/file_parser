from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import get_user

def id_keyboard(user_id, status):
    builder = InlineKeyboardBuilder()
    if status == 'approved':
        builder.button(text='Закрыть доступ', callback_data=f'id_reject_{user_id}')
        builder.button(text='Удалить из БД', callback_data=f'id_delete_{user_id}')
    elif status == 'rejected':
        builder.button(text='Открыть доступ', callback_data=f'id_approve_{user_id}')
        builder.button(text='Удалить из БД', callback_data=f'id_delete_{user_id}')
    else:
        builder.button(text='Закрыть доступ', callback_data=f'id_reject_{user_id}')
        builder.button(text='Открыть доступ', callback_data=f'id_approve_{user_id}')
        builder.button(text='Удалить из БД', callback_data=f'id_delete_{user_id}')
    return builder