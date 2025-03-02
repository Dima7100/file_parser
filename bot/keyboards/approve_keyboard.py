from aiogram.utils.keyboard import InlineKeyboardBuilder

def approve_keyboard(user_id):
    builder = InlineKeyboardBuilder()
    builder.button(text="Подтвердить", callback_data=f"approve_{user_id}")
    builder.button(text="Отклонить", callback_data=f"reject_{user_id}")
    builder.adjust(2)
    return builder