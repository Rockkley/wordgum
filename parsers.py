import sqlite3
from aiogram import types
from datetime import datetime
import game
from prettytable import PrettyTable as pt

def welcome_text():
    if 0 <= datetime.now().hour < 6:
        return "🌖 Доброй ночи"
    elif 6 <= datetime.now().hour < 12:
        return "🌅 Доброе утро"
    elif 12 <= datetime.now().hour < 17:
        return "🌞 Добрый день"
    elif 17 <= datetime.now().hour <= 23:
        return "🌃 Добрый вечер"


class UserInfoParser:

    def __init__(self, msg: types.CallbackQuery):
        #  Register user if new
        self.conn = sqlite3.connect('./databases/users.db')
        self.cur = self.conn.cursor()
        self.cur.execute(f'INSERT OR IGNORE INTO users '
                         f'VALUES("{msg.from_user.id}","@{msg.from_user.username}","0","0","1")')
        self.write_user_level(msg)

    def main_menu_text(self, msg):
        # Forms Main page text
        main_menu_text = f'<b>WordsGum - - Главное меню</b>\n' \
                         f'{welcome_text()} {msg.from_user.username}\n' \
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
        degree = ''
        user_level = self.get_user_level(msg)
        if user_level < 10:
            degree = 'Новичок'
        elif 10 <= user_level < 20:
            degree = 'Говорун'
        elif 20 <= user_level <= 30:
            degree = 'Толмач'
        return degree

    def _stat_menu_text(self, msg):
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

    def _cat_menu_text(self, lang):
        # Forms category page text
        language = ''
        if lang.data[5:] == 'fin':
            language = '🇫🇮Финский'
        elif lang.data[5:] == 'eng':
            language = '🇺🇸Английский'

        cat_text = f'<b>WordsGum - - Выберите категорию</b>\n' \
                   f'{language} язык'

        return cat_text

    def after_game_text(self, call):
        cups_result_text = ''
        if game.Answer.cups.get(call.from_user.id) == 0:
            cups_result_text = 'Для получения 🏆 необходимо отгадать 10 слов.'
        else:
            cups_result_text = f'Получено 🏆 - {game.Answer.cups.get(call.from_user.id)}'

        return f'Вы завершили игру со счётом {game.Answer.score.get(call.from_user.id)}.\n{cups_result_text}'

    def top_page_text(self):
        self.cur.execute('SELECT * FROM users')
        users = sorted(self.cur.fetchall(), key=lambda user: user[2]+user[3], reverse=True)
        string = ''

        # Creating table
        tb = pt()

        tb.field_names = ["№", "Имя", "🇺🇸", "🇫🇮", "Общий"]
        for i in range(5):
            tb.add_row([i+1, users[i][1], users[i][2], users[i][3], users[i][4]])

        return f'<b>WordsGum- - ТОП 5 участников</b>\n  <pre>{str(tb)}</pre>'

