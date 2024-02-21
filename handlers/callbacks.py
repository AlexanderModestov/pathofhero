from aiogram import Router, types, Bot, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from PostgreSQL import PostgreSQL
from utils.menu import gen_markup_chips, gen_markup
from strategy import get_strategy, get_archetype
from fsm.statusgroup import ProfileStatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
import config
import scenario
import pandas as pd
from utils.reg import extract_number, extract_text

db_worker = PostgreSQL(config.database, config.user, config.password, config.host, config.port)
archetypes = scenario.archetypes
archetype_descriptions = scenario.archetype_descriptions
first_step = scenario.first_step
answers_1 = scenario.answers_1
answers_2 = scenario.answers_2
answers_3 = scenario.answers_3
pictures = scenario.pictures
symbols = scenario.symbols
question_list = scenario.question_list
strategies_description = scenario.strategies_description
instructions_1 = scenario.instructions_1
instructions_2 = scenario.instructions_2
instructions_3 = scenario.instructions_3
instructions_4 = scenario.instructions_4
instructions_5 = scenario.instructions_5
path_more_18 = scenario.path_more_18
path_less_18 = scenario.path_less_18

TOKEN = config.TOKEN
bot = Bot(TOKEN)

router = Router()

def get_results(db_worker):
    ###########################################################################
    return db_worker.select_all()

@router.message(ProfileStatesGroup.age)
async def callback_profile(message: types.Message, state: FSMContext) -> None:
    await state.update_data(age=message.text)
    db_worker.insert_user([message.chat.id, extract_number(message.text), str(extract_text(message.text))])
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.button(text="Начать тест", callback_data="start_test")
    markup = InlineKeyboardMarkup(inline_keyboard=builder.export())
    #await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id-1, 
    #                            text="Сейчас будет блок вопросов, чтобы подсветить твою выигрышную персональную стратегию и уникальное сочетание талантов.", reply_markup=markup)
    await bot.send_message(chat_id=message.chat.id, 
                                text="Сейчас будет блок вопросов, чтобы подсветить твою выигрышную персональную стратегию и уникальное сочетание талантов.", reply_markup=markup)
    #await message.delete()

@router.callback_query(F.data == "profile")
async def callback_profile(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text="Напиши свое имя и возраст:", parse_mode='markdown')
    await state.set_state(ProfileStatesGroup.age)
    await callback.answer()

@router.callback_query(F.data == "start_test")
async def callback_start_test(callback: types.CallbackQuery):
    poll_number = db_worker.get_poll(callback.message.chat.id) + 1
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await bot.send_message(callback.message.chat.id, instructions_1, parse_mode='markdown')
    await bot.send_message(callback.message.chat.id, question_list[0], parse_mode='markdown', reply_markup=gen_markup(answers_1, 0, poll_number))

@router.callback_query()
async def callback_profile(callback: types.CallbackQuery):
    response = int(callback.data.split('|')[0])
    number = int(callback.data.split('|')[1]) + 1
    poll_number = int(callback.data.split('|')[2])
    db_worker.insert_row([callback.message.chat.id, callback.message.from_user.id, poll_number, number, response])
    if number < 4:
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        await bot.send_message(callback.message.chat.id, instructions_1, parse_mode='markdown')
        await bot.send_message(callback.message.chat.id, question_list[number],
                             parse_mode='markdown', reply_markup=gen_markup(answers_1, number, poll_number))
    elif number < 8:
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        await bot.send_message(callback.message.chat.id, instructions_2, parse_mode='markdown')
        await bot.send_message(callback.message.chat.id, question_list[number],
                             parse_mode='markdown', reply_markup=gen_markup(answers_2, number, poll_number))
    elif number < 12:
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        await bot.send_message(callback.message.chat.id, instructions_3, parse_mode='markdown')
        await bot.send_message(callback.message.chat.id, question_list[number],
                             parse_mode='markdown', reply_markup=gen_markup(answers_3, number, poll_number))
    elif number < 16:
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        await bot.send_message(callback.message.chat.id, instructions_4, parse_mode='markdown')
        if number == 12:
            await bot.send_photo(callback.message.chat.id, FSInputFile('pictures/1.jpg'))
        elif number == 13:
            await bot.delete_message(callback.message.chat.id, callback.message.message_id - 2)
            await bot.send_photo(callback.message.chat.id, FSInputFile('pictures/2.jpg'))
        elif number == 14:
            await bot.delete_message(callback.message.chat.id, callback.message.message_id - 2)
            await bot.send_photo(callback.message.chat.id, FSInputFile('pictures/3.jpg'))
        else:
            await bot.delete_message(callback.message.chat.id, callback.message.message_id - 2)
            await bot.send_photo(callback.message.chat.id, FSInputFile('pictures/4.jpg'))
        await bot.send_message(callback.message.chat.id, text='*Варианты оценок:*', parse_mode='markdown', reply_markup=gen_markup(pictures, number, poll_number))
    elif number == 16:
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)  # Добавил
        await bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)  # Добавил
        await bot.delete_message(callback.message.chat.id, callback.message.message_id - 2) 
        await bot.send_message(callback.message.chat.id, text=instructions_5, parse_mode='markdown')
        await bot.send_photo(callback.message.chat.id, FSInputFile('strategies/icons_new.jpg'))
        await bot.send_message(callback.message.chat.id, '*Список символов:*',
                             parse_mode='markdown',
                             reply_markup=gen_markup_chips(symbols, number, 4, poll_number))
    else:
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        await bot.delete_message(callback.message.chat.id, callback.message.message_id - 2)
        strategy = get_strategy(get_results(db_worker), callback.message.chat.id, poll_number)[0]
        strategies = get_strategy(get_results(db_worker), callback.message.chat.id, poll_number)[1]
        await bot.send_message(callback.message.chat.id, '''*Лови свой результат! Это твоя ведущая стратегия – делай на нее ставку и не забывай прокачивать слабые стороны.*''',  parse_mode='markdown')
        await bot.send_message(callback.message.chat.id, strategy, parse_mode='markdown')
        if db_worker.more_18(callback.message.chat.id):
            await bot.send_message(callback.message.chat.id, path_more_18, parse_mode='markdown')
        else:
            await bot.send_message(callback.message.chat.id, path_less_18, parse_mode='HTML')