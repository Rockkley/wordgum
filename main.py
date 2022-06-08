from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types
import keyboards
import parsers
import game
import conf

API_TOKEN = conf.TELEGRAM_BOT_API_TOKEN
bot = Bot(API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(msg: types.CallbackQuery):
    user_info = parsers.UserInfoParser(msg)
    await bot.send_message(chat_id=msg.from_user.id,
                           reply_markup=keyboards.main_menu(),
                           text=user_info.main_menu_text(msg),
                           parse_mode='HTML')


@dp.callback_query_handler()
async def menu(call: types.CallbackQuery):
    user_info = parsers.UserInfoParser(call)
    if call.data == 'lang_page':
        await call.message.edit_text(text='<b>WordsGum - - Меню игры</b>\nВыберите язык:',
                                     parse_mode='HTML',
                                     reply_markup=keyboards.lang_menu())
    if call.data == 'about_page':
        await call.message.edit_text(text=parsers.about_text(),
                                     disable_web_page_preview=True,
                                     parse_mode='HTML',
                                     reply_markup=keyboards.about_page())
    if call.data == 'main_page':
        await call.message.edit_text(text=user_info.main_menu_text(call),
                                     parse_mode='HTML',
                                     reply_markup=keyboards.main_menu())
    if call.data == 'top_page':
        await call.message.edit_text(text=user_info.top_page_text(),
                                     parse_mode='HTML',
                                     reply_markup=keyboards.stat_menu())
    if call.data == 'endgame_page':
        await user_info.endgame(call)

    if call.data == 'in_development':
        await call.answer('Раздел находится разработке. Try later!')

    if call.data == 'stat_page':
        await call.message.edit_text(text=user_info._stat_menu_text(call),
                                     parse_mode='HTML',
                                     reply_markup=keyboards.stat_menu())

    if call.data.startswith('play'):
        await call.message.edit_text(text=user_info._cat_menu_text(call),
                                     parse_mode='HTML',
                                     reply_markup=keyboards.category_menu(call.data[5:]))

    if call.data.startswith('cat_'):
        await game.set_game(call)

    if call.data.startswith('!'):
        if call.data[1:] == game.SessionData.answer.get(call.from_user.id):
            await call.answer('Правильный ответ!')
            game.SessionData.score[call.from_user.id] += 1
            game.SessionData.ten[call.from_user.id] += 1
            game.SessionData.used_words[call.from_user.id].append(call.data[1:])

            if game.SessionData.ten[call.from_user.id] == 10:
                await call.answer('🏆 Кубок получен!')
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
            await call.answer('❗️ У этого слова другой перевод ❗️')
            # Updating SessionData
            game.SessionData.ten[call.from_user.id] = 0
            game.SessionData.used_words[call.from_user.id].clear()
            if game.SessionData.score[call.from_user.id] > 0:
                game.SessionData.score[call.from_user.id] -= 1

        if len(game.SessionData.dict[call.from_user.id]) > 2:
            await game.set_game(game.SessionData.call.get(call.from_user.id))
        else:

            await user_info.endgame(call)

if __name__ == '__main__':
    executor.start_polling(dp)
