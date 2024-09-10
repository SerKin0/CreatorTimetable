import json
import math
import pandas as pd

from src.settings import start_points, time, count_lessons


def excel_to_list(file_path):
    # Чтение Excel файла в DataFrame
    df = pd.read_excel(file_path)
    # Преобразование DataFrame в список списков
    data_as_list = df.values.tolist()
    return data_as_list


def check_nan(n):
    return (type(n) is str) or (not math.isnan(n))


def convertor_xlsx_to_json(path_xlsx: str, path_json: str) -> bool:
    data_list = excel_to_list(path_xlsx)
    subjects = {}

    for week in start_points.keys():
        pos = start_points[week]
        lessons_on_day = []
        for number_lesson in range(count_lessons):
            flag = False
            row = pos[0] + 3 * number_lesson
            temp = {"number": number_lesson + 1}
            if check_nan(data_list[row][pos[1]]):
                temp["left"] = {
                    "summary": data_list[row][pos[1]],
                    "location": data_list[row + 1][pos[1]],
                    "description": data_list[row + 2][pos[1]],
                    "start": time[f'{number_lesson + 1}_start'],
                    "end": time[f'{number_lesson + 1}_end']
                }
                flag = True
            if check_nan(data_list[row][pos[1] + 1]):
                temp["right"] = {
                    "summary": data_list[row][pos[1] + 1],
                    "location": data_list[row + 1][pos[1] + 1],
                    "description": data_list[row + 2][pos[1] + 1],
                    "start": time[f'{number_lesson + 1}_start'],
                    "end": time[f'{number_lesson + 1}_end']
                }
                flag = True
            temp['free'] = flag
            lessons_on_day += [temp]
            print(temp)
        subjects[week] = lessons_on_day

    print(subjects)
    # Преобразуем словарь в JSON-строку
    json_string = json.dumps(subjects)

    # Сохраняем JSON-строку в файл
    with open(path_json, "w", encoding="utf-8") as f:
        f.write(json_string)
    return True
