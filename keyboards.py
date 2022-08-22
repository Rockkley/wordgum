from configparser import ConfigParser
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import main
import os
import parsers


def show_main_menu():

    main_menu_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=main.conf['KEYBOARDS']['play'],           callback_data='lang_page')
            ],
            [
                InlineKeyboardButton(text=main.conf['KEYBOARDS']['my_statistic'],   callback_data='stat_page')
            ],
            [
                InlineKeyboardButton(text=main.conf['KEYBOARDS']['top5players'],    callback_data='top_page')
            ],
            [
                InlineKeyboardButton(text=main.conf['KEYBOARDS']['about_game'],     callback_data='about_page')]])
    return main_menu_kb


def show_lang_menu(dicts_data):
    print(dicts_data)
    language_kb = InlineKeyboardMarkup(
        inline_keyboard=[  # Generates language choice inline keyboard of language folders from the 'dicts' folder
            [InlineKeyboardButton(text=dicts_data[language]['flag'] + language.capitalize(),
                                  callback_data='play_'+language[:3]) for language in dicts_data],
            [InlineKeyboardButton(text=main.conf['KEYBOARDS']['back'],            callback_data='main_page')]])
    return language_kb


def show_stat_menu():
    stat_kb = InlineKeyboardMarkup(
        inline_keyboard=[[
                InlineKeyboardButton(text=main.conf['KEYBOARDS']['back'],         callback_data='main_page')]])
    return stat_kb


def show_category_menu(call, opened):

    languages_list = os.listdir('dicts')
    categories_list = dict.fromkeys(languages_list)
    for folder in os.listdir('dicts'):
        categories_list[folder[:3]] = os.listdir(f'dicts/{folder}')

    lang = call.data[5:]
    print(categories_list[lang])
    categories_new = {}
    categories = {'Животные 🦄': 'cat_animals', 'Еда 🌭': 'cat_food',  # fixme
                  'Город 🏙': 'cat_city', 'Музыка 🎼': 'cat_music'}

    is_locked = ['' if i < opened else '🔒' for i in range(len(categories))]
    # Creating buttons list from categories

    buttons = [InlineKeyboardButton(text=str(is_locked[i]+list(categories.keys())[i]),
                                    callback_data='locked' if is_locked[i] == '🔒'
                                    else list(categories.values())[i]+lang) for i in range(len(categories))]
    buttons = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    buttons.append([InlineKeyboardButton(text=main.conf['KEYBOARDS']['back'], callback_data='main_page')])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def show_about_page_kb():
    about_page_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=main.conf['KEYBOARDS']['support_project'],
                                     url=main.conf['KEYBOARDS']['tinkoff_url'])
            ], [
                InlineKeyboardButton(text=main.conf['KEYBOARDS']['back'],    callback_data='main_page')
            ]])
    return about_page_kb
