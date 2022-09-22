import json
import os
import sqlite3
from configparser import ConfigParser
from aiogram import types
from datetime import datetime
import dicts
import game
from prettytable import PrettyTable as Pt
import keyboards
import main
from datetime import date


def show_welcome_text() -> str:
    main.conf.read('conf.ini', encoding="UTF-8")
    current_hour = datetime.now().hour
    txt = [main.conf['TEXTS']['good_night'], main.conf['TEXTS']['good_morning'],
           main.conf['TEXTS']['good_day'], main.conf['TEXTS']['good_evening']]
    return txt[current_hour//6]


class UserInfoParser:

    def __init__(self, msg: types.CallbackQuery):
        #  Register user if new
        self.conn = sqlite3.connect('./databases/users.db')
        self.cur = self.conn.cursor()
        self.cur.execute(f'INSERT OR IGNORE INTO users '
                         f'VALUES(null,"{msg.from_user.id}","{msg.from_user.username}","{msg.from_user.first_name}",'
                         f'"{msg.from_user.last_name}","1","{date.today()}")')
        self.conn.commit()

        main.conf.read('conf.ini', encoding="UTF-8")

    async def endgame(self, call):
        await call.message.edit_text(text=self.show_after_game_text(call),
                                     parse_mode='HTML',
                                     reply_markup=keyboards.show_main_menu())
        game.SessionData.score[call.from_user.id] = game.SessionData.ten[call.from_user.id] = game.SessionData.cups[
            call.from_user.id] = 0
        game.SessionData.used_words[call.from_user.id] = []
        game.SessionData.wrong_words[call.from_user.id] = set()

    def show_main_menu_text(self, msg) -> str:
        # Forms Main page text
        main_menu_text = f'<b>WordsGum - - Главное меню</b>\n' \
                         f'{show_welcome_text()} {msg.from_user.username}\n' \
                         f'🔸 Ранг <b>{self.get_user_level(msg)} {self.get_user_degree(msg)}</b>'
        return main_menu_text

    def get_user_cups(self, msg, language):
        self.cur.execute('SELECT ? FROM scores WHERE telegram_id = ?', (language, msg.from_user.id))

    def get_user_level(self, msg) -> int:
        # Gets level of a user
        self.cur.execute('SELECT level FROM users WHERE telegram_id = ?', (msg.from_user.id,))
        user_level = self.cur.fetchone()[0]
        return user_level

    def write_user_level(self, msg):
        # Writes users level calculated of cups sum to the database
        user_level = 1  # fixme
        self.cur.execute(f'UPDATE users SET level = ? WHERE telegram_id = ?', (user_level, msg.from_user.id))
        self.conn.commit()

    def get_user_degree(self, msg) -> str:
        # Gets degree of a user
        main.conf.read('conf.ini', encoding="UTF-8")
        user_level = self.get_user_level(msg)
        degree = ('Новичок', 'Говорун', 'Толмач', 'Лексикограф', 'Слововяз')
        return degree[user_level//10]

    def _show_stat_menu_text(self, msg) -> str:
        # Forms statistic page text
        self.write_user_level(msg)

        stat_text = f'<b>WordsGum - - Статистика</b>\n' \
                    f'Пользователь {msg.from_user.username}\n' \
                    f'ID - {msg.from_user.id}\n' \
                    f'🔸 Ранг <b>{self.get_user_level(msg)} {self.get_user_degree(msg)}</b>\n'\
                    f'🏆 Кубки:\n'
                   # f'🇺🇸: {self.get_eng_cups(msg)} 🇫🇮: {self.get_fin_cups(msg)}'  # fixme

        self.conn.close()
        return stat_text

    def _show_cat_menu_text(self, lang):
        print(lang.data)

        # Forms category page text # fixme
        language = ''
        if lang.data[5:] == 'suo':
            language = '🇫🇮Финский'
        elif lang.data[5:] == 'eng':
            language = '🇺🇸Английский'

        cat_text = f'<b>WordsGum - - Выберите категорию</b>\n' \
                   f'{language} язык. Доступно {2+self.get_user_level(lang)//10} из 4 категорий.\n' \
                   f'До открытия следующей категории осталось получить {10-int(str(self.get_user_level(lang))[-1])} кубков'

        return cat_text

    def show_after_game_text(self, call) -> str:
        if game.SessionData.cups.get(call.from_user.id) == 0:
            cups_result_text = 'Для получения 🏆 необходимо отгадать 10 слов.'
        else:
            cups_result_text = f'Получено 🏆 - {game.SessionData.cups.get(call.from_user.id)}'

        return f'Вы завершили игру со счётом {game.SessionData.score.get(call.from_user.id)}.\n{cups_result_text}\n'

    def show_top_page_text(self) -> str:
        self.cur.execute('SELECT * FROM users')
        users = sorted(self.cur.fetchall(), key=lambda user: user[2]+user[3], reverse=True)
        self.cur.close()
        # Creating table
        tb = Pt()
        tb.field_names = ["Имя", "🇺🇸", "🇫🇮", "Общий"]
        for i in range(5):
            tb.add_row([users[i][1], users[i][2], users[i][3], users[i][4]])

        return f'<b>WordsGum- - ТОП 5 участников</b>\n<i>из {len(users)}</i><pre>{str(tb)}</pre>'


async def scan_dicts() -> dict:
    lang_info = ConfigParser()
    languages_and_flags = {}

    for language in os.listdir("dicts/"):
        lang_info.read(f'dicts/{language}/info.ini', encoding="UTF-8")
        languages_and_flags[language] = lang_info['MAIN']['flag']
    print(f'parsers -> scan_dicts -> keyboards \n{languages_and_flags}\n# # # # # ')
    return languages_and_flags


def scan_lang(categories_list, lang) -> dict:
    for category in categories_list[lang]:
        with open(f'dicts/{lang}/{category}') as file:
            data = json.load(file)["title"]
        return data
