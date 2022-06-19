from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    main_menu_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='⚡️Играть',           callback_data='lang_page')
            ],
            [
                InlineKeyboardButton(text='🎓Моя статистика',   callback_data='stat_page')
            ],
            [
                InlineKeyboardButton(text='☄️ТОП 5 участников', callback_data='top_page')
            ],
            [
                InlineKeyboardButton(text='📙Об игре',          callback_data='about_page')
            ]
        ]
    )
    return main_menu_kb


def lang_menu():
    language_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🇺🇸 English',         callback_data='play_eng'),
                InlineKeyboardButton(text='🇫🇮 Suomi',           callback_data='play_fin')
            ],
            [
                InlineKeyboardButton(text='◀️Назад',            callback_data='main_page'),
            ]
        ]
    )
    return language_kb


def stat_menu():
    stat_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='◀️Назад',            callback_data='main_page'),
            ]
        ]
    )
    return stat_kb


def category_menu(call, opened):

    lang = call.data[5:]
    categories = {'Животные 🦄': 'cat_animals', 'Еда 🌭': 'cat_food',
                  'Город 🏙': 'cat_city', 'Музыка 🎼': 'cat_music'}

    is_locked = ['' if i < opened else '🔒' for i in range(len(categories))]
    # Creating buttons list from categories

    buttons = [InlineKeyboardButton(text=str(is_locked[i]+list(categories.keys())[i]),
                                    callback_data='locked' if is_locked[i] == '🔒'
                                    else list(categories.values())[i]+lang)
               for i in range(len(categories))]
    buttons = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    buttons.append([InlineKeyboardButton(text='◀️Назад', callback_data='main_page')])
    cat_kb = InlineKeyboardMarkup(inline_keyboard=buttons)

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
