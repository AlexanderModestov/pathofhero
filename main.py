# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from aiogram import types
import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import FSInputFile, Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from fsm.statusgroup import ProfileStatesGroup
from aiogram.filters.state import StatesGroup, State
from io import BytesIO
import config
from PostgreSQL import PostgreSQL
import scenario
import pandas as pd
from handlers import setup_router

TOKEN = config.TOKEN

bot = Bot(TOKEN)
dp = Dispatcher()

# Подключаемся к БД
db_worker = PostgreSQL(config.database, config.user, config.password, config.host, config.port)
archetypes = scenario.archetypes
archetype_descriptions = scenario.archetype_descriptions
first_step = scenario.first_step
question_list = scenario.question_list
strategies_description = scenario.strategies_description

async def main():
    handler_router = setup_router()
    dp.include_router(handler_router)
    #dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())