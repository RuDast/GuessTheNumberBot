import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, BotCommandScopeAllPrivateChats
from aiogram.filters import Command

from dotenv import find_dotenv, load_dotenv

from handlers.user_private import user_router
from common.bot_commands import private_commands

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)
dp.include_router(user_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private_commands, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=['message'])


if __name__ == '__main__':
    asyncio.run(main())
