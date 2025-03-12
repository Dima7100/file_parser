import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from configs.config import ADMIN_ID

user_commands = [
    BotCommand(command='/start', description='Запустить бота'),
    BotCommand(command='/subscription', description='Оформить подписку на рассылку или отказаться от неё')
]

admin_commands = [
    BotCommand(command='/start', description='Запустить бота'),
    BotCommand(command='/subscription', description='Оформить подписку на рассылку или отказаться от неё'),
    BotCommand(command='/id', description='/id 123456 - действия с ботом'),
    BotCommand(command='/users', description='Список юзеров в БД'),
]

async def set_commands(bot: Bot):
    await bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())
    await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=ADMIN_ID))