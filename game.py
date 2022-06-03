import random
from aiogram import types
from aiogram.types import CallbackQuery

import dicts
from new import bot, dp


async def set_game(call):
    # print(f'Категория - {call.data[4:-3]}, язык - {call.data[-3:]}')
    dict_data = call.data[4:-3]+'_'+call.data[-3:]
    dictionary = dicts.return_dict(dict_data)

    await run(dictionary, call)

  #  print(f'Создан экземпляр игровой сессии для ID {call.from_user.id}\n'
   #       f'Словарь - {dict_data}\n'
   #       f'^ v ^ v ^ ')


async def run(dictionary, call):
    if call.from_user.id not in Answer.score.keys():
        Answer.score[call.from_user.id] = 0
        Answer.ten[call.from_user.id] = 0
        Answer.cups[call.from_user.id] = 0
        Answer.used_words[call.from_user.id] = []

    Answer.lang[call.from_user.id] = call.data[-3:]
    # Shuffle the chosen dictionary and slice it to 8 words for a new round
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

    await call.message.edit_text(f'🔹 Счёт - {Answer.score.get(call.from_user.id)} '
                                 f'🏆 Кубков - {Answer.cups.get(call.from_user.id)} || Прогресс - {emo_digits[Answer.ten[call.from_user.id]]}<b>/</b>🔟\n\n'
                                 f'Выбери правильный перевод. Кто такой {the_word.callback_data[1:]}?',
                                 reply_markup=markup, parse_mode='HTML')

    Answer.a[call.from_user.id] = the_word.callback_data[1:]
    Answer.call[call.from_user.id] = call
    Answer.dict = dictionary


class Answer:
    a = {}
    call = {}
    score = {}
    ten = {}
    cups = {}
    lang = {}
    used_words = {}
