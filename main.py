from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types
import keyboards
import parsers
import game
from configparser import ConfigParser
import sqlite3
import os

conf = ConfigParser()
conf.read('conf.ini', encoding="UTF-8")
bot = Bot(os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())


# Main menu
@dp.message_handler(commands=['start'])
async def start(msg: types.CallbackQuery):

    user_info = parsers.UserInfoParser(msg)
    await bot.send_message(chat_id=msg.from_user.id,
                           reply_markup=keyboards.show_main_menu(),
                           text=user_info.show_main_menu_text(msg),
                           parse_mode='HTML')


@dp.callback_query_handler()
async def show_main_menu(call: types.CallbackQuery):

    user_info = parsers.UserInfoParser(call)
    if call.data == 'lang_page':
        await call.message.edit_text(text='<b>WordsGum - - Меню игры</b>\nВыберите язык:',
                                     parse_mode='HTML',
                                     reply_markup=keyboards.show_lang_menu(await parsers.scan_dicts()))
    if call.data == 'about_page':
        await call.message.edit_text(text=conf['TEXTS']['about_bot_text'],
                                     disable_web_page_preview=True,
                                     parse_mode='HTML',
                                     reply_markup=keyboards.show_about_page_kb())
    if call.data == 'main_page':
        await call.message.edit_text(text=user_info.show_main_menu_text(call),
                                     parse_mode='HTML',
                                     reply_markup=keyboards.show_main_menu())
    if call.data == 'top_page':
        await call.message.edit_text(text=user_info.show_top_page_text(),
                                     parse_mode='HTML',
                                     reply_markup=keyboards.show_stat_menu())

    if call.data == 'stat_page':
        await call.message.edit_text(text=user_info._show_stat_menu_text(call),
                                     parse_mode='HTML',
                                     reply_markup=keyboards.show_stat_menu())

    if call.data.startswith('lang'):
        # user_level = user_info.get_user_level(call)
        await call.message.edit_text(text=user_info._show_cat_menu_text(call),
                                     parse_mode='HTML',
                                     reply_markup=keyboards.show_category_menu(
                                         call, 2+user_info.get_user_level(call)//10))
    if call.data == 'endgame_page':
        await user_info.endgame(call)

    if call.data.startswith('cat_'):
        try:
            await game.set_game(call)
        except Exception:
            await call.answer(conf['TEXTS']['section_in_development'])

    if call.data == 'locked':
        locked_msg = conf['TEXTS']['not_enough_cups_to_open'].split()
        locked_msg.insert(3, str(10-int(str(user_info.get_user_level(call))[-1])))
        await call.answer(' '.join(locked_msg))

    if call.data.startswith('!'):
        if call.data[1:] == game.SessionData.answer.get(call.from_user.id):
            await call.answer(conf['TEXTS']['correct_answer'])
            game.SessionData.score[call.from_user.id] += 1
            game.SessionData.ten[call.from_user.id] += 1
            game.SessionData.used_words[call.from_user.id].append(call.data[1:])

            if game.SessionData.ten[call.from_user.id] == 10:
                await call.answer(conf['TEXTS']['cup_achieved'])
                lang = str(game.SessionData.lang[call.from_user.id]+'_score')
                # Adding +1 cup to database
                user_info.cur.execute(f'SELECT {lang} FROM users WHERE telegram_id = {call.from_user.id}')
                current_score = user_info.cur.fetchone()[0]
                user_info.cur.execute(f'UPDATE users SET {lang} = {current_score+1} '
                                      f'WHERE telegram_id = {call.from_user.id}')
                user_info.conn.commit()
                # Updating SessionData
                game.SessionData.cups[call.from_user.id] += 1
                game.SessionData.ten[call.from_user.id] = 0

        else:
            await call.answer(conf['TEXTS']['incorrect_answer'])
            # Updating SessionData
            game.SessionData.wrong_words[call.from_user.id].add(call.data[1:])
            game.SessionData.ten[call.from_user.id] = 0
            game.SessionData.used_words[call.from_user.id].clear()
            if game.SessionData.score[call.from_user.id] > 0:
                game.SessionData.score[call.from_user.id] -= 1

            # If only 1 word left, game ends
        if len(game.SessionData.dict[call.from_user.id]) > 2:
            await game.set_game(game.SessionData.call.get(call.from_user.id))
        else:
            await user_info.endgame(call)

if __name__ == '__main__':
    conn = sqlite3.connect('./databases/users.db')
    cur = conn.cursor()

    create_users_table = open('./sql/create_users_table.sql')
    cur.executescript(create_users_table.read())
    create_users_table.close()

    create_score_table = open('./sql/create_score_table.sql')
    cur.executescript(create_score_table.read())
    create_score_table.close()
    cur.close()
    executor.start_polling(dp)
