import random
from aiogram import types
import dicts
import parsers


async def set_game(call):
    dict_data = call.data[4:-3]+'_'+call.data[-3:]
    dictionary = dicts.return_dict(dict_data)
    await run(dictionary, call)


async def run(dictionary, call):
    if call.from_user.id not in SessionData.score.keys():
        SessionData.score[call.from_user.id] = SessionData.ten[call.from_user.id] = \
            SessionData.cups[call.from_user.id] = 0
        SessionData.used_words[call.from_user.id] = []

    SessionData.lang[call.from_user.id] = call.data[-3:]
    if len(SessionData.used_words[call.from_user.id]) != 0:
        _f = dictionary
        for i in range(len((SessionData.used_words[call.from_user.id]))):
            for key, value in dict(_f).items():
                if value == SessionData.used_words[call.from_user.id][i]:
                    del _f[key]

            _ = list(_f.keys())
    else:
        _ = list(dictionary.keys())

    random.shuffle(_)
    session_words = _[:8]

    # Creating inline keyboard from shuffled dictionary
    row = []
    for i in range(len(session_words)):
        word = session_words[i]
        row.append(types.InlineKeyboardButton(word, callback_data='!' + str(dictionary.get(word))))
    random.shuffle(row)
    buttons = [row[:4], row[4:]]
    markup = types.InlineKeyboardMarkup(row_width=4, inline_keyboard=buttons)
    markup.add(types.InlineKeyboardButton('Завершить игру', callback_data='endgame_page'))
    the_word = random.choice(row)

    emo_digits = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

    await call.message.edit_text(f'🔹 Счёт - {SessionData.score.get(call.from_user.id)} '
                                 f'🏆 Кубков - {SessionData.cups.get(call.from_user.id)} || '
                                 f'Прогресс - {emo_digits[SessionData.ten[call.from_user.id]]}<b>/</b>🔟\n\n'
                                 f'Выбери правильный перевод. Кто такой {the_word.callback_data[1:]}?',
                                 reply_markup=markup, parse_mode='HTML')

    SessionData.answer[call.from_user.id] = the_word.callback_data[1:]
    SessionData.call[call.from_user.id] = call
    SessionData.dict[call.from_user.id] = dictionary


class SessionData:
    dict = {}
    answer = {}
    call = {}
    score = {}
    ten = {}
    cups = {}
    lang = {}
    used_words = {}
