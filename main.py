# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from aiogram import types
import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import FSInputFile, Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from strategy import get_strategy, get_archetype
from fsm.statusgroup import ProfileStatesGroup
from aiogram.filters.state import StatesGroup, State
from utils.menu import gen_markup_chips, gen_markup
from io import BytesIO
import config
from PostgreSQL import PostgreSQL
import scenario
import pandas as pd

TOKEN = config.TOKEN

user_info = {}

storage = MemoryStorage()
bot = Bot(TOKEN)
router = Router()

# Подключаемся к БД
db_worker = PostgreSQL(config.database, config.user, config.password, config.host, config.port)
archetypes = scenario.archetypes
archetype_descriptions = scenario.archetype_descriptions
first_step = scenario.first_step
question_list = scenario.question_list
estimations_1 = scenario.estimations_1
estimations_strategies = scenario.estimations_strategies
strategies_description = scenario.strategies_description
contacts_step_1 = scenario.contacts_step_1
instructions = scenario.instructions

def get_results(db_worker):
    return db_worker.select_all()


@router.message(ProfileStatesGroup.info)
async def callback_profile(message: types.Message, state: FSMContext) -> None:
    await state.update_data(info=message.text)
    await state.set_state(ProfileStatesGroup.interests)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id-1, 
                                text="Что тебе сейчас интересно, помимо профессиональной деятельности, хобби, увлечения:")
    await message.delete()

@router.message(ProfileStatesGroup.interests)
async def load_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(interests=message.text)
    await state.set_state(ProfileStatesGroup.occupation)   
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id-2, 
                                text="Чем ты профессионально занимаешься? Сколько лет? Есть ли специфика именно в твоем подходе? В чем твоя профессиональная фишка, уникальность? Расскажи, пожалуйста, коротко, но емко.")
    await message.delete()

@router.message(ProfileStatesGroup.occupation)
async def load_age(message: types.Message, state: FSMContext) -> None:
    await state.update_data(occupation=message.text)
    await state.set_state(ProfileStatesGroup.achievments)    
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id-3, text="Чем особенно гордишься, какие есть интересные факты о себе, достижения в работе?")
    await message.delete()

@router.message(ProfileStatesGroup.achievments)
async def load_age(message: types.Message, state: FSMContext) -> None:
    await state.update_data(achievments=message.text)
    await state.set_state(ProfileStatesGroup.links)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id-4, text="Ссылки на личный сайт, соцсети:")
    await message.delete()

@router.message(ProfileStatesGroup.links)
async def load_age(message: types.Message, state: FSMContext) -> None:
    await state.update_data(links=message.text)
    user_info[message.chat.id] = await state.get_data()
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.button(text="Начать тест", callback_data="start_test")
    markup = InlineKeyboardMarkup(inline_keyboard=builder.export())
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id-5, 
                                text="Сейчас будет блок вопросов, чтобы подсветить твою выигрышную профессиональную стратегию и уникальное сочетание талантов.", reply_markup=markup)
    await message.delete()

@router.callback_query()
async def callback_profile(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'profile':
        await callback.message.delete()
        await callback.message.answer(text="Твое имя, возраст, локация?", parse_mode='markdown')
        await state.set_state(ProfileStatesGroup.info)
        await callback.answer()
    elif callback.data == 'start_test':
        poll_number = db_worker.get_poll(callback.message.chat.id) + 1
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await bot.send_message(callback.message.chat.id, instructions, parse_mode='markdown')
        await bot.send_message(callback.message.chat.id, '*Номер вопроса {}/24*'.format(1), parse_mode='markdown')
        await bot.send_message(callback.message.chat.id, question_list[0], parse_mode='markdown', reply_markup=gen_markup(estimations_1, 0, poll_number))
    else:
        response = int(callback.data.split('|')[0])
        number = int(callback.data.split('|')[1]) + 1
        poll_number = int(callback.data.split('|')[2])
        db_worker.insert_row([callback.message.chat.id, callback.message.from_user.id, poll_number, number, response])
        if number < 24:
            await bot.delete_message(callback.message.chat.id, callback.message.message_id)
            await bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
            await bot.delete_message(callback.message.chat.id, callback.message.message_id - 2)
            await bot.send_message(callback.message.chat.id, instructions, parse_mode='markdown')
            await bot.send_message(callback.message.chat.id, '*Номер вопроса {}/24*'.format(int(number + 1)),
                             parse_mode='markdown')
            await bot.send_message(callback.message.chat.id, question_list[number],
                             parse_mode='markdown', reply_markup=gen_markup(estimations_1, number, poll_number))
        elif number == 24:
            await bot.delete_message(callback.message.chat.id, callback.message.message_id)  # Добавил
            await bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)  # Добавил
            await bot.delete_message(callback.message.chat.id, callback.message.message_id - 2)
            await bot.send_message(callback.message.chat.id,
                             '*Пожалуйста, выбирите один из 12 символ, который вам больше всего понравится. Отвечайте быстро, без глубокого аналтиза: на что произошла самая яркая реакция?*', parse_mode='markdown')
            await bot.send_photo(callback.message.chat.id, FSInputFile('strategies/icons.jpg'))
            await bot.send_message(callback.message.chat.id, '*Список символов:*',
                             parse_mode='markdown',
                             reply_markup=gen_markup_chips(estimations_strategies, number, 4, poll_number))
        else:
            await bot.delete_message(callback.message.chat.id, callback.message.message_id)
            await bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
            await bot.delete_message(callback.message.chat.id, callback.message.message_id - 2)
            strategy = get_strategy(get_results(db_worker), callback.message.chat.id, poll_number)[0]
            strategies = get_strategy(get_results(db_worker), callback.message.chat.id, poll_number)[1]
            info = user_info[callback.message.chat.id]
            print('user info: ', info)
            archetypes_df = pd.DataFrame(data={'archetypes': archetypes, 'values': strategies})
            archetypes_list = archetypes_df.sort_values(by='values', ascending=False)[:3]['archetypes']
            archetypes_list = archetypes_list.values.tolist()
            await bot.send_message(callback.message.chat.id, '''*Спасибо за ответы!*\n\nПолучился профиль, описывающий твою профессиональную и личную уникальность.\n\nИспользуй его для самопрезентации и создания позиционирования.''',  parse_mode='markdown')
            await bot.send_message(callback.message.chat.id, info['info'] + '\n' +
                                   '*Интересы: *' + info['interests'] + '\n' +
                                   '*Чем занимаешься: *' + info['occupation'] + '\n' +
                                   '*Соцсеть:* ' + info['links'] + '\n' + strategy + '\n' +
                                   '*Описание твоих основных талантов:*' + '\n\n' +
                                   archetype_descriptions[archetypes_list[0]] + '\n\n' +
                                   archetype_descriptions[archetypes_list[1]] + '\n\n' + archetype_descriptions[archetypes_list[2]]
                                   , parse_mode='markdown')
            #markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            #markup.add(KeyboardButton('Cамопрезентация'), KeyboardButton('Сопроводительное письмо'), KeyboardButton('Посты в соцсети')).\
            #    add(KeyboardButton('Аватар'), KeyboardButton('Все это нужно'))
            #await bot.send_message(callback.message.chat.id,
            #                       '''Этот профиль – основа для дальнейшей работы над личным позиционированием и коммуникацией.\n\nЧто тебе актульно сейчас?\n\nБлагодарим! Оставь свои контакты и мы вернемся с инструментом для твоей задачи: телеграм ник''', parse_mode='markdown', reply_markup=markup)

def use_button():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Крутой отчет, готов к монетизации')
    itembtn2 = types.KeyboardButton('Не согласен с результатом, не интересно')
    itembtn3 = types.KeyboardButton('Не все понимаю в отчете, нужна консультация')
    itembtn4 = types.KeyboardButton('Итересно! хочу полный отчет обо мне')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    return markup

async def main():
    #logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())