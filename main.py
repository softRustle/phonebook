import keyboard
import os
import click
import json
import random


def print_menu():
    print('''
                        МЕНЮ
        ========================================

        1. Показать справочник
        2. Добавить контакт
        3. Изменить контакт
        4. Найти контакт(ы)        
        5. Сгенерировать 20 контактов

        press ESC to exit''')


def print_table_header():
    print('''
                                            ТЕЛЕФОННАЯ КНИГА
================================================================================================================
|№     | Имя      |  Фамилия    | Отчество   | Организация                        | Раб. номер | Личн. номер   |
________________________________________________________________________________________________________________   
''')


def print_table_footer():
    print('''
================================================================================================================
  
''')


def rewrite_file(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def generate_number(length):
    generated_number = "".join([str(random.randint(0, 9)) for _ in range(length)])
    return generated_number


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def input_record():
    print('\n')
    record = {"first_name": input('Имя: '),
              "last_name": input('Фамилия: '),
              "father_name": input('Отчество: '),
              "organization": input('Название организации: '),
              "office_number": input('Рабочий номер: '),
              "personal_number": input('Личный номер: ')}
    return record


def print_record(index, record):
    print(f"|{str(index).ljust(6)[:6]}|"
          f"{record['first_name'].ljust(10)[:10]}|"
          f"{record['last_name'].ljust(13)[:13]}|"
          f"{record['father_name'].ljust(12)[:12]}|"
          f"{record['organization'].ljust(36)[:36]}|"
          f"{record['office_number'].ljust(12)[:12]}|"
          f"{record['personal_number'].ljust(15)[:15]}|")


db_path = "data.json"
# Загружает в память данные из файла
try:
    dataList = read_file(db_path)
except FileNotFoundError:
    print(f"База данных {db_path} не существует")
    dataList = []

while True:
    cls()
    print_menu()
    button = keyboard.read_key()
    match button:
        case '1':
            cls()
            print_table_header()
            local_index = 1
            for rec in dataList:
                print_record(local_index, rec)
                local_index += 1
            print_table_footer()
            click.pause()
            click.pause()

        case '2':
            cls()
            print('''
            Новый контакт
========================================''')
            dataList.append(input_record())
            rewrite_file(db_path, dataList)
            click.pause()

        case '3':
            cls()
            local_index = input('Введите номер записи, которую хотите изменить: ')
            # ADD try except on converting user input or otherwise validate it
            if int(local_index) - 1 in range(0, len(dataList)):
                print_table_header()
                rec = dataList[int(local_index) - 1]
                print_record(local_index, rec)
                print_table_footer()
                new_data = input_record()
                dataList[int(local_index) - 1] = new_data
                rewrite_file(db_path,dataList)
            else:
                print("Вы ввели некорректный номер. Уточните его и попробуйте снова.")
            click.pause()

        case '4':
            cls()
            print("Введите параметры поиска далее. Если какой-то параметр не нужен, нажимайте Enter")
            search_data = input_record()
            cls()
            print_table_header()
            local_index = 1
            for rec in dataList:
                if \
                        (
                        rec['first_name'].find(search_data['first_name']) != -1
                        and
                        rec['last_name'].find(search_data['last_name']) != -1
                        and
                        rec['father_name'].find(search_data['father_name']) != -1
                        and
                        rec['organization'].find(search_data['organization']) != -1
                        and
                        rec['office_number'].find(search_data['office_number']) != -1
                        and
                        rec['personal_number'].find(search_data['personal_number']) != -1
                        ):
                    print_record(local_index, rec)
                local_index += 1
            print_table_footer()
            click.pause()

        case '5':
            cls()
            source = "source.txt"
            try:
                file = open(source, "r", encoding="utf-8")
            except FileNotFoundError:
                print(f"    Не найден файл {source}, автозаполнение невозможно.\nВы можете добавить записи вручную.")
            else:
                with file:
                    f_names = file.readline().rstrip().split(",")
                    s_names = file.readline().rstrip().split(",")
                    fth_names = file.readline().rstrip().split(",")
                    orgs = file.readline().rstrip().split(",")
                    prefix = file.readline().rstrip().split(",")

                    for i in range(20):
                        dataList.append({"first_name": f_names[random.randint(0, len(f_names) - 1)],
                                         "last_name": s_names[random.randint(0, len(s_names) - 1)],
                                         "father_name": fth_names[random.randint(0, len(fth_names) - 1)],
                                         "organization": orgs[random.randint(0, len(orgs) - 1)],
                                         "office_number": generate_number(6),
                                         "personal_number":
                                             f"8({prefix[random.randint(0, len(prefix) - 1)]}){generate_number(7)}"})
                    rewrite_file(db_path, dataList)
            click.pause()
        case 'esc':
            cls()
            exit()
