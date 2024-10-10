from random import randint

from aiogram import types, Router
from aiogram.types import Message, PollAnswer
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiohttp.web_routedef import options

from database.database import db
from keyboards import reply

user_router = Router()


class GameState(StatesGroup):
    choosing_answer = State()
    guessing_number = State()


@user_router.message(CommandStart())
async def startCommand(message: Message):
    await message.delete()
    await message.answer('Привет, это была команда для старта бота', reply_markup=reply.main_menu_keyboard)
    db.register_user(message.from_user.id, message.chat.id)
    await message.answer_poll(question="?", options=["1", "2", "3"])


@user_router.message(StateFilter(None), F.text.lower() == 'начать игру')
@user_router.message(StateFilter(None), Command('game'))
async def start_one_game(message: Message, state: FSMContext):
    await message.delete()
    await message.answer('Вы начали игру "Угадай число". Бот загадал число от 0 до 1000. Попробуйте угадать его!', reply_markup=reply.delete_keyboard)
    db.start_game(message.from_user.id, randint(0, 1000))
    await state.set_state(GameState.guessing_number)


@user_router.message(GameState.guessing_number, F.text.lower() == 'начать игру')
@user_router.message(GameState.guessing_number, Command('game'))
async def start_last_game(message: Message, state: FSMContext):
    await message.answer('У вас уже есть активная игра')
    await message.answer('Хотите продолжить предыдующую игру?', reply_markup=reply.choose_answer_keyboard)
    await state.set_state(GameState.choosing_answer)


@user_router.message(GameState.choosing_answer, F.text.lower() == 'да')
async def continue_game(message: Message, state: FSMContext):
    await message.delete()
    await message.answer('Продолжаем игру...', reply_markup=reply.delete_keyboard)
    await message.answer('Угадайте число от 0 до 1000')
    await state.set_state(GameState.guessing_number)


@user_router.message(GameState.choosing_answer, F.text.lower() == 'нет')
async def create_new_game(message: Message, state: FSMContext):
    await message.delete()
    await message.answer('Создаем новую игру...', reply_markup=reply.delete_keyboard)
    await message.answer('Угадайте число от 0 до 1000')
    db.finish_game(message.from_user.id)
    db.start_game(message.from_user.id, randint(0, 1000))
    await state.set_state(GameState.guessing_number)


@user_router.message(Command('finish'))
async def finish_game(message: Message):
    await message.delete()
    no_finished_games = db.check_game(message.from_user.id)
    if len(no_finished_games) == 0:
        await message.answer('У вас нет активных игр', reply_markup=reply.main_menu_keyboard)
    else:
        await message.answer('Активная игра завершена!')
        await message.answer(f'Загаданное число: {db.check_number(message.from_user.id)}', reply_markup=reply.main_menu_keyboard)
        db.finish_game(message.from_user.id)


@user_router.message(GameState.guessing_number, F.text.isdigit())
async def guess_number(message: Message, state: FSMContext):
    user_number = int(message.text)
    hidden_number = db.check_number(message.from_user.id)
    if hidden_number == user_number:
        await message.answer('Вы угадали!', reply_markup=reply.main_menu_keyboard)
        db.finish_game(message.from_user.id)
        db.user_win(message.from_user.id)
        await state.clear()
    elif hidden_number > user_number:
        await message.answer('Загаданное число больше')
    else:
        await message.answer('Загаданное число меньше')


@user_router.message(F.text.lower() == 'статистика')
@user_router.message(Command('stats'))
async def show_stats(message: Message):
    await message.delete()
    stats = db.get_stats(message.from_user.id)
    await message.answer(
        f'Статистика игрока {message.from_user.first_name}:\nКоличество побед: {stats[0]}\nКоличество поражений: {stats[1]}',
        reply_markup=reply.main_menu_keyboard)

@user_router.poll_answer()
async def poll_answer(pol: PollAnswer):
    options_ids = pol.option_ids

    print(options_ids)

