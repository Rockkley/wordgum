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


def show_welcome_text():
    main.conf.read('conf.ini', encoding="UTF-8")
    current_hour = datetime.now().hour
    txt = {0: main.conf['TEXTS']['good_night'], 1: main.conf['TEXTS']['good_morning'],
           2: main.conf['TEXTS']['good_day'], 3: main.conf['TEXTS']['good_evening']}
    return txt[current_hour//6]


class UserInfoParser:

    def __init__(self, msg: types.CallbackQuery):
        #  Register user if new
        self.conn = sqlite3.connect('./databases/users.db')
        self.cur = self.conn.cursor()
        self.cur.execute(f'INSERT OR IGNORE INTO users '
                         f'VALUES("{msg.from_user.id}","@{msg.from_user.username}","0","0","1","0","0")')
        self.write_user_level(msg)
        main.conf.read('conf.ini', encoding="UTF-8")

    async def endgame(self, call):
        await call.message.edit_text(text=self.show_after_game_text(call),
                                     parse_mode='HTML',
                                     reply_markup=keyboards.show_main_menu())
        game.SessionData.score[call.from_user.id] = game.SessionData.ten[call.from_user.id] = game.SessionData.cups[
            call.from_user.id] = 0
        game.SessionData.used_words[call.from_user.id] = []
        game.SessionData.wrong_words[call.from_user.id] = set()

    def show_main_menu_text(self, msg):
        # Forms Main page text
        main_menu_text = f'<b>WordsGum - - Главное меню</b>\n' \
                         f'{show_welcome_text()} {msg.from_user.username}\n' \
                         f'🔸 Ранг <b>{self.get_user_level(msg)} {self.get_user_degree(msg)}</b>'
        return main_menu_text

    def get_eng_cups(self, msg):
        # Gets English language cups score of a user
        self.cur.execute('SELECT eng_score FROM users WHERE telegram_id = ?', (msg.from_user.id,))
        user_eng_cups = self.cur.fetchone()[0]
        return user_eng_cups

    def get_fin_cups(self, msg):
        # Gets Suomi language cups score of a user
        self.cur.execute('SELECT fin_score FROM users WHERE telegram_id = ?', (msg.from_user.id,))
        user_fin_cups = self.cur.fetchone()[0]
        return user_fin_cups

    def get_user_level(self, msg):
        # Gets level of a user
        self.cur.execute('SELECT level FROM users WHERE telegram_id = ?', (msg.from_user.id,))
        user_level = self.cur.fetchone()[0]
        return user_level

    def write_user_level(self, msg):
        # Writes users level calculated of cups sum to the database
        user_level = int(self.get_fin_cups(msg)) + int(self.get_eng_cups(msg))
        self.cur.execute(f'UPDATE users SET level = ? WHERE telegram_id = ?', (user_level, msg.from_user.id))
        self.conn.commit()

    def get_user_degree(self, msg):
        # Gets degree of a user
        main.conf.read('conf.ini', encoding="UTF-8")
        user_level = self.get_user_level(msg)
        degree = {0: 'Новичок', 1: 'Говорун', 2: 'Толмач', 3: 'Лексикограф', 4: 'Слововяз'}
        return degree[user_level//10]

    def _show_stat_menu_text(self, msg):
        # Forms statistic page text
        self.write_user_level(msg)

        stat_text = f'<b>WordsGum - - Статистика</b>\n' \
                    f'Пользователь {msg.from_user.username}\n' \
                    f'ID - {msg.from_user.id}\n' \
                    f'🔸 Ранг <b>{self.get_user_level(msg)} {self.get_user_degree(msg)}</b>\n'\
                    f'🏆 Кубки:\n' \
                    f'🇺🇸: {self.get_eng_cups(msg)} 🇫🇮: {self.get_fin_cups(msg)}'

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

    def show_after_game_text(self, call):
        if game.SessionData.cups.get(call.from_user.id) == 0:
            cups_result_text = 'Для получения 🏆 необходимо отгадать 10 слов.'
        else:
            cups_result_text = f'Получено 🏆 - {game.SessionData.cups.get(call.from_user.id)}'

        return f'Вы завершили игру со счётом {game.SessionData.score.get(call.from_user.id)}.\n{cups_result_text}\n'

    def show_top_page_text(self):
        self.cur.execute('SELECT * FROM users')
        users = sorted(self.cur.fetchall(), key=lambda user: user[2]+user[3], reverse=True)
        self.cur.close()
        # Creating table
        tb = Pt()
        tb.field_names = ["Имя", "🇺🇸", "🇫🇮", "Общий"]
        for i in range(5):
            tb.add_row([users[i][1], users[i][2], users[i][3], users[i][4]])

        return f'<b>WordsGum- - ТОП 5 участников</b>\n<i>из {len(users)}</i><pre>{str(tb)}</pre>'


def scan_dicts():
    dir_list = os.listdir("dicts/")

    langpacks_info = ConfigParser()
    dicts_data = {}

    for i in dir_list:
        langpacks_info.read(f'dicts/{i}/info.ini', encoding="UTF-8")
        dicts_data[i] = {
            'flag': langpacks_info['MAIN']['flag'],
            'categories': [x for x in os.listdir(f"dicts/{i}")]}

    return dicts_data

