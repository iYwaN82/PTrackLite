import csv
import datetime
import re
from os import path, listdir
from lite import *



def str_to_datetime(input: str) -> datetime:
    out = datetime.datetime.fromisoformat(input.rstrip())
    return out


def remove_bad_strings(str: str):
    out = ''
    # print(str)
    regex = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} EPC: [0-9A-F]{24}, TID: [0-9A-F]{24}"
    matches = re.search(regex, str)
    if matches:
        out = matches.group()
        # print (out)
        # print(f"Выход в файл: {out}")
    else:
        out = ''
        # print(f"Строка потеряна: {str}")
    return out


def save_groups(gr:str,data):
    out=[]
    for line in data:
        #print (line)
        out.append([line['Группа'],line['EPC'][0],line['EPC'][1],line['EPC'][2]])
    with open(gr, 'w') as f:
        writer = csv.writer(f, delimiter = ",", lineterminator="\r")
        writer.writerows(out)


def load_groups(groups_file:str):
    # подключаем БД
    sqlite_connection = sqlite3.connect(dbname)
    cursor = sqlite_connection.cursor()
    with open(groups_file, newline='') as f:
        reader = csv.reader(f, delimiter= ",")
        for row in reader:
            sc = f"INSERT INTO Groups (Name, EPC1,EPC2,EPC3) VALUES ('{row[0]}','{row[1]}','{row[2]}', '{row[3]}');"
            cursor.execute(sc)
    sqlite_connection.commit()  # Сораняем БД
    print("Группы датчиков загружены")
    cursor.close()  # Закрываем БД


def load_dir(input_dir: str, out_dir: str):
    for filename in listdir(input_dir):
        if path.isfile(out_dir + filename): print (f"Файл {out_dir + filename} уже обработан и находится в папке: {out_dir[:-1]}")
        if not path.isfile(out_dir+filename):
            print(f"Читаем файл {input_dir + filename}")
            out = ''
            with open(path.join(input_dir, filename), 'rb') as f:
                for x in f:
                    good_out = remove_bad_strings(str(x))
                    if good_out:
                        out += good_out + "\n"
                f.close()
            # Сохраняем файл в иторию
            o = open(path.join(out_dir, filename), 'w')
            o.write(out)
            o.close()
            # Загружаем в БД
            load_data(out)


def load_data(input_file_data):
    # подключаем БД
    sqlite_connection = sqlite3.connect(dbname)
    cursor = sqlite_connection.cursor()
    #Задаем базовые переменные
    input = input_file_data.split('\n')
    out = []
    old_epc = ''
    old_dt = ''
    start_dt = ''
    end_dt = ''
    epc = ''
    dt = ''
    count = 0
    # good_count = 0
    # f = open(file_in, 'r')
    for line in input:
        count += 1
        #print(f"COUNT: {count} LEN:{len(input)}")
        old_epc = epc
        old_dt = dt
        dt = line[0:19]
        epc = line[25:49]
        if epc == old_epc or old_epc == '': end_dt = line[0:19].strip()
        if start_dt == '': start_dt = old_dt
        if epc != old_epc:
            if old_epc != '':
                if end_dt == '': end_dt = start_dt
                df = str(str_to_datetime(end_dt.strip()) - str_to_datetime(start_dt.strip()))
                #if count == len(input): print(f"последняя строка old_epc={old_epc} epc={epc}"); old_epc=epc
                out.append({'EPC': old_epc, 'StartDT': start_dt, 'EndDT': end_dt, 'Dif': df})
                #Заполняем БД
                sc = f"INSERT INTO input_data (EPC, StartDT,EndDT,Dif) VALUES ('{old_epc}','{start_dt}','{end_dt}', '{df}');"
                cursor.execute(sc)
                #sqlite_connection.commit()
                start_dt = ''
                end_dt = ''
    #sc = f"INSERT INTO input_data (EPC, StartDT,EndDT,Dif) VALUES ('{old_epc}','{start_dt}','{end_dt}', '{df}');"
    #cursor.execute(sc)
    #sqlite_connection.commit()
    sqlite_connection.commit() #Сораняем БД
    cursor.close() #Закрываем БД

    """
    good_count += 1  
    f.close()
    print(f"Обработано {all_count} строк, получено записей: {good_count}, ",
          f"процент избыточных данных: {round(int(all_count) / int(good_count) * 100, 2)}%")
    
    try:
        with open(file_out, 'w') as csvfile:
            fieldnames = ['EPC', 'StartDT', 'EndDT', 'Dif']
            writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames, dialect='excel')
            writer.writeheader()
            writer.writerows(out)
    except:
        print("Файл занят")
    return out
    """


"""
def load_file2(file_in, file_out):
    out = []
    old_epc = ''
    old_dt = ''
    start_dt = ''
    end_dt = ''
    epc = ''
    dt = ''
    all_count = 0
    good_count = 0
    f = open(file_in, 'r')
    for line in f:
        all_count += 1
        old_epc = epc
        old_dt = dt
        dt = line[0:19]
        epc = line[25:49]
        if epc == old_epc or old_epc == '': end_dt = line[0:19].strip()
        if start_dt == '': start_dt = old_dt
        if epc != old_epc:
            if old_epc != '':
                if end_dt == '': end_dt = start_dt
                print(f"start:{start_dt.strip()}:", f"end:{end_dt.strip()}:")
                df = str(str_to_datetime(end_dt.strip()) - str_to_datetime(start_dt.strip()))
                out.append({'EPC': old_epc, 'StartDT': start_dt, 'EndDT': end_dt, 'Dif': df})
                start_dt = ''
                end_dt = ''
                good_count += 1
    df = str(str_to_datetime(end_dt) - str_to_datetime(start_dt))
    out.append({'EPC': epc, 'StartDT': start_dt, 'EndDT': end_dt, 'Dif': df})
    good_count += 1
    f.close()
    print(f"Файл: {file_in}",
          f"Обработано {all_count} строк, получено записей: {good_count}, ",
          f"процент избыточных данных: {round(int(all_count) / int(good_count) * 100, 2)}%")
    try:
        with open(file_out, 'w') as csvfile:
            fieldnames = ['EPC', 'StartDT', 'EndDT', 'Dif']
            writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames, dialect='excel')
            writer.writeheader()
            writer.writerows(out)
    except:
        print("Файл занят")
    return out
"""
"""
def calc(csv_in, db_in):
    out = []
    for csv_line in csv_in:
        for db_line in db_in:
            if csv_line['EPC'] in db_line['EPC']:
                out.append({'Группа': db_line['Группа'], 'EPC': csv_line['EPC'], 'Start': csv_line['StartDT'],
                            'End': csv_line['EndDT']})
    return out
"""