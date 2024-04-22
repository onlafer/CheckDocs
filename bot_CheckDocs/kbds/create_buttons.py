from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def create_buttons_inline(*btns, **kwargs):
    """Используется для создания клавиатуры с кнопками, стоящими в одну линию (ширина и высота кнопок автоматическая).
    Так же для любой созданной клавиатуры добавляется ряд с кнопкой для перехода в меню.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t) for t in btns],
            [KeyboardButton(text="Меню")],
        ],
        resize_keyboard=True,
        **kwargs
    )


def create_menus(**kwargs):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=text, callback_data=callback_data)] for callback_data, text in kwargs.items()]
    )
