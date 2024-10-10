from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


choose_answer_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да"),
        ],
        [
            KeyboardButton(text="Нет"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите варинант ответа",
)

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Начать игру"),
            KeyboardButton(text="Статистика"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню",
)

delete_keyboard = ReplyKeyboardRemove()
