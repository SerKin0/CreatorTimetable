import os.path
import time
from datetime import datetime

from settings import timetable_json_path, timetable_xlsx_path
from src.convertor import xlsx2json

# Проверяем, есть ли готовый json файл с расписанием
if not os.path.exists(timetable_json_path):

    print(f"В указанной директории ({timetable_json_path}) не был найден файл с расписанием формата json.")
    # Тогда, запускаем программу по его созданию
    if not os.path.exists(timetable_xlsx_path):
        print(f"В указанной директории ({timetable_json_path}) не был найден файл с расписанием формата xlsx.")
        exit()
        # Преобразуем таблицу Excel в JSON
    xlsx2json(timetable_xlsx_path, timetable_json_path)

start_time = tuple(map(int, input("Введите дату, с которой начнется создание расписания. "
                   "Заполнить в следующей форме: 2024 12 31\n>>> ").split()))
end_time = tuple(map(int, input("Введите дату, до которой начнется создание расписания. "
                 "Заполнить в следующей форме: 2024 12 31\n>>> ").split()))

print(datetime.combine(datetime(*start_time), datetime.min.time()).isocalendar().week % 2 == 0)
print(datetime.combine(datetime(*end_time), datetime.min.time()).isocalendar().week % 2 == 0)

print(datetime(*start_time).weekday())
print(datetime(*end_time).weekday())
