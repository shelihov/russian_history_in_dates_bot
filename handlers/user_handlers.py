from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import Message, CallbackQuery
from keyboards.keyboards import (create_inline_kb, go_start_time_boards_keyboard,
                                go_start_battles_keyboard, go_start_wars_and_riot_keyboard,
                                go_start_reforms_keyboard)

from lexicon.lexicon import LEXICON_RU

router = Router()

# Cоздаем класс StatesGroup для нашей машины состояний
class FSMStatistics(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    сhoice_direction_state = State()
    choice_answer_time_boards_state = State()
    choice_answer_battles_state = State()
    choice_answer_wars_and_riot_state = State()
    choice_answer_reforms_state = State()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(),  StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])

# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего. Вы вне теста\n\n'
             'Чтобы перейти к перейти к выполнению тестов - '
             'отправьте команду /start и выберите направление'
    )

# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из теста.\n\n'
             'Чтобы снова перейти к выполнению тестов - '
             'отправьте команду /start и выберите направление'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду /filldirection
# и переводить бота в состояние ожидания выбора темы
@router.message(Command(commands='filldirection'), StateFilter(default_state))
async def process_filldirection_command(message: Message, state: FSMContext):
    choice_direction_keyboard = create_inline_kb(1, 'time_boards', 'battles',
                                                 'wars_and_riot', 'reforms')
    await message.answer(text=LEXICON_RU['/filldirection'],
                         reply_markup=choice_direction_keyboard)
    # Устанавливаем состояние ожидания выбора темы
    await state.set_state(FSMStatistics.сhoice_direction_state)


# Этот хэндлер срабатывает на выбор направления "Время правления"
@router.callback_query(StateFilter(FSMStatistics.сhoice_direction_state),
                       F.data == 'time_boards')
async def process_time_boards_direction(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Было выбрано направление: Время правления.',
        reply_markup=go_start_time_boards_keyboard
    )
    # Устанавливаем состояние прохождения теста
    await state.set_state(FSMStatistics.choice_answer_time_boards_state)

# Этот хэндлер срабатывает на выбор направления "Битвы"
@router.callback_query(StateFilter(FSMStatistics.сhoice_direction_state),
                       F.data == 'battles')
async def process_battles_direction(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Было выбрано направление: Битвы.',
        reply_markup=go_start_battles_keyboard
    )
    # Устанавливаем состояние прохождения теста
    await state.set_state(FSMStatistics.choice_answer_battles_state)

# Этот хэндлер срабатывает на выбор направления "Войны и восстания"
@router.callback_query(StateFilter(FSMStatistics.сhoice_direction_state),
                       F.data == 'wars_and_riot')
async def process_wars_and_riot_direction(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Было выбрано направление: Войны и восстания.',
        reply_markup=go_start_wars_and_riot_keyboard
    )
    # Устанавливаем состояние прохождения теста
    await state.set_state(FSMStatistics.choice_answer_wars_and_riot_state)

# Этот хэндлер срабатывает на выбор направления "Реформы"
@router.callback_query(StateFilter(FSMStatistics.сhoice_direction_state),
                       F.data == 'reforms')
async def process_reforms_direction(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Было выбрано направление: Реформы.',
        reply_markup=go_start_reforms_keyboard
    )
    # Устанавливаем состояние прохождения теста
    await state.set_state(FSMStatistics.choice_answer_reforms_state)