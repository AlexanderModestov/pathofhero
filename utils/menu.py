from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import utils

def gen_markup_chips(list_of_items, i, count_in_row, poll_serial):
    builder = InlineKeyboardBuilder()
    for item in range(12):
        builder.button(text=list_of_items[item], callback_data=str(item) + "|" + str(i) + "|" + str(poll_serial))
    builder.adjust(3,3,3,3)
    markup = InlineKeyboardMarkup(inline_keyboard=builder.export())
    return markup

def gen_markup(list_of_items, i, poll_serial):
    builder = InlineKeyboardBuilder()
    builder.button(text="Полностью НЕ согласен", callback_data=str(0) + "|" + str(i) + "|" + str(poll_serial))
    builder.button(text="Не согласен", callback_data=str(1) + "|" + str(i) + "|" + str(poll_serial))
    builder.button(text="Затрудняюсь ответить (ни то, ни другое)", callback_data=str(2) + "|" + str(i) + "|" + str(poll_serial))
    builder.button(text="Согласен", callback_data=str(3) + "|" + str(i) + "|" + str(poll_serial))
    builder.button(text="Полностью согласен", callback_data=str(4) + "|" + str(i) + "|" + str(poll_serial))
    builder.adjust(2,1,2)
    markup = InlineKeyboardMarkup(inline_keyboard=builder.export())
    return markup