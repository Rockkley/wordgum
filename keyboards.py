from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    main_menu_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='⚡️Играть', callback_data='lang_page')
            ],
            [
                InlineKeyboardButton(text='🎓Моя статистика', callback_data='stat_page')
            ],
            [
                InlineKeyboardButton(text='☄️ТОП 5 участников', callback_data='top_page')
            ],
            [
                InlineKeyboardButton(text='📙Об игре', callback_data='about_page')
            ]
        ]
    )
    return main_menu_kb


def lang_menu():
    language_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🇺🇸 English', callback_data='play_eng'),
                InlineKeyboardButton(text='🇫🇮 Suomi', callback_data='play_fin')
            ],
            [
                InlineKeyboardButton(text='◀️Назад', callback_data='main_page'),
            ]
        ]
    )
    return language_kb


def stat_menu():
    stat_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='◀️Назад', callback_data='main_page'),
            ]
        ]
    )
    return stat_kb


def category_menu(lang):

    cat_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'Животные 🦄', callback_data='cat_animals'+lang),
                InlineKeyboardButton(text=f'Еда 🌭', callback_data='cat_food'+lang),
            ],
            [
                InlineKeyboardButton(text=f'Город 🏙', callback_data='in_development'),
                InlineKeyboardButton(text=f'Музыка 🎼', callback_data='in_development'),
            ],
            [
                InlineKeyboardButton(text='◀️Назад', callback_data='lang_page'),
            ]
        ]
    )
    return cat_kb


def about_page():
    about_page_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [

                InlineKeyboardButton(text='💶 Поддержать проект',
                                     url='https://www.tinkoff.ru/rm/samarin.evgeniy34/QKONl27816')
            ],
            [
                InlineKeyboardButton(text='◀️Назад', callback_data='main_page')
            ]
        ]
    )
    return about_page_kb
