import os.path
from datetime import datetime, timedelta

from settings import timetable_json_path, timetable_xlsx_path, token_path, credentials_path, days_in_week
from convertor import Convertor
from src.SKCalendarG import Calendar


def check_even(date):
    """Проверяет дату на четность недели"""
    return date.isocalendar().week % 2


con = Convertor()
cal = Calendar(token_path=token_path, credentials_path=credentials_path)
timetable = con.timetable

con.xlsx2json(timetable_xlsx_path, timetable_json_path)

# Вводим дату, которой будет начинать и заканчивать создавать расписание
start_time = tuple(
        map(
            int,
            input(
                "Введите дату, с которой начнется создание расписания. Заполнить в следующей форме: 2024 12 31\n>>> "
            ).split(),
        )
    )
end_time = tuple(
        map(
            int,
            input(
                "Введите дату, до которой начнется создание расписания. Заполнить в следующей форме: 2024 12 31\n>>> "
            ).split(),
        )
    )

start_time, end_time = datetime(*start_time), datetime(*end_time)
until_date = (end_time.year, end_time.month, end_time.day, 0, 0, 0)

# Создаем чек-лист четных и нечетных недель
check_list = []
for _ in range(7):
    check_list.append([False, False])

# Устанавливаем курсор на первый рассматриваемый день
cur_time = start_time

# Пока не заполнится чек-лист и курсор не дойдет до конца рассматриваемого времени, делать...
while (cur_time <= end_time) and not all([all(num) for num in check_list]):
    # Проверяет дату на четность недели
    even_day = check_even(cur_time)
    # Получаем индекс дня недели 0 - Понедельник, ..., 6 - Воскресенье
    week_day = cur_time.weekday()
    # Если день не Воскресенье И день еще заполнен событием, то...
    if (week_day != 6) and not check_list[cur_time.weekday()][check_even(cur_time)]:
        # Получаем расписание на определенный день недели с четным и нечетным расписанием
        temp = timetable.get(days_in_week[week_day])
        # Если получили пустое расписание (что не должно быть), то...
        if not temp:
            # Текст Ошибки
            error_data = f"День недели не был найден: {even_day=}, {week_day=}, {temp=}"
            raise KeyError(error_data)
        else:
            for day in temp:
                # Если есть занятия, то ...
                if day.get('free'):
                    day = day.get(('right', 'left')[even_day])
                    cal.create_date(
                        summary=day.get("summary"),
                        start=(cur_time.year, cur_time.month, cur_time.day, *map(int, day.get('start').split(':'))),
                        end=(cur_time.year, cur_time.month, cur_time.day, *map(int, day.get('end').split(':'))),
                        description=day.get('description'),
                        location=day.get('location'),
                        repeat_type="weekly",
                        interval=2,
                        until_date=until_date
                    )
            check_list[week_day][even_day] = True
    cur_time += timedelta(days=1)
