import sqlite3
import sys
import traceback
from os import path


#------------ Конфигруция ------------------
dbname = 'ptrack.db'
#-------------------------------------------

def conf_load():
    if path.exists(dbname):
        create_db()
    exec_sql_file('sql/c_config.sql')
    exec_sql_file('sql/c_input_data.sql')
    exec_sql('DROP TABLE IF EXISTS Groups;')
    exec_sql_file('sql/c_groups.sql')
    exec_sql('DROP TABLE IF EXISTS Work;')
    exec_sql_file('sql/c_work.sql')
    exec_sql_file('sql/f_work-1.sql')
    exec_sql_file('sql/f_work-2.sql')
    exec_sql_file('sql/f_work-3.sql')
    #exec_sql ('INSERT INTO Work VALUES (1,"----"," ",1," "," ")')
    exec_sql('''INSERT INTO Work (NAME, EPC, EPC_NUM, StartDT, EndDT)
    SELECT Groups.Name, Input_Data.EPC, 1, Input_Data.StartDT ,Input_Data.EndDT
    FROM Input_Data
    INNER JOIN Groups ON EPC = Groups.EPC1;''')

def create_db():
    #global sqlite_connection
    try:
        sqlite_connection = sqlite3.connect(dbname)
        cursor = sqlite_connection.cursor()
        print("База данных создана и успешно подключена к SQLite")
        sqlite_select_query = "select sqlite_version();"
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        print("Версия базы данных SQLite: ", record)
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def exec_sql_file(sql_file: str):
    global sqlite_connection
    try:
        sqlite_connection = sqlite3.connect(dbname)
        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        with open(sql_file, 'r') as sqlite_file:
            sql_script = sqlite_file.read()
        cursor.executescript(sql_script)
        print(f"Скрипт {sql_file} SQLite успешно выполнен")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def exec_sql(sql_script: str):
    try:
        print (sql_script)
        sqlite_connection = sqlite3.connect(dbname)
        cursor = sqlite_connection.cursor()
        #print("База данных подключена к SQLite")

        sqlite_insert_query = sql_script

        count = cursor.execute(sqlite_insert_query)
        sqlite_connection.commit()
        #print("Запись успешно вставлена в таблицу sqlitedb_developers ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Не удалось вставить данные в таблицу sqlite")
        print("Класс исключения: ", error.__class__)
        print("Исключение", error.args)
        print("Печать подробноcтей исключения SQLite: ")
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            #print("Соединение с SQLite закрыто")


def read_sql(sql_script: str):
    try:
        sqlite_connection = sqlite3.connect(dbname, timeout=20)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        sqlite_select_query = sql_script
        cursor.execute(sqlite_select_query)
        total_rows = cursor.fetchall()
        print("Всего строк:  ", total_rows)
        print(str(total_rows))
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")





