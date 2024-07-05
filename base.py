# пробую работать с SQLite
import sqlite3 as sl
import os
from datetime import datetime

def sql_addendum(data):
    # подготавливаем множественный запрос
    sql = ('INSERT INTO reminder (id, chat_id, human, time, time_bot_day, time_bot_min, '
           'reminder_time, commits) values(?, ?, ?, ?, ?, ?, ?, ?)')
    # добавляем с помощью множественного запроса все данные сразу
    with connection:
        connection.executemany(sql, data)

def sql_deletion(id):
    with connection:
        connection.execute(f'DELETE FROM reminder WHERE id = {id}')

def sql_update(data, id):
    with connection:
        connection.execute(f'UPDATE reminder SET {data} WHERE id = {id}')

def sql_whatch():
    with connection:
        # получаем количество таблиц с нужным нам именем
        data = connection.execute("SELECT * FROM reminder")
        for row in data:
            current_date = datetime.now()
            date = current_date.replace(second=0, microsecond=0)
            # сверяем дату/время напоминания с текущим
            if (row[3] == date):
                None
            if (row[4] == date):
                None


if __name__ == "__main__":
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