import json
import os
from datetime import datetime, timedelta, date
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from calendar import monthrange

from tqdm import tqdm

# Импортируем время занятий из settings.py
from src.settings import time, credentials_path, token_path, timetable_json_path
from src.logger import logger as log
from src.settings import SCOPES

flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)

creds = None
if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
          credentials_path, SCOPES
        )
        creds = flow.run_local_server(port=0)
    with open(token_path, "w") as token:
        token.write(creds.to_json())

service = build('calendar', 'v3', credentials=creds)


# Функция для создания события
def create_event(calendar, event_data):
    print(event_data)
    event = service.events().insert(calendarId=calendar, body=event_data).execute()
    log.info('Событие создано: %s' % (event.get('htmlLink')))


# Функция для получения всех понедельников месяца
def get_mondays_of_month(year: int, month: int) -> list:
    mondays = []
    days_in_month = monthrange(year, month)[1]  # количество дней в месяце
    for day in range(1, days_in_month + 1):
        current_date = date(year, month, day)
        if current_date.weekday() == 0:  # понедельник
            mondays.append(current_date)
    return mondays


# Загружаем расписание из json файла
with open(timetable_json_path, "r", encoding="utf-8") as json_file:
    schedule = json.load(json_file)

# Получаем месяц и год от пользователя
year = int(input("Введите год (например, 2024): "))
month = int(input("Введите месяц (1-12): "))

# Получаем все понедельники выбранного месяца
mondays = get_mondays_of_month(year, month)

# Заполняем расписание для каждой недели месяца
for monday in tqdm(mondays):
    week_start = datetime.combine(monday, datetime.min.time())

    # Определяем, четная ли неделя. Проверяет на четность номер недели
    is_even = week_start.isocalendar().week % 2 == 0

    # Устанавливаем расписание на соответствующую неделю
    for day_name, day_schedule in schedule.items():
        for pair in day_schedule:
            # Если пара свободна, то пропускаем и даже не рассматриваем
            if not pair["free"]:
                continue
            # Определяем, на какую неделю устанавливать пару
            if is_even and ("right" in pair.keys()):
                event_data = pair["right"]
            elif not is_even and ("left" in pair.keys()):
                event_data = pair["left"]
            else:
                # Если произошла ошибка и записалась не как right и left, то пропускаем
                continue

            # Формируем данные для события
            event_data["summary"] = event_data["summary"]
            event_data["location"] = event_data["location"]
            event_data["description"] = event_data["description"]

            # Используем время начала и конца из settings.py
            lesson_number = pair["number"]
            event_start_time_str = time[f"{lesson_number}_start"]
            event_end_time_str = time[f"{lesson_number}_end"]

            # Формируем дату и время начала/окончания пары
            event_start = week_start + timedelta(days=list(schedule.keys()).index(day_name))
            event_start_time = datetime.strptime(event_start_time_str, "%H:%M:%S").time()
            event_end_time = datetime.strptime(event_end_time_str, "%H:%M:%S").time()
            print(f"""
            {event_start=} {event_start}
            {event_start_time=} {event_start_time}
            {event_end_time=} {event_end_time}
            """)

            event_data["start"] = {
                'dateTime': datetime.combine(event_start, event_start_time).strftime('%Y-%m-%dT%H:%M:%S') + '+03:00',
                'timeZone': 'Europe/Moscow',
            }
            event_data["end"] = {
                'dateTime': datetime.combine(event_start, event_end_time).strftime('%Y-%m-%dT%H:%M:%S') + '+03:00',
                'timeZone': 'Europe/Moscow',
            }

            event_data["recurrence"] = [
                'RRULE:FREQ=WEEKLY;COUNT=2'  # Указывает на еженедельное повторение в течение 4 недель
            ]
            print(event_data)

            # Создаем событие в календаре
            # create_event('primary', event_data)
