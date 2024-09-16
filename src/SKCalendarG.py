from datetime import datetime

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os
from googleapiclient.discovery import build

from src.settings import SCOPES


def convert_to_iso_format(year, month, day, hour, minute, second, timezone_offset_hours: int = 3):
    """
  Преобразует дату и время в формат ISO 8601.

  Args:
    year: Год.
    month: Месяц.
    day: День.
    hour: Час.
    minute: Минута.
    second: Секунда.
    timezone_offset_hours: Смещение часового пояса от UTC в часах.

  Returns:
    Строка с датой и временем в формате ISO 8601.
  """

    # Создаем объект datetime
    dt = datetime(year, month, day, hour, minute, second)

    # Форматируем дату и время в формате ISO 8601
    iso_format = dt.isoformat() + f"+{timezone_offset_hours:02}:00"

    return iso_format


def format_event_time(start, end):
    return datetime(*start).strftime('%Y%m%dT%H%M%SZ') if datetime(*start).date() == datetime(*end).date() else None


class Calendar:
    def __init__(self, token_path: str, credentials_path: str) -> None:
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

        self.service = build('calendar', 'v3', credentials=creds)

    def create_date(self,
                    summary: str,
                    start: tuple,
                    end: tuple,
                    location: str = "",
                    description: str = "",
                    time_zone: str = "Europe/Moscow",
                    repeat_type: str = "none",  # "daily", "weekly", "monthly", "yearly", "none"
                    count_repeat: int = 0,  # Количество повторений
                    interval: int = 0,
                    until_date: tuple = None,  # Дата окончания повторения
                    recurrence: str = "",  # Пользовательский параметр повторения
                    calendar: str = "primary",
                    print_link: bool = False
                    ):
        """
        Создание нового события
        Args:
            summary: Название события
            start: Время начала мероприятия. Пример: (2024, 3, 9, 7, 0, 0) - год, месяц, день, час, мин., сек.
            end: Время конца мероприятия. Пример: (2024, 3, 9, 8, 0, 0) - год, месяц, день, час, мин., сек.
            location: Место мероприятия
            description: Описание мероприятия
            time_zone: Временная зона (см. документация в Google)
            repeat_type: Интервал повторений события по дням ("daily"), неделям ("weekly"), месяцам ("monthly"), годам
            ("yearly"), либо без повторений
            count_repeat: Количество повторений
            interval: Интервал времени между мероприятиями. ! Работает вместе с repeat_type !
            until_date: Дата окончания повторения. Пример: (2024, 12, 9, 8, 0, 0) - год, месяц, день, час, мин., сек.
            recurrence: Пользовательский параметр повторения
            calendar:
            print_link:

        Returns:

        """
        event_data = {
            "summary": summary,
            "start": {
                "dateTime": convert_to_iso_format(*start),
                "timeZone": time_zone
            },
            "end": {
                'dateTime': convert_to_iso_format(*end),
                'timeZone': time_zone,
            }
        }
        if location:
            event_data["location"] = location
        if description:
            event_data["description"] = description

        if count_repeat > 0 or repeat_type != "none":
            # Добавляем параметр повторения
            if recurrence:
                event_data["recurrence"] = [recurrence]
            else:
                recurrence_rule = f"RRULE:FREQ={repeat_type.upper()};"
                if until_date:
                    recurrence_rule += f"UNTIL={datetime(*until_date).strftime('%Y%m%dT%H%M%S')}Z"
                    if interval != 0:
                        recurrence_rule += f";INTERVAL={interval}"
                elif count_repeat > 0:
                    recurrence_rule += f"COUNT={count_repeat}"
                event_data["recurrence"] = [recurrence_rule]
        print(event_data)
        event = self.service.events().insert(calendarId=calendar, body=event_data).execute()
        if print_link:
            print('Событие создано: %s' % (event.get('htmlLink')))
