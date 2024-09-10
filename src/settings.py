# В нее записывается время начала и конца занятия (формат записи: 00:00:00)
time = {
    "1_start": "07:30:00", "1_end": "09:00:00",
    "2_start": "09:10:00", "2_end": "10:40:00",
    "3_start": "10:50:00", "3_end": "12:20:00",
    "4_start": "13:00:00", "4_end": "14:30:00",
    "5_start": "14:40:00", "5_end": "16:10:00",
    "6_start": "16:20:00", "6_end": "17:50:00"
}

# Индексы для обращения к левому верхнему элементу дня в таблице Excel
start_points = {
    "Понедельник": (1, 2),
    "Вторник": (19, 2),
    "Среда": (37, 2),
    "Четверг": (1, 6),
    "Пятница": (19, 6),
    "Суббота": (37, 6)
}

# Количество занятий/пар в день
count_lessons = 6

# Если измените эти значения, удалите файл token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Пути
timetable_json_path = '../files/timetable.json'
timetable_xlsx_path = "../files/timetable.xlsx"
credentials_path = "../files/credentials.json"
token_path = '../files/token.json'

