import telebot
from telebot import types
import os

path = os.path.realpath('main.py')
path = path.replace('main.py', '')

with open(path + "token.pkl", "r") as f:
    token = f.read()
bot = telebot.TeleBot(str(token))

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Add reminder")
    btn2 = types.KeyboardButton("Сhange of reminder")
    btn3 = types.KeyboardButton("Today's plans")
    btn4 = types.KeyboardButton("All plans")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id,
                     text="HI, {0.first_name}! I am here to remind you of your plan.".format(
                         message.from_user), reply_markup=markup)
@bot.message_handler(content_types=['text'])
def main_func(message):
    if (message.text == "Add reminder"): addreminder(message)
    elif (message.text == "Сhange reminder"): changereminder(message)
    elif (message.text == "Today's plans"): todaysplans(message)
    elif (message.text == "All plans"): allplans(message)
    else:
        bot.send_message(message.chat.id, text="I wasn't taught that..")

def addreminder(message):
    bot.send_message(message.chat.id, text="addreminder")

def changereminder(message):
    bot.send_message(message.chat.id, text="changereminder")

def todaysplans(message):
    bot.send_message(message.chat.id, text="todaysplans")

def allplans(message):
    bot.send_message(message.chat.id, text="allplans")

bot.polling(none_stop=True)