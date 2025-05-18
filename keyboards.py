from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_general_kb():
    builder = ReplyKeyboardBuilder()

    builder.button(text='/registration')
    builder.button(text='/login')

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

