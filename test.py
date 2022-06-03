# API Ключи и импорт библиотек
import telebot
from telebot import types
import random
import time

API_TOKEN = '5171246594:AAFMy2YKNoM_7AOvGZnXwbmN3ciVPY6ZXHA'
bot = telebot.TeleBot(API_TOKEN)
words = {'Dog': 'Собака', 'Сat': 'Кошка', 'Parrot': 'Попугай', 'Elephant': 'Слон', 'Carrot': 'Морковь', 'Bird': 'Птица',
         'Eagle': 'Орёл', 'Bug': 'Жук'}


@bot.message_handler(commands='start')
def starwindow(message):
    global zgdword, zgan, msg

    row = []
    randnum = random.randint(0, len(words)) - 1
    zgdword = [*words.values()][randnum]
    zgan = "'" + [*words.keys()][randnum] + "'"

    for i in range(len(words)):
        kk = "'" + list(words)[i] + "'"
        print(kk)
        row.append(telebot.types.InlineKeyboardButton([*words.keys()][i], callback_data=kk))
        random.shuffle(row)
    buttons = [row[:4], row[4:]]
    markup=telebot.types.InlineKeyboardMarkup(buttons)
    bot.send_message(message.chat.id,f'Выбери правильный перевод. Кто такой {zgdword}?', reply_markup=markup)

@bot.callback_query_handler(func=lambda c: True)

def answer(c):
    global zgdword, zgan
    if str(c.data) == str(zgan):
        
        row=[]
        randnum = random.randint(0, len(words)) - 1
        zgdword = [*words.values()][randnum]
        zgan = "'"+[*words.keys()][randnum]+"'"

        for i in range(len(words)):
            kk="'"+list(words)[i]+"'"
            print(kk)
            row.append(telebot.types.InlineKeyboardButton([*words.keys()][i], callback_data=kk))
            random.shuffle(row)
        buttons = [row[:4],row[4:]]
        markup=telebot.types.InlineKeyboardMarkup(buttons)
        bot.delete_message(chat_id=c.message.chat.id, message_id=c.message.message_id)
        bot.send_message(c.message.chat.id, 'YES')
        bot.send_message(c.message.chat.id,f'Выбери правильный перевод. Кто такой {zgdword}?', reply_markup=markup)

    else:
        row=[]
        randnum = random.randint(0, len(words)) - 1
        zgdword = [*words.values()][randnum]
        zgan = "'"+[*words.keys()][randnum]+"'"

        for i in range(len(words)):
            kk="'"+list(words)[i]+"'"
            print(kk)
            row.append(telebot.types.InlineKeyboardButton([*words.keys()][i], callback_data=kk))
            random.shuffle(row)
        buttons = [row[:4], row[4:]]
        markup = telebot.types.InlineKeyboardMarkup(buttons)
        bot.delete_message(chat_id=c.message.chat.id, message_id=c.message.message_id)
        bot.send_message(c.message.chat.id, 'У этого слова другой перевод. Попробуй ещё раз!')
        bot.send_message(c.message.chat.id, f'Выбери правильный перевод. Кто такой {zgdword}?', reply_markup=markup)

bot.infinity_polling()