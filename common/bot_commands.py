from aiogram.types import BotCommand

private_commands = {
    BotCommand(command='start', description='Перезапустить бота в чате'),
    BotCommand(command='game', description='Начать игру "Угадай число"'),
    BotCommand(command='finish', description='Закончить текущую игру'),
    BotCommand(command='stats', description='Получить статистику игрока')
}
