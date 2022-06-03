from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types
import keyboards
import parsers
import game
import conf
import os
# webhook settings
WEBHOOK_HOST = f'https://wordgum.herokuapp.com'
WEBHOOK_PATH = conf.TELEGRAM_BOT_API_TOKEN
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

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
async def menu_navigation(call: types.CallbackQuery):
    user_info = parsers.UserInfoParser(call)
    if call.data == 'lang_page':
        await call.message.edit_text(text='<b>WordsGum - - Меню игры</b>\nВыберите язык:',
                                     parse_mode='HTML',
                                     reply_markup=keyboards.lang_menu())
    if call.data == 'about_page':
        await call.message.edit_text(text='<b>WordsGum - - Об игре:</b>\n'
                                          'Этот бот поможет вам легко выучить слова Английского и Финского языков.\n'
                                          'Выберите категорию, отвечайте на вопросы и зарабатывайте кубки.\n'
                                          'Следите за своим прогрессом в разделе <i>"Моя статистика"</i>.\n'
                                          'За каждые 10 правильно отгаданных слов вы получаете 1 кубок.\n'
                                          'Автор - Самарин Евгений aka Rockkley\n'
                                          '(@Evgeniy_Samarin, https://github.com/Rockkley)',
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
        await call.message.edit_text(text=user_info.after_game_text(call),
                                     parse_mode='HTML',
                                     reply_markup=keyboards.main_menu())
        game.Answer.score[call.from_user.id] = 0
        game.Answer.ten[call.from_user.id] = 0
        game.Answer.cups[call.from_user.id] = 0

    if call.data == 'in_development':
        await call.answer('Раздел находится разработке. Try later!')
    if call.data == 'stat_page':
        await call.message.edit_text(text=user_info._stat_menu_text(call),
                                     parse_mode='HTML',
                                     reply_markup=keyboards.stat_menu())
    if call.data == 'play_eng' or call.data == 'play_fin':
        await call.message.edit_text(text=user_info._cat_menu_text(call),
                                     parse_mode='HTML',
                                     reply_markup=keyboards.category_menu(call.data[5:]))
    if call.data.startswith('cat_'):

        await game.set_game(call)

    if call.data.startswith('!'):

        if call.data[1:] == game.Answer.a.get(call.from_user.id):
            game.Answer.used_words[call.from_user.id].append(game.Answer.a.get(call.from_user.id))
            print(game.Answer.used_words)
            await call.answer('Правильный ответ!')
            game.Answer.score[call.from_user.id] += 1
            game.Answer.ten[call.from_user.id] += 1
            if game.Answer.ten[call.from_user.id] == 10:
                await call.answer('🏆 Кубок получен!')
                lang = str(game.Answer.lang[call.from_user.id]+'_score')
                user_info.cur.execute(f'SELECT {lang} FROM users WHERE telegram_id = {call.from_user.id}')
                current_score = user_info.cur.fetchone()[0]
                user_info.cur.execute(f'UPDATE users SET {lang} = {current_score+1} WHERE telegram_id = {call.from_user.id}')
                user_info.conn.commit()
                game.Answer.cups[call.from_user.id] += 1
                game.Answer.ten[call.from_user.id] = 0

            await game.set_game(game.Answer.call.get(call.from_user.id))

        else:
            if game.Answer.a.get(call.from_user.id) in game.Answer.used_words[call.from_user.id]:
                game.Answer.used_words[call.from_user.id].remove(game.Answer.a.get(call.from_user.id))
            print(game.Answer.used_words)
            await call.answer('❗️ У этого слова другой перевод ❗️')
            if game.Answer.score[call.from_user.id] > 0:
                game.Answer.score[call.from_user.id] -= 1
            await game.set_game(game.Answer.call.get(call.from_user.id))


if __name__ == '__main__':
    executor.start_polling(dp)
