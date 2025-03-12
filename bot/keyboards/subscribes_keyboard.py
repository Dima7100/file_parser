from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import text
from aiogram import types
def subscribes_keyboard(subscribes, user_subscribes = None):
    builder = InlineKeyboardBuilder()
    subscribes = list(set(subscribes) - set(user_subscribes))
    for subscribe in subscribes:
        builder.add(types.InlineKeyboardButton(text=subscribe, callback_data = f'sub_not_{subscribe}'))
    for user_subscribe in user_subscribes:
        text = f'✅ {user_subscribe}'
        builder.add(types.InlineKeyboardButton(text=text, callback_data = f'sub_yes_{user_subscribe}'))
    builder.adjust(2)
    return builder