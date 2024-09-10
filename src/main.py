import os.path
import time

from settings import timetable_json_path, timetable_xlsx_path
from convertor import convertor_xlsx_to_json

# Проверяем, есть ли готовый json файл с расписанием
if not os.path.exists(timetable_json_path):

    print(f"В указанной директории ({timetable_json_path}) не был найден файл с расписанием формата json.")
    # Тогда, запускаем программу по его созданию
    if not os.path.exists(timetable_xlsx_path):
        print(f"В указанной директории ({timetable_json_path}) не был найден файл с расписанием формата xlsx.")
        exit()

        # Преобразуем таблицу Excel в JSON
    convertor_xlsx_to_json(timetable_xlsx_path, timetable_json_path)


year = int(input("\n\nВведите год (если в этом году, то можете не заполнять): "))
# Если год не вели, то вводим нынешний
if not year:
    year = time.strftime("%Y")

print("""1 - Январь
2 - Февраль
3 - Март
4 - Апрель
5 - Май
6 - Июнь
7 - Июль
8 - Август
9 - Сентябрь
10 - Октябрь
11 - Ноябрь
12 - Декабрь
""")
month = int(input("Введите месяц (1-12): "))

