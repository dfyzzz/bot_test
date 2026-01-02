from aiogram import Bot
from aiogram.types import BotCommand


async def set_bot_commands(bot: Bot):
    """Set bot commands in the menu"""
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="profile", description="Мой профиль"),
        BotCommand(command="book", description="Записаться на прием"),
        BotCommand(command="cancel", description="Отменить запись"),
        BotCommand(command="admin", description="Админ-панель")
    ]
    
    await bot.set_my_commands(commands)