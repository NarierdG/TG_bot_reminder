import time
import telebot
from telebot import types
import os
import sqlite3 as sl
import threading
from datetime import datetime


# узнаем абсолютный путь main и обрезаем от main.py
path = os.path.realpath('main.py')
path = path.replace('main.py', '')

# забираем токен из отдельного файла
with open(path + "token.pkl", "r") as f:
    token = f.read()
bot = telebot.TeleBot(str(token))


def create_table():
    connection = sl.connect(path + "MyBase.db")
    with connection:
        # получаем количество таблиц с нужным нам именем
        data = connection.execute("select count(*) from sqlite_master where type='table' and name='reminder'")
        for row in data:
            # если таких таблиц нет
            if row[0] == 0:
                # создаём таблицу для товаров
                with connection:
                    connection.execute("""
                            CREATE TABLE reminder (
                            id INTEGER AUTO_INCREMENT PRIMARY KEY,
                            chat_id INTEGER,
                            human VARCHAR(40),
                            time VARCHAR(16),
                            time_bot_day VARCHAR(16),
                            time_bot_min VARCHAR(16),
                            reminder_time INTEGER,
                            commits VARCHAR(100)
                        );
                    """)


# обработка команды /start и добавление клавиатуры с вариантами кнопок
@bot.message_handler(commands=['start'])
def start(message):
    create_table()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Добавить напоминание 📒")
    btn2 = types.KeyboardButton("Изменить напоминание 📇")
    btn3 = types.KeyboardButton("Сегодняшние планы 📃")
    btn4 = types.KeyboardButton("Все напоминания 📚")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я здесь для того, чтобы напомнить Вам о вашем плане. 🤔".format(
                         message.from_user), reply_markup=markup)


# обработка текстовых команд
@bot.message_handler(content_types=['text'])
def main_func(message):
    if (message.text == "Добавить напоминание 📒"): addreminder(message)
    elif (message.text == "Изменить напоминание 📇"): changereminder(message)
    elif (message.text == "Сегодняшние планы 📃"): todaysplans(message)
    elif (message.text == "Все напоминания 📚"): allplans(message)
    else:
        bot.send_message(message.chat.id, text="Такому меня еще не учили..")


def addreminder(message):
    connection = sl.connect(path + "MyBase.db")
    # подготавливаем множественный запрос
    sql = ('INSERT INTO reminder (chat_id, human, time, time_bot_day, time_bot_min, '
           'reminder_time, commits) values(?, ?, ?, ?, ?, ?, ?)')
    data = []
    bot.send_message(message.chat.id, text="Пожалуйста, укажите дату в следующем формате: YYYY-MM-DD HH:MM:SS")
    if (len(message.text) != 16 or datetime.strptime(message.text, "%Y-%m-%d %H:%M:%S") == False):
        bot.send_message(message.chat.id, text="Я думаю, что Вы, возможно, допустили ошибку в своем сообщении. 🤔")
        bot.send_message(message.chat.id, text="Чтобы внести ясность, позвольте мне начать "
                                               "с самого начала нашего разговора.")
        start(message)
        return
    data.append = str(message.text)
    # добавляем с помощью множественного запроса все данные сразу
    with connection:
        connection.executemany(sql, tuple(data))


def changereminder(message):
    bot.send_message(message.chat.id, text="todaysplans")

def todaysplans(message):
    bot.send_message(message.chat.id, text="todaysplans")

def allplans(message):
    bot.send_message(message.chat.id, text="todaysplans")


def update_database():
    while (True):
        connection = sl.connect(path + "MyBase.db")
        data = connection.execute("SELECT * FROM reminder")
        for row in data:
            current_date = datetime.now()
            date_now = current_date.replace(second=0, microsecond=0)
            # сверяем дату/время напоминания с текущим
            if (row[4] == date_now):
                bot.send_message(chat_id=data[1], text=f'Привет, {data[2]}, напоминаю, что завтра: {data[3]} '
                                                       f' у тебя заплонированно: {data[7]}')
            if (row[5] == date_now):
                bot.send_message(chat_id=data[1], text=f'Привет, {data[2]}, напоминаю, что  {data[3]} '
                                                       f' У тебя заплонированно: {data[7]}')
        time.sleep(50)


# создаем тред для базы данных
thread = threading.Thread(target=update_database)
thread.start()

# непрерывный polling бота
bot.polling(none_stop=True, interval=0)