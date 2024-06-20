# пробую работать с SQLite
import sqlite3 as sl
import os

path = os.path.realpath('base.py')
path = path.replace('base.py', '')

connection = sl.connect(path + "MyBase.db")

# открываем базу
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
                        human VARCHAR(40),
                        time VARCHAR(16),
                        time_bot_day VARCHAR(16),
                        time_bot_min VARCHAR(16),
                        periodicity INTEGER,
                        reminder_time INTEGER,
                        commits VARCHAR(100)
                    );
                """)

# подготавливаем множественный запрос
sql = ('INSERT INTO reminder (human, time, time_bot_day, time_bot_min, '
       'periodicity, reminder_time, commits) values(?, ?, ?, ?, ?, ?, ?)')
# указываем данные для запроса
data = [
    ('narierdg', '12:12:2023 08%12', '12:12:2023 08%12', '12:12:2023 08%12', 0, 0, 'Врач офтальмолог, 202 кабинет')
]

# добавляем с помощью множественного запроса все данные сразу
with connection:
    connection.executemany(sql, data)

# выводим содержимое таблицы на экран
with connection:
    data = connection.execute("SELECT * FROM reminder")
    for row in data:
        print(row)


# На вход программа получает значения из чата,
# Первым типом, будет время (День:Месяц:Год + Часы:минуты) на которое нужно назначить напоминание.
# (это нужно сделать календарем или выбором, чтобы нельзя было приписывать рандомные значения)
# Второй тип, разовое или цикличное (это можно сделать кнопками)
# Третье, за сколько нужно напомнить о нем (два или три варианта, кнопками)
# Четрвертым значением, будет комментарий по напоминанию (просто текст)
# + id пользователя

# Так же надо сделать ограничение по напоминанияем (30-50)
# И сделать автоматическое удаление напоминаний, которые уже прошли
