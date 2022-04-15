import github
import random
import telebot
import pandas as pd
from telebot import types

bot = telebot.TeleBot('5287616989:AAHeN3K4ZstBHtHEORurQbwOCokCOQcYMmc')
#g = github.Github('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')
#repo = g.get_user().get_repo("kazakhverificationbot")
#kvdata = repo.get_contents("kvdata.csv")

@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Показать номер", request_contact=True)
    markup.add(button1)
    bot.send_message(m.chat.id, 'Салам! Это бот ЦУС. Чтобы начать верификацию, нажмите "Показать номер".', reply_markup=markup)
    
@bot.message_handler(content_types=['contact'])
def contact(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Показать номер", request_contact=True)
    button2 = types.KeyboardButton(text = 'Показать код')
    markup.add(button1, button2)
    if m.contact is not None:
        if m.from_user.id == m.contact.user_id:
            phone = str(m.contact.phone_number)
            bot.send_message(m.chat.id, 'Ваш номер: ' + phone + '. Принято!', reply_markup=markup)
        else:
            bot.send_message(m.chat.id, 'Кажется, это не Ваш номер. Пожалуйста, поделитесь своим!', reply_markup=markup)
        
        #data = str(kvdata.decoded_content.decode())
        #code = str(random.randint(1000, 9999))
        #repo.update_file("kvdata.csv", "", data + '\n1,1,' + phone + ',1,1,1,1,' + code + ',1,1,1', kvdata.sha)
        
    @bot.message_handler(content_types=['text'])
    def number(message):
        url = 'https://raw.githubusercontent.com/artemsmirnov93/verificationbot/main/kvdata.csv'
        data = pd.read_csv(url)

        if message.text=="Показать код" and message.from_user.id == m.contact.user_id:
            code = str(random.randint(1000, 9999))
            bot.send_message(message.chat.id, 'Ваш код в сообщении ниже. Скопируйте и введите его на странице аутентификации.',  reply_markup=markup)
            bot.send_message(message.chat.id, code, reply_markup=markup)
        
        #if len(data.loc[data['phone']==int(phone)]['pay_id']) > 0:
        #    code = data.loc[data['phone']==int(phone)]['pay_id'].values[-1]
        #    bot.send_message(message.chat.id, 'Ваш код в сообщении ниже. Скопируйте и введите его на странице аутентификации.',  reply_markup=markup)
        #    bot.send_message(message.chat.id, str(code), reply_markup=markup)
        #else:
        #    bot.send_message(message.chat.id, 'Код для этого телефонного номера не обнаружен. Убедитесь, что вы запросили код и возвращайтесь!',  reply_markup=markup)
                
bot.polling(none_stop=True, interval=0)
